from django.db import models

# Create your models here.
# vocabulary/models.py
from django.db import models
from apps.common.utils.tts import generate_tts_audio
from django.utils.text import slugify


class Level(models.Model):
    """
    HSK 级别
    """
    name = models.CharField(
        max_length=10,
        unique=True,
        choices=[
            ('HSK1', 'HSK1'),
            ('HSK2', 'HSK2'),
            ('HSK3', 'HSK3'),
            ('HSK4', 'HSK4'),
        ]
    )
    order = models.PositiveSmallIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "级别"
        verbose_name_plural = "级别"
        ordering = ['order']

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    词汇分类（物品 / 饮食 / 交通）
    """
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ['level__order', 'order']


    def __str__(self):
        return f'{self.level.name} - {self.name}'



class Word(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="所属分类")
    chinese = models.CharField(max_length=50, verbose_name="汉字")
    pinyin = models.CharField(max_length=100, verbose_name="拼音")
    english = models.CharField(max_length=200, verbose_name="英文释义")
    measure_word = models.CharField(max_length=20, blank=True, verbose_name="量词")
    example = models.CharField(max_length=200, blank=True, verbose_name="例句")

    audio_zh = models.FileField(upload_to='audio/zh/', blank=True, verbose_name="中文音频")
    audio_en = models.FileField(upload_to='audio/en/', blank=True, verbose_name="英文音频")

    order = models.IntegerField(default=0, verbose_name="排序")
    image = models.ImageField(upload_to='images/', blank=True, verbose_name="图片")

    class Meta:
        verbose_name = "词汇"
        verbose_name_plural = "词汇"
        ordering = ['id']

    def save(self, *args, **kwargs):
        """
        ✅ 自动生成 TTS 音频
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            if not self.audio_zh:
                zh_path = generate_tts_audio(self.chinese, lang='zh')
                self.audio_zh = zh_path

            if not self.audio_en:
                en_path = generate_tts_audio(self.english, lang='en')
                self.audio_en = en_path

            super().save(update_fields=['audio_zh', 'audio_en'])