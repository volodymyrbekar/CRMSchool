from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods

from .forms import CreateCenterForm, CreateStudentForm, CreateGroupTrialForm, CreateGroupForm, UpdateStudentFirstForm, UpdateStudentSecondForm
from .models import Center, Student, GroupTrial, GroupPermanent
from users.models import CustomUser


@login_required
def centers_list_view(request):
    centers_obj = Center.objects.all()
    context = {
        'title': 'Центри',
        'centers': centers_obj,
    }
    return render(request, 'centers/centers_list.html', context)  # This is the file that will be rendered


@login_required
@permission_required('users.can_add_centers', raise_exception=True)
def create_center_view(request):
    # if not request.user.has_perm('users.centers'):
    #     raise PermissionDenied("You do not have permission to create a center")
    form = CreateCenterForm(request.POST or None)
    breadcrumbs = [
        ('Центри', '/centers/'),  # Centers list page
    ]
    context = {
        'title': 'Створити центр',
        'form': form,
        'breadcrumbs': breadcrumbs,
        }
    if request.method == 'POST':
        if form.is_valid():
            create_center = form.save()
            context['form'] = CreateCenterForm()
            messages.success(request, 'Center created successfully')
            return redirect('centers_list')
    return render(request, 'centers/create_center.html', context)


@login_required
def student_list_view(request, pk):
    print(request.user.__dict__)
    try:
        center_obj = Center.objects.get(pk=pk)
    except Center.DoesNotExist:
        raise Http404("Center does not exist")
    student_obj = Student.objects.filter(center_id=pk).order_by('-student_add_date').all()

    paginator = Paginator(student_obj, 50)  # Show 10 students per page
    page_number = request.GET.get('page')
    student_obj_page = paginator.get_page(page_number)

    breadcrumbs = [
        ('Центри', '/centers/'),  # Centers list page
        (center_obj.center_name, f'/centers/{center_obj.id}/students')
    ]

    group_trial_obj = GroupTrial.objects.filter(center_id=pk).all()
    group_obj = GroupPermanent.objects.filter(center_id=pk).all()
    context = {
        'title': 'Студенти',
        'student_obj_page': student_obj_page,
        'center_obj': center_obj,
        'group_trial_obj': group_trial_obj,
        'group_obj': group_obj,
        'breadcrumbs': breadcrumbs,

    }
    return render(request, 'students/students_list.html', context)


@login_required
def create_student_view(request, pk):
    center = get_object_or_404(Center, pk=pk)
    form = CreateStudentForm(request.POST or None, initial={'center': pk})
    breadcrumbs = [
        ('Центри', '/centers/'),  # Centers list page
        (center.center_name, f'/centers/{center.id}/students'),  # Current center page
        ('Додати учня', request.path),  # Current page
    ]

    context = {
        'title': 'Додати студента',
        'form': form,
        'center': center,
        'pk': pk,
        'breadcrumbs': breadcrumbs,
    }
    if request.method == 'POST':
        if form.is_valid():
            create_student = form.save()
            context['form'] = CreateStudentForm(initial={'center': pk})
            success_message = f'Учень <strong>{create_student.student_full_name}</strong> успішно оновлений'
            messages.success(request, mark_safe(success_message))
            # return redirect('students_list')
    return render(request, 'students/create_student.html', context)


def create_student_with_token(request, pk, token):
    center = get_object_or_404(Center, pk=pk)
    form = CreateStudentForm(request.POST or None, initial={'center': center.pk})
    currect_link = Center.objects.get(pk=pk).unique_link

    if center.unique_link is None or center.unique_link != currect_link:
        raise Http404("This link has been deactivated.")

    context = {
        'title': 'Додати учня',
        'form': form,
        'center': center,
        'pk': pk,
        'token': token,
    }
    if request.method == 'POST':
        if form.is_valid():
            create_student = form.save()
            context['form'] = CreateStudentForm(initial={'center': pk})
            success_message = f'Учень <strong>{create_student.student_full_name}</strong> успішно створений'
            messages.success(request, mark_safe(success_message))
    return render(request, 'students/create_student_with_token.html', context)


