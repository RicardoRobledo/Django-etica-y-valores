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


class FileInline(admin.TabularInline):
    model = FileModel
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = ['file']


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

    pass


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
