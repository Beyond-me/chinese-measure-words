from django.shortcuts import render

# Create your views here.
# vocabulary/views.py
from django.shortcuts import render, get_object_or_404
from .models import Level, Category, Word


def index_view(request):
    """
    首页：展示 HSK 级别
    """
    levels = Level.objects.all()
    return render(
        request,
        'vocabulary/index.html',
        {
            'levels': levels
        }
    )


def level_view(request, level_slug):
    """
    HSK 级别页：展示分类
    """
    level = get_object_or_404(Level, id=level_slug)
    categories = level.category_set.all()
    return render(request, 'vocabulary/level.html', {
        'level': level,
        'categories': categories
    })


def category_view(request, category_id):
    """
    分类页：展示词汇列表
    """
    category = get_object_or_404(Category, id=category_id)
    words = category.word_set.all()
    return render(request, 'vocabulary/category.html', {
        'category': category,
        'words': words
    })


def word_detail_view(request, word_id):
    """
    词汇详情页
    """
    word = get_object_or_404(Word, id=word_id)
    return render(request, 'vocabulary/word_detail.html', {
        'word': word
    })