@login_required
@permission_required('users.can_edit_first_call', raise_exception=True)
def first_call_student_update_view(request, pk):
    student = get_object_or_404(Student, id=pk)
    form = UpdateStudentFirstForm(center_instance=student.center, instance=student)
    User = get_user_model()
    all_users = User.objects.all()
    group_trials = GroupTrial.objects.filter(center=student.center)
    context = {
        'title': 'Перший дзвінок',
        'form': form,
        'student_obj': student,
        'user': request.user,
        'operators': all_users,
        'group_trials': group_trials,
    }
    if request.method == 'POST':
        form = UpdateStudentFirstForm(request.POST, center_instance=student.center, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            group_trial_id = request.POST.get('group_trial')
            if group_trial_id:
                student.trial_registration = GroupTrial.objects.get(id=group_trial_id)
            else:
                student.trial_registration = None
            student.save()
            success_message = f'Учень <strong>{form.instance.student_full_name}</strong> успішно оновлений'
            messages.success(request, mark_safe(success_message))
            return redirect('first_call', pk=student.center.pk)
        else:
            # print(form.errors)
            messages.error(request, 'Помилка валідації форми. Будь ласка, перевірте дані')
    return render(request, 'students/first_call_student_update.html', context)


@login_required
@permission_required('users.can_edit_second_call', raise_exception=True)
def second_call_student_update_view(request, pk):
    try:
        student = get_object_or_404(Student, id=pk)
        form = UpdateStudentSecondForm(center_instance=student.center, instance=student)
        User = get_user_model()
        all_users = User.objects.all()
        group_permanents = GroupPermanent.objects.filter(center=student.center)
        context = {
            'title': 'Другий дзвінок',
            'form': form,
            'student_obj': student,
            'user': request.user,
            'operators': all_users,
            'group_permanents': group_permanents,
        }
        if request.method == 'POST':
            form = UpdateStudentSecondForm(request.POST or None, center_instance=student.center, instance=student)
            if form.is_valid():
                student = form.save(commit=False)
                group_id = request.POST.get('add_to_group')
                if group_id:
                    # Assign the selected group to the student
                    student.add_to_group = GroupPermanent.objects.get(id=group_id)
                else:
                    # If no group selected, set it to None
                    student.add_to_group = None

                student.save()
                success_message = f'Учень <strong>{form.instance.student_full_name}</strong> успішно оновлений'
                messages.success(request, mark_safe(success_message))
                return redirect('second_call', pk=student.center.pk)
            else:
                print(form.errors)
                messages.error(request, 'Помилка валідації форми. Будь ласка, перевірте дані')
        return render(request, 'students/second_call_student_update.html', context)
    except Student.DoesNotExist:
        messages.error(request, "Студент із зазначеним id не знайдений")
        return redirect('centers_list')


@login_required
@permission_required('users.can_add_grouptrial', raise_exception=True)
def create_group_trial_view(request):
    form = CreateGroupTrialForm(request.POST or None)
    context = {
        'title': 'Створити групу пробна',
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            create_group_trial = form.save()
            context['form'] = CreateGroupTrialForm()
            success_message = f'Група <strong>{create_group_trial.group_name}</strong> на пробне успішно створена'
            messages.success(request, mark_safe(success_message))
            return redirect('centers_list')
    return render(request, 'groups/create_group_trial.html', context)


@login_required
def group_detail_trial_view(request, pk):
    try:
        group_trial_obj = GroupTrial.objects.get(pk=pk)
        center = group_trial_obj.center
    except GroupTrial.DoesNotExist:
        raise Http404("Group does not exist")
    student_obj = Student.objects.filter(center=center, trial_registration=group_trial_obj).order_by('-student_add_date')
    breadcrumbs = [
        ('Центри', '/centers/'),  # Centers list page
        (center.center_name, f'/centers/{center.id}/students'),  # Current center page
        (group_trial_obj.group_name, request.path),  # Current page
    ]
    context = {
        'title': group_trial_obj,
        'group_trial_obj': group_trial_obj,
        'student_obj': student_obj,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'groups/group_detail_trial.html', context)


@login_required
@permission_required('users.can_add_grouppermanent', raise_exception=True)
def create_group(request):

    form = CreateGroupForm(request.POST or None)
    context = {
        'title': 'Створити групу постійна',
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            create_group = form.save()
            context['form'] = CreateGroupForm()
            success_message = f'Група <strong>{create_group.group_name}</strong> успішно створена'
            messages.success(request, mark_safe(success_message))
            return redirect('centers_list')
    return render(request, 'groups/create_group_permanent.html', context)


@login_required
def group_detail_view(request, pk):
    try:
        group_obj = GroupPermanent.objects.get(pk=pk)
        center = group_obj.center
    except GroupPermanent.DoesNotExist:
        raise Http404("Group does not exist")
    student_obj = Student.objects.filter(center=center, add_to_group=group_obj).order_by('-student_add_date')
    breadcrumbs = [
        ('Центри', '/centers/'),  # Centers list page
        (center.center_name, f'/centers/{center.id}/students'),  # Current center page
        (group_obj.group_name, request.path),  # Current page
    ]
    context = {
        'title': group_obj,
        'group_obj': group_obj,
        'student_obj': student_obj,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'groups/group_detail_permanent.html', context)


@login_required
def first_call_view(request, pk):
    try:
        center_obj = get_object_or_404(Center, pk=pk)
        operators = CustomUser.objects.filter(role='operator')
        selected_operator = request.GET.get('operator')
        # students = Student.objects.filter(center=center_obj)
        student_obj = Student.objects.filter(center=center_obj)
        if selected_operator:
            student_obj = student_obj.filter(first_call=selected_operator)
    except Center.DoesNotExist:
        raise Http404("Центр не знайдений")

    breadcrumbs = [
        ('Центри', '/centers/'),  # Centers list page
        (center_obj.center_name, f'/centers/{center_obj.id}/students'),  # Current center page
        ('Перший дзвінок', request.path),  # Current page
    ]

    context = {
        'title': 'Перший дзвінок',
        # 'students': students,
        'student_obj': student_obj,
        'center_obj': center_obj,
        'operators': operators,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'students/first_call.html', context)


@login_required
def second_call_view(request, pk):
    try:
        center_obj = Center.objects.get(pk=pk)
        operators = CustomUser.objects.filter(role='operator')
        selected_operator = request.GET.get('operator')
        student_obj = Student.objects.filter(center=center_obj)
        if selected_operator:
            student_obj = student_obj.filter(
                second_call=selected_operator,
                first_call_satus='Так, прийдуть на пробне'
            )
        else:
            student_obj = Student.objects.filter(
                center=center_obj).filter(
                first_call_satus='Так, прийдуть на пробне').order_by('-student_add_date')
    except Center.DoesNotExist:
        raise Http404("Центр не знайдений")

    breadcrumbs = [
        ('Центри', '/centers/'),  # Centers list page
        (center_obj.center_name, f'/centers/{center_obj.id}/students'),  # Current center page
        ('Другий дзвінок', request.path),  # Current page
    ]

    context = {
        'title': 'Другий дзвінок',
        'center_obj': center_obj,
        'student_obj': student_obj,
        'operators': operators,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'students/second_call.html', context)


@login_required
def generate_unique_link(request, pk):
    try:
        center = get_object_or_404(Center, pk=pk)
        if center.unique_link is None:
            center.generate_unique_link()
            messages.success(request, 'Unique link generated successfully')
        else:
            messages.error(request, 'Unique link already exists')
    except:
        messages.error(request, 'Посилання не згенеровано')
    return redirect('admin:centers_center_change', pk)


@login_required
def deactivate_unique_link(request, pk):
    center = get_object_or_404(Center, pk=pk)
    center.unique_link = None
    center.save()
    messages.success(request, 'Unique link deactivated successfully')
    return redirect('admin:centers_center_change', pk)
