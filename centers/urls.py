from django.urls import path
from . import views


urlpatterns = [
    path('centers/', views.centers_list_view, name='centers_list'),
    # path('centers/<int:pk>/', views.center_detail_view, name='center'),
    path('centers/create/', views.create_center_view, name='create_center'),
    path('centers/<int:pk>/students/', views.student_list_view, name='students_list'),
    path('centers/<int:pk>/students/create/', views.create_student_view, name='create_student'),
    path('group-trial/crate/', views.create_group_trial_view, name='create_group_trial'),
    path('group/create/', views.create_group, name='create_group'),
    path('group-trial/<int:pk>/', views.group_detail_trial_view, name='group_detail_trial'),
    path('group/<int:pk>/', views.group_detail_view, name='group_detail'),
    path('centers/<int:pk>/first-call/', views.first_call_view, name='first_call'),
    path('centers/<int:pk>/second-call/', views.second_call_view, name='second_call'),
    path('first-call/update/<int:pk>/', views.first_call_student_update_view, name='student_update'),
    path('second-call/update/<int:pk>/', views.second_call_student_update_view, name='student_update_second'),
]
