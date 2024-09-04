from .models import Email, Phone, File
from django.contrib import admin

from .models import Complaint, Email, Phone, File


class FileInline(admin.TabularInline):
    model = File
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = ['file']


class EmailInline(admin.TabularInline):
    model = Email
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = ['email']


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = ['phone_type', 'phone_number']


@admin.register(Complaint)
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

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Email, EmailAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(File, FileAdmin)
