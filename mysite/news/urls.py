from django.urls import path

from .views import *

urlpatterns = [
    # path('', index, name='home'),
    path('', HomeNews.as_view(), name='home'),
    # path('category/<int:category_id>/', get_category, name='category'),
    path('category/<int:category_id>/', NewsCategory.as_view(), name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('view_news/<int:pk>/', ViewNews.as_view(), name='view_news'), # news_id на pk в моделях тоже меняемм
    # path('news/add-news/', add_news, name='add-news'),
    path('form_news/add_news/', CreateNews.as_view(), name='add_news'),
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]

# path(route, view, kwargs=None, name=None)
# route - маршрут
# view - вид
# name - имя шаблона

# path('', index, name='home'),     при функцанальном представлении
# path('', HomeNews.as_view(), name='home'),  # при классовых представлении
# <int:category_id> - int тип перемнный , category_id сам переменный(параметр)