from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required

from .forms import CreateCenterForm, CreateStudentForm, CreateGroupTrialForm, CreateGroupForm, UpdateStudentFirstForm, UpdateStudentSecondForm
from .models import Center, Student, GroupTrial, GroupPermanent
from users.models import CustomUser


@login_required
def centers_list_view(request):
    centers_obj = Center.objects.all()
    context = {
        'centers': centers_obj,
    }
    return render(request, 'centers/centers_list.html', context)  # This is the file that will be rendered


@login_required
@permission_required('users.can_add_centers', raise_exception=True)
def create_center_view(request):
    # if not request.user.has_perm('users.centers'):
    #     raise PermissionDenied("You do not have permission to create a center")
    form = CreateCenterForm(request.POST or None)
    context = {'form': form}
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
    student_obj = Student.objects.filter(center_id=pk).all()
    group_trial_obj = GroupTrial.objects.filter(center_id=pk).all()
    group_obj = GroupPermanent.objects.filter(center_id=pk).all()
    context = {
        'student_obj': student_obj,
        'center_obj': center_obj,
        'group_trial_obj': group_trial_obj,
        'group_obj': group_obj,

    }
    return render(request, 'students/students_list.html', context)


@login_required
@permission_required('users.can_add_students', raise_exception=True)
def create_student_view(request, pk):
    center = Center.objects.get(pk=pk)
    form = CreateStudentForm(request.POST or None, initial={'center': pk})
    context = {
        'form': form,
        'center': center,
        'pk': pk,
    }
    if request.method == 'POST':
        if form.is_valid():
            create_student = form.save()
            context['form'] = CreateStudentForm(initial={'center': pk})
            messages.success(request, 'Учень створений успішно')
            # return redirect('students_list')
    return render(request, 'students/create_student.html', context)


@login_required
@permission_required('users.can_edit_first_call', raise_exception=True)
def first_call_student_update_view(request, pk):
    try:
        student = get_object_or_404(Student, id=pk)
        form = UpdateStudentFirstForm(instance=student)
        context = {
            'form': form,
            'student_obj': student,
        }
        if request.method == 'POST':
            form = UpdateStudentFirstForm(request.POST or None, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'Учень успішно оновлений')
                return redirect('first_call', pk=student.center.pk)
            else:
                # print(form.errors)
                messages.error(request, 'Помилка валідації форми. Будь ласка, перевірте дані')
        return render(request, 'students/first_call_student_update.html', context)
    except Student.DoesNotExist:
        messages.error(request, "Студент із зазначеним id не знайдений")
        return redirect('centers_list')


@login_required
@permission_required('users.can_edit_second_call', raise_exception=True)
def second_call_student_update_view(request, pk):
    try:
        student = get_object_or_404(Student, id=pk)
        form = UpdateStudentSecondForm(instance=student)
        context = {
            'form': form,
            'student_obj': student,
        }
        if request.method == 'POST':
            form = UpdateStudentSecondForm(request.POST or None, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'Учень успішно оновлений')
                return redirect('second_call', pk=student.center.pk)
            else:
                # print(form.errors)
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
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            create_group_trial = form.save()
            context['form'] = CreateGroupTrialForm()
            messages.success(request, 'Група на пробне успішно створена')
            return redirect('centers_list')
    return render(request, 'groups/create_group_trial.html', context)


@login_required
def group_detail_trial_view(request, pk):
    try:
        group_trial_obj = GroupTrial.objects.get(pk=pk)
        center = group_trial_obj.center
    except GroupTrial.DoesNotExist:
        raise Http404("Group does not exist")
    student_obj = Student.objects.filter(center=center, trial_registration=group_trial_obj)
    context = {
        'group_trial_obj': group_trial_obj,
        'student_obj': student_obj,
    }
    return render(request, 'groups/group_detail_trial.html', context)


@login_required
@permission_required('users.can_add_grouppermanent', raise_exception=True)
def create_group(request):

    form = CreateGroupForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            create_group = form.save()
            context['form'] = CreateGroupForm()
            messages.success(request, 'Група успішно створена')
            return redirect('centers_list')
    return render(request, 'groups/create_group_permanent.html', context)


@login_required
def group_detail_view(request, pk):
    try:
        group_obj = GroupPermanent.objects.get(pk=pk)
        center = group_obj.center
    except GroupPermanent.DoesNotExist:
        raise Http404("Group does not exist")
    student_obj = Student.objects.filter(center=center, add_to_group=group_obj)
    context = {
        'group_obj': group_obj,
        'student_obj': student_obj,
    }
    return render(request, 'groups/group_detail_permanent.html', context)


@login_required
def first_call_view(request, pk):
    try:
        center_obj = Center.objects.get(pk=pk)
        student_obj = Student.objects.filter(center_id=pk).all()
    except Center.DoesNotExist:
        raise Http404("Student does not exist")
    context = {
        'center_obj': center_obj,
        'student_obj': student_obj,
    }
    return render(request, 'students/first_call.html', context)


@login_required
def second_call_view(request, pk):
    try:
        center_obj = Center.objects.get(pk=pk)
        student_obj = Student.objects.filter(center_id=pk, first_call_satus='Так, прийдуть на пробне').all()
    except Center.DoesNotExist:
        raise Http404("Student does not exist")
    context = {
        'center_obj': center_obj,
        'student_obj': student_obj,
    }
    return render(request, 'students/second_call.html', context)