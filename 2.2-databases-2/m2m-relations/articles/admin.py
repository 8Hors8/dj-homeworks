from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Article, Tag, ArticleScope


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_scope_count = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_main', False):
                    main_scope_count += 1
        if main_scope_count == 0:
            raise ValidationError('Должен быть хотя бы один основной тег (is_main=True).')
        if main_scope_count > 1:
            raise ValidationError('Может быть только один основной тег.')
        return super().clean()


class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleScopeInline]

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
