from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Center, Student, GroupTrial, GroupPermanent


User = get_user_model()


class CenterAdmin(admin.ModelAdmin):
    list_display = ['center_name', 'location', 'created_at']
    search_fields = ['center_name', 'location']


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

