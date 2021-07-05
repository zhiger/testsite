from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import News, Category


""" Редактор формы """
class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewAdmin(admin.ModelAdmin):
    form = NewsAdminForm # для админки подключаем данный класс
    list_display = ('id', 'title', 'category',
                    'created_te', 'updated_at', 'is_published')

    list_display_links = ['id', 'title']
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('category', 'is_published')

    fields = ('title', 'content', 'photo',
              'get_photo',  'category', 'is_published',
              'views', 'created_te', 'updated_at')

    readonly_fields = ('views', 'created_te', 'updated_at', 'get_photo')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src = " {obj.photo.url}" width="50">')

    get_photo.short_description = "Миниатюра"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ['id', 'title']
    search_fields = ('title',)



admin.site.register(News, NewAdmin)
admin.site.register(Category, CategoryAdmin)

