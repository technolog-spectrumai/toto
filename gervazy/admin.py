from django.contrib import admin
from django.utils.html import format_html
from .models import TLSCertificate


@admin.register(TLSCertificate)
class TLSCertificateAdmin(admin.ModelAdmin):
    list_display = ('common_name', 'organization_name', 'country_name', 'state_or_province_name', 'locality_name',
                    'qr_code_preview')
    search_fields = ('common_name', 'organization_name')
    list_filter = ('country_name', 'state_or_province_name')
    ordering = ('organization_name',)
    readonly_fields = ('certificate', 'qr_code_preview', 'qr_code',)  # QR code is read-only
    exclude = ('private_key', )
    fieldsets = (
        ("Certificate Details", {
            "fields": ("common_name", "organization_name", "certificate", "qr_code_preview", 'qr_code'),
        }),
        ("Location Information", {
            "fields": ("country_name", "state_or_province_name", "locality_name"),
        }),
    )

    def qr_code_preview(self, obj):
        """Display QR code preview in the admin interface."""
        if obj.qr_code:
            size = 256
            html = '<img src="{}"' + f'width="{size}" height="{size}"' + ' alt="QR Code" />'
            return format_html(html, obj.qr_code.url)
        return "No QR Code Available"

    qr_code_preview.short_description = "QR Code Preview"
