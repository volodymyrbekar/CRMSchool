from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Center, Student, GroupTrial, GroupPermanent


User = get_user_model()


class CenterAdmin(admin.ModelAdmin):
    list_display = ['center_name', 'location', 'created_at', 'unique_link']
    search_fields = ['center_name', 'location']
    actions = ['generate_unique_link', 'deactivate_unique_link']
    readonly_fields = ['unique_link']
    change_form_template = 'admin/centers/center/center_change_form.html'

    def generate_unique_link(self, request, queryset):
        for center in queryset:
            if center.unique_link is None:
                center.generate_unique_link()
        self.message_user(request, 'Unique link - згенеровано')
    generate_unique_link.short_description = 'Generate unique link'

    def deactivate_unique_link(self, request, queryset):
        queryset.update(unique_link=None)
        self.message_user(request, 'Unique link - деактивовано')
    deactivate_unique_link.short_description = 'Deactivate unique link'


class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_full_name', 'student_phone_number', 'parent_phone_number', 'school',
                    'class_number', ]
    search_fields = ['student_full_name', 'student_phone_number', 'school']


class GroupTrialAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'center']
    search_fields = ['group_name', 'center']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'center']
    search_fields = ['group_name', 'center']


admin.site.register(Center, CenterAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(GroupPermanent)
admin.site.register(GroupTrial)

