from django import forms
import logging
from django.contrib.auth import get_user_model
from .models import Center, Student, GroupTrial, GroupPermanent
from .choices import CHOICES_FIRST_CALL_STATUS, CHOICES_SECOND_CALL_STATUS, CHOICES_TRIAL_STATUS

logger = logging.getLogger(__name__)


class CreateCenterForm(forms.ModelForm):
    center_name = forms.CharField(required=True, max_length=80, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва центру'}), label="")
    location = forms.CharField(required=True, max_length=80, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Локація'}), label="")

    class Meta:
        model = Center
        fields = ['center_name', 'location']

    def clean(self):
        data = self.cleaned_data
        center_name = data.get('center_name')
        qs = Center.objects.filter(center_name__icontains=center_name)
        if qs.exists():
            self.add_error("center_name", f'\"{center_name}\" already in use.')
        return data


class CreateStudentForm(forms.ModelForm):
    student_full_name = forms.CharField(required=True, max_length=50, widget=forms.TextInput())
    student_phone_number = forms.CharField(required=False, max_length=50, widget=forms.TextInput())
    parent_phone_number = forms.CharField(required=True, max_length=50, widget=forms.TextInput())
    parent_full_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput())
    school = forms.CharField(required=True, max_length=50, widget=forms.TextInput())
    class_number = forms.IntegerField(required=True, widget=forms.NumberInput())
    center = forms.ModelChoiceField(
        required=True,
        queryset=Center.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    class Meta:
        model = Student
        fields = ['student_full_name', 'student_phone_number', 'parent_phone_number',  'parent_full_name', 'school', 'class_number', 'center']

    def __init__(self, *args, **kwargs):
        super(CreateStudentForm, self).__init__(*args, **kwargs)

        self.fields['student_full_name'].widget.attrs['class'] = 'form-control'
        self.fields['student_full_name'].widget.attrs['placeholder'] = 'Повне Ім\'я'

        self.fields['student_phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['student_phone_number'].widget.attrs['placeholder'] = 'Номер Телефону Учня'

        self.fields['parent_phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['parent_phone_number'].widget.attrs['placeholder'] = 'Номер Телефону Батьків'

        self.fields['parent_full_name'].widget.attrs['class'] = 'form-control'
        self.fields['parent_full_name'].widget.attrs['placeholder'] = 'ПІБ Батьків'

        self.fields['school'].widget.attrs['class'] = 'form-control'
        self.fields['school'].widget.attrs['placeholder'] = 'Назва Школи'

        self.fields['class_number'].widget.attrs['class'] = 'form-control'
        self.fields['class_number'].widget.attrs['placeholder'] = 'Клас'

    # def clean(self):
    #     optional_fields = ['first_call', 'first_call_status', 'trial_registration', 'comment_first_call',
    #                        'second_call', 'second_call_status', 'add_to_group', 'comment_second_call']
    #     data = self.cleaned_data
    #     for field_name in optional_fields:
    #         if field_name in data and not data[field_name]:
    #             data[field_name] = ''
    #     student_phone_number = data.get('student_full_name')
    #     qs = Student.objects.filter(student_phone_number__icontains=student_phone_number)
    #     if qs.exists():
    #         self.add_error("student_phone_number", f'\"{student_phone_number}\" already in use.')
    #     return data


class UpdateStudentFirstForm(forms.ModelForm):
    student_full_name = forms.CharField(
        required=False, max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
        label=""
    )
    student_phone_number = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        label=""
    )
    parent_phone_number = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent Phone Number'}),
        label=""
    )
    parent_full_name = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent Full Name'}),
        label=""
    )
    school = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School'}),
        label=""
    )
    class_number = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'max': 11, 'min': 1, 'placeholder': 'Class Number'}),
        label=""
    )
    center = forms.ModelChoiceField(
        required=True,
        queryset=Center.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        label=""
    )

    first_call = forms.ChoiceField(choices=[], required=True, widget=forms.Select())
    first_call_status = forms.ChoiceField(
        required=True,
        choices=CHOICES_FIRST_CALL_STATUS,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Статус першого дзвінка'}),
        label=""
    )
    trial_registration = forms.ModelChoiceField(
        queryset=GroupTrial.objects.none(),
        empty_label='---',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Реєстрація на пробне'})
    )
    trial_status = forms.ChoiceField(
        required=False,
        choices=CHOICES_TRIAL_STATUS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=""
    )
    comment_first_call = forms.CharField(
        required=False,
        max_length=250,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Коментар'}),
        label=""
    )

    def __init__(self, *args, **kwargs):
        center_instance = kwargs.pop('center_instance', None)
        super(UpdateStudentFirstForm, self).__init__(*args, **kwargs)
        self.fields.pop('center')

        if center_instance:
            self.fields['trial_registration'].queryset = GroupTrial.objects.filter(center=center_instance)

        if self.instance and self.instance.pk:
            self.fields['trial_registration'].initial = self.instance.trial_registration

        User = get_user_model()
        all_users = User.objects.all()
        self.fields['first_call'].choices = [(user.username, user.username) for user in all_users]

    def save(self, commit=True):
        instance = super(UpdateStudentFirstForm, self).save(commit=False)
        instance.first_call = self.cleaned_data.get('first_call')
        instance.parent_phone_number = self.cleaned_data.get('parent_phone_number')
        instance.parent_full_name = self.cleaned_data.get('parent_full_name')
        instance.trial_registration = self.cleaned_data.get('trial_registration')
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Student
        fields = ['student_full_name', 'student_phone_number', 'parent_phone_number', 'parent_full_name', 'school',
                  'class_number', 'center', 'first_call', 'first_call_status', 'trial_registration', 'trial_status', 'comment_first_call']


