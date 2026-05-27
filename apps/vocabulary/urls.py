# vocabulary/urls.py
from django.urls import path
from . import views

app_name = 'vocabulary'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('<int:level_slug>/', views.level_view, name='level'),
    path('category/<int:category_id>/', views.category_view, name='category'),
    path('word/<int:word_id>/', views.word_detail_view, name='word_detail'),
]