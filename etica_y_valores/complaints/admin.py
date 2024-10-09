from django.contrib import admin

from .models import (
    ComplaintModel,
    EmailModel,
    PhoneModel,
    FileModel,
    ChannelCategoryModel,
    CityCategoryModel,
    ClassificationCategoryModel,
    CommentModel,
    PhoneTypeCategoryModel,
    PriorityCategoryModel,
    RelationCategoryModel,
    StatusCategoryModel,
    LogModel,
)


from django.utils.html import format_html
from django.urls import reverse


class FileInline(admin.TabularInline):
    model = FileModel
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = ['file', 'decrypted_file']

    def decrypted_file(self, obj):
        """
        Muestra un enlace para descargar el archivo desencriptado.
        """

        if obj.id:
            url = reverse('app_complaints:view_pdf', args=[obj.id])
            return format_html('<a href="{}" target="_blank">PDF</a>', url)

    decrypted_file.short_description = "Ver PDF"


class EmailInline(admin.TabularInline):
    model = EmailModel
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = ['email']


class PhoneInline(admin.TabularInline):
    model = PhoneModel
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = ['phone_type', 'phone_number']


@admin.register(ComplaintModel)
class ComplaintAdmin(admin.ModelAdmin):
    inlines = [FileInline, EmailInline, PhoneInline]


class EmailAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PhoneAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class FileAdmin(admin.ModelAdmin):

    list_display = ('id', 'view_pdf_link',)

    def has_change_permission(self, request, obj=None):
        return False

    def view_pdf_link(self, obj):
        url = reverse('app_complaints:view_pdf', args=[obj.id])
        return format_html('<a href="{}" target="_blank">{}</a>', url, obj.file.name)

    view_pdf_link.short_description = 'PDF'


admin.site.register(EmailModel, EmailAdmin)
admin.site.register(PhoneModel, PhoneAdmin)
admin.site.register(FileModel, FileAdmin)
admin.site.register(ChannelCategoryModel)
admin.site.register(CityCategoryModel)
admin.site.register(ClassificationCategoryModel)
admin.site.register(CommentModel)
admin.site.register(PriorityCategoryModel)
admin.site.register(PhoneTypeCategoryModel)
admin.site.register(RelationCategoryModel)
admin.site.register(StatusCategoryModel)
admin.site.register(LogModel)
