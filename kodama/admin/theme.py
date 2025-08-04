from django.contrib import admin
from kodama.models import Theme
from import_export import resources
from django.http import HttpResponse
import json
from django import forms
import logging
from kodama.models import Font


logger = logging.getLogger("django")

class ThemeResource(resources.ModelResource):

    def export(self, queryset):
        data = []
        for obj in queryset:
            data.append({
                "id": obj.id,
                "name": obj.name,
                "theme": obj.theme,
                "font": obj.font.name if obj.font else None
            })
        return data

    class Meta:
        model = Theme
        fields = ("id", "name", "theme")


class ThemeAdminForm(forms.ModelForm):
    upload = forms.FileField(required=False, help_text="Upload a JSON file to populate 'data'")

    class Meta:
        model = Theme
        fields = ['name', 'theme', 'font']  # ⬅️ Add font to form

    def clean(self):
        cleaned_data = super().clean()
        upload = self.files.get('upload')

        if upload:
            try:
                file_content = upload.read().decode()
                json_data = json.loads(file_content)

                if isinstance(json_data, list) and json_data:
                    json_data = json_data[0]

                if isinstance(json_data, dict):
                    cleaned_data['theme'] = json_data.get('theme', cleaned_data.get('theme'))
                    cleaned_data['name'] = json_data.get('name', cleaned_data.get('name'))

                    # Optional: match font by name if provided in JSON
                    font_name = json_data.get('font')
                    if font_name:
                        try:
                            font = Font.objects.get(name=font_name)
                            cleaned_data['font'] = font
                        except Font.DoesNotExist:
                            self.add_error('upload', f"Font '{font_name}' not found in database.")
                else:
                    self.add_error('upload', "Unsupported JSON structure. Must be a dict or a non-empty list of dicts.")

            except UnicodeDecodeError:
                self.add_error('upload', "File could not be decoded. Ensure it's a valid text file.")
            except json.JSONDecodeError:
                self.add_error('upload', "Invalid JSON format.")
            except Exception as e:
                logger.warning("Unexpected error during upload: %s", str(e))
                self.add_error('upload', "Unexpected error while processing file.")

        return cleaned_data


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    resource_class = ThemeResource
    list_display = ("name", "font")  # ⬅️ Show font name
    search_fields = ("name", "font__name")
    readonly_fields = ("id",)
    fieldsets = (
        (None, {
            "fields": ("name", "font", "upload")  # ⬅️ Add font selector
        }),
        ("Theme Tokens", {
            "classes": ("collapse",),
            "fields": ("theme", )
        }),
    )

    actions = ["download_selected_themes"]
    form = ThemeAdminForm

    def download_selected_themes(self, request, queryset):
        resource = self.resource_class()
        parsed_data = resource.export(queryset)

        exported_json = json.dumps(parsed_data, indent=2)
        response = HttpResponse(exported_json, content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename="themes.json"'
        return response

    download_selected_themes.short_description = "Download selected themes as JSON"


@admin.register(Font)
class FontAdmin(admin.ModelAdmin):
    list_display = ('name', 'cdn_link')
    search_fields = ('name', 'cdn_link')
