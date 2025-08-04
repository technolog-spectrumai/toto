from django.contrib import admin
from kodama.models import Section, SiteConfig
from django_tiptap.widgets import TipTapWidget
from django import forms
from django_tiptap.widgets import TipTapWidget


class SectionAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config = SiteConfig.objects.first()
        use_wysiwyg = getattr(config, "enable_wysiwyg", True)

        if use_wysiwyg:
            self.fields['content'].widget = TipTapWidget()
        else:
            self.fields['content'].widget = forms.Textarea(attrs={'rows': 15})

    class Meta:
        model = Section
        fields = '__all__'


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    form = SectionAdminForm
    list_display = ('title', 'article', 'order')
    list_filter = ('article',)
    search_fields = ('title', 'content')
    ordering = ('article', 'order')
