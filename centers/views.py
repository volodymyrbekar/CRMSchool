from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required


from .forms import CreateCenterForm, CreateStudentForm, CreateGroupTrialForm, CreateGroupForm, UpdateStudentForm, UpdateStudentSecondForm
from .models import Center, Student, GroupTrial, Group


def centers_list_view(request):
    centers_obj = Center.objects.all()
    context = {
        'centers': centers_obj,
    }
    return render(request, 'centers/centers_list.html', context)  # This is the file that will be rendered


@login_required
def create_center_view(request):
    form = CreateCenterForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            create_center = form.save()
            context['form'] = CreateCenterForm()
            messages.success(request, 'Center created successfully')
            return redirect('centers_list')
    return render(request, 'centers/create_center.html', context)


def center_search_view(request):
    query = request.GET.get('q')
    qs = Center.objects.search(query=query)
    context = {
        'object': qs
    }
    return render(request, 'search/search_result.html', context=context)


def student_list_view(request, pk):
    try:
        center_obj = Center.objects.get(pk=pk)
    except Center.DoesNotExist:
        raise Http404("Center does not exist")
    student_obj = Student.objects.filter(center_id=pk).all()
    group_trial_obj = GroupTrial.objects.filter(center_id=pk).all()
    group_obj = Group.objects.filter(center_id=pk).all()
    context = {
        'student_obj': student_obj,
        'center_obj': center_obj,
        'group_trial_obj': group_trial_obj,
        'group_obj': group_obj,

    }

    return render(request, 'students/students_list.html', context)


@login_required
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
def first_call_student_update_view(request, pk):
    try:
        student = get_object_or_404(Student, id=pk)
        form = UpdateStudentForm(instance=student)
        context = {
            'form': form,
            'student_obj': student,
        }
        if request.method == 'POST':
            form = UpdateStudentForm(request.POST or None, instance=student)
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


def group_detail_trial_view(request, pk):
    try:
        group_trial_obj = GroupTrial.objects.get(pk=pk)
    except GroupTrial.DoesNotExist:
        raise Http404("Group does not exist")
    student_obj = Student.objects.filter(center_id=pk).all()
    context = {
        'group_trial_obj': group_trial_obj,
        'student_obj': student_obj,
    }
    return render(request, 'groups/group_detail_trial.html', context)


@login_required
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


def group_detail_view(request, pk):
    try:
        group_obj = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        raise Http404("Group does not exist")
    context = {
        'group_obj': group_obj,
    }
    return render(request, 'groups/group_detail_permanent.html', context)


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


def second_call_view(request, pk):
    try:
        center_obj = Center.objects.get(pk=pk)
        student_obj = Student.objects.filter(center_id=pk).all()
    except Center.DoesNotExist:
        raise Http404("Student does not exist")
    context = {
        'center_obj': center_obj,
        'student_obj': student_obj,
    }
    return render(request, 'students/second_call.html', context)