class UpdateStudentSecondForm(forms.ModelForm):
    second_call = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Другий дзвінок'})
    )
    second_call_status = forms.ChoiceField(
        required=False,
        choices=CHOICES_SECOND_CALL_STATUS,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Статус другого дзвінка'})
    )
    add_to_group = forms.ModelChoiceField(
        queryset=GroupPermanent.objects.none(),
        empty_label='---',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Обрати групу'}),
        label="Запис на пробне"
    )
    comment_second_call = forms.CharField(
        required=False,
        max_length=250,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Коментар'})
    )

    def __init__(self, *args, **kwargs):
        center_instance = kwargs.pop('center_instance', None)
        user_instance = kwargs.pop('user_instance', None)
        super(UpdateStudentSecondForm, self).__init__(*args, **kwargs)
        self.fields.pop('center')
        self.fields['add_to_group'].required = False
        if center_instance:
            self.fields['add_to_group'].queryset = GroupPermanent.objects.filter(center=center_instance)

        User = get_user_model()
        all_users = User.objects.all()
        self.fields['second_call'].choices = [(user.username, user.username) for user in all_users]

        if self.instance and self.instance.pk:
            self.fields['second_call'].initial = self.instance.second_call
        else:
            self.fields['second_call'].initial = user_instance.username

    def clean(self):
        data = super().clean()
        if self.errors:
            logger.error(f"Form validation errors: {self.errors}")
        return data

    def save(self, commit=True):
        instance = super(UpdateStudentSecondForm, self).save(commit=False)
        instance.second_call = self.cleaned_data.get('second_call')
        instance.second_call_status = self.cleaned_data.get('second_call_status')
        instance.add_to_group = self.cleaned_data.get('add_to_group')
        instance.comment_second_call = self.cleaned_data.get('comment_second_call')

        if commit:
            instance.save()
        return instance

    class Meta:
        model = Student
        fields = ['second_call', 'second_call_status', 'add_to_group', 'comment_second_call', 'center']


class CreateGroupTrialForm(forms.ModelForm):
    group_name = forms.CharField(required=True, max_length=80, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва Групи'}), label="")
    center = forms.ModelChoiceField(queryset=Center.objects.all(), to_field_name='center_name', widget=forms.Select(attrs={'class': 'form-control'}), label="")

    class Meta:
        model = GroupTrial
        fields = ['group_name', 'center']

    # def clean(self):
    #     data = self.cleaned_data
    #     group_name = data.get('group_name')
    #     qs = GroupTrial.objects.filter(group_name__icontains=group_name)
    #     if qs.exists():
    #         self.add_error("group_name", f'\"{group_name}\" already in use.')
    #     return data


class CreateGroupForm(forms.ModelForm):
    group_name = forms.CharField(required=True, max_length=80, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва Групи'}), label="")
    center = forms.ModelChoiceField(queryset=Center.objects.all(), to_field_name='center_name', widget=forms.Select(attrs={'class': 'form-control'}), label="")

    class Meta:
        model = GroupPermanent
        fields = ['group_name', 'center']

    # def clean(self):
    #     data = self.cleaned_data
    #     group_name = data.get('group_name')
    #     qs = GroupPermanent.objects.filter(group_name__icontains=group_name)
    #     if qs.exists():
    #         self.add_error("group_name", f'\"{group_name}\" already in use.')
    #     return data