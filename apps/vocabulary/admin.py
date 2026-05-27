from django.contrib import admin
from .models import Level, Category, Word


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'order')
    list_filter = ('level',)
    ordering = ('level__order', 'order')


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = (
        'chinese',
        'pinyin',
        'english',
        'measure_word',
        'category',
        'order',
    )
    list_filter = ('category__level', 'category')
    search_fields = ('chinese', 'pinyin', 'english')
    ordering = ('category__level__order', 'category__order', 'order')

    fieldsets = (
        ('基本信息', {
            'fields': ('category', 'chinese', 'pinyin', 'english')
        }),
        ('量词与例句', {
            'fields': ('measure_word', 'example')
        }),
        ('媒体', {
            'fields': ('image', 'audio_zh', 'audio_en')
        }),
        ('排序', {
            'fields': ('order',)
        }),
    )

    # ✅ 防止你手点保存时重复生成 TTS
    readonly_fields = ('audio_zh', 'audio_en')
