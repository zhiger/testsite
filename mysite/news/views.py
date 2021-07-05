from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .models import News, Category
from .utils import MyMixin
from django.contrib import messages
from django.core.paginator import Paginator


""" Классы представлении"""


class HomeNews(MyMixin, ListView):
    """ Главная страница """
    model = News
    # указываем тот шаблон который хотим отобразить вместо news_list.html
    template_name = 'news/index.html'

    # указываем тот объект с которым хотим работать вместо object_list в шаблоне index.html
    context_object_name = 'news_index'

    # желательно только для статичных данных, для динамичных страниц не
    # рекамендуеся, для этого есть метод get_context_data
    # extra_context = {'title':"Главная"}
    mixin_prop = 'this is mixin'  # выводится через файл nav.html

    # Целое число, указывающее, сколько объектов должно отображаться на странице.
    # Если это задано, представление будет разбивать объекты на страницы с объектами
    # paginate_by на каждой странице.
    paginate_by = 4

    # Целое число, определяющее количество объектов «переполнения», которые может
    # содержать последняя страница. Это увеличивает ограничение paginate_by на
    # последней странице до paginate_orphans, чтобы на последней странице не было
    # очень маленького количества объектов.
    paginate_orphans =2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # Выводим title, mixin_prop в верхним регистре используя миксин
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_mixin_prop()
        return context

    def get_queryset(self):
        """ выбирает только опубликованные """
        return News.objects.filter(is_published=True).select_related('category')

        # select_related(*fields)
        # Повышает производительность, т.к. при доступе к связанным объектам через модель не
        # потребуются дополнительные запросы в базу данных


class NewsCategory(MyMixin, ListView):
    """ Категория """
    model = News
    # по-умолчанию создаст шаблон news_list.html, чтобы переопределить вызовим атрибут template_name
    template_name = 'news/category.html'
    context_object_name = 'news_category'
    allow_empty = False
    #extra_context = {'title':"Категория"}
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        # category_id , здесь мы используем миксин
        return context

    def get_queryset(self):
        """ выбирает только опубликованные """
        return News.objects.filter(category_id=self.kwargs['category_id'],
                                   is_published=True).select_related('category')


class ViewNews(DetailView):
    """ Страница контента """
    model = News
    # по-умолчанию создаст шаблон news_detail.html, чтобы переопределить вызовим атрибут template_name
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    """ Форма """
    form_class = NewsForm
    template_name = 'news/add_news.html'
    context_object_name = 'add_news'
    # success_url = reverse_lazy('home')    # после отправки формы перенаправляет на главную страницу
    #login_url = '/admin/' # при вводе http://127.0.0.1:8000/form_news/add_news/ перенапрвит вход в admin панель
    #login_url = reverse_lazy('home') # при попытке получит доступ по ссылке, перенаправляет на галвную страницу
    # ( не забудьте импортировать reverse_lazy)
    raise_exception = True # при попытке получит доступ по ссылке, бросает исключение 403 Forbidden


""" РЕГИСТРАЦИЯ """
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


""" ЛОГИН """
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


""" ВЫХОД """
def user_logout(request):
    logout(request)
    return redirect('login')


""" Отправка письем"""
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'],
                             form.cleaned_data['content'],
                             'zhiger_alban89@mail.ru', ['zhiger2007@gmail.com'],
                             fail_silently=True)
            if mail:
                messages.success(request, 'Отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидаций')
    else:
        form = ContactForm()
    return render(request, 'news/contact.html', {'form': form})

""" Функции представлении"""
# так как в news/urls.py мы изменили и вместо функций вызвали класс нам не понадобится эти функций

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список сериалов',
#     }
#     return render(request, 'news/index.html',context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news':news,'category':category})

# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})

# def add_news(request):
#     if request.method == 'POST':  # если данные пришли методом
#         form = NewsForm(request.POST)  # то мы создаём объект формы и заполняем его полученными данными и формы
#         if form.is_valid():  # проверяем прошла ли наши данные валидацию
#             # news = News.objects.create(**form.cleaned_data) # в случай если форма не связаной моделями
#             news = form.save()  # в случай если форма связаной моделями
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})


# Пагинация стрраниц
# def test(request):
#     #objects = ['john', 'paul', 'george', 'ringo',
#     #           'john2', 'paul2', 'george2', 'ringo2',
#      #          'john3', 'paul3', 'george3', 'ringo3']
#
#     objects = News.objects.all()
#     paginator = Paginator(objects, 4) # Экземпляр класса Paginator, 2-ой аргумент кол.записей в одной странице
#     page_num = request.GET.get('page', 1) # номер текущей страницы
#     page_objects = paginator.get_page(page_num)
#     # Возвращает объект, Page соответствующий индексу number (начиная с 1), также обрабатывая недопустимые или выходящие за пределы диапазона номера страниц
#
#     # page_objects = paginator.page(page_num)
#     # Возвращает объект, Page соответствующий индексу number (начиная с 1). Если указанный номер страницы не существует, создается исключение InvalidPage .
#     return render(request, 'news/contact.html', {'page_obj': page_objects})