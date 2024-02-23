from django import forms
from .models import Center, Student, GroupTrial, Group


class CreateCenterForm(forms.ModelForm):
    center_name = forms.CharField(required=True, max_length=80, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Center Name'}), label="")
    location = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}), label="")

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
    student_full_name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}), label="")
    student_phone_number = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}), label="")
    parent_phone_number = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent Phone Number'}), label="")
    school = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School'}), label="")
    class_number = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'max': 11, 'min': 1, 'placeholder': 'Class Number'}), label="")
    center = forms.ModelChoiceField(required=True, queryset=Center.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}), label="")

    first_call = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Call'}), label="")
    first_call_satus = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Call Status'}), label="")
    trial_registration = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Trial Registration'}), label="")
    trial_status = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label="Статус Пробного")
    comment_first_call = forms.CharField(required=False, max_length=250, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comment First Call'}), label="")

    second_call = forms.CharField(required=False,  max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Second Call'}), label="")
    second_call_satus = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Second Call Status'}), label="")
    add_to_group = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add To Group'}), label="")
    comment_second_call = forms.CharField(required=False, max_length=250, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comment Second Call'}), label="")

    class Meta:
        model = Student
        fields = ['student_full_name', 'student_phone_number', 'parent_phone_number', 'school', 'class_number', 'center']


    def __init__(self, *args, **kwargs):
        super(CreateStudentForm, self).__init__(*args, **kwargs)

        self.fields['student_full_name'].widget.attrs['class'] = 'form-control'
        self.fields['student_full_name'].widget.attrs['placeholder'] = 'Повне Ім\'я'
        self.fields['student_full_name'].label = ''

        self.fields['student_phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['student_phone_number'].widget.attrs['placeholder'] = 'Номер Телефону Учня'

        self.fields['parent_phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['parent_phone_number'].widget.attrs['placeholder'] = 'Номер Телефону Батьків'

        self.fields['school'].widget.attrs['class'] = 'form-control'
        self.fields['school'].widget.attrs['placeholder'] = 'Назва Школи'

        self.fields['class_number'].widget.attrs['class'] = 'form-control'
        self.fields['class_number'].widget.attrs['placeholder'] = 'Клас'



        self.fields['first_call'].widget.attrs['class'] = 'form-control'
        self.fields['first_call'].widget.attrs['placeholder'] = 'Перший Дзвінок'

        self.fields['first_call_satus'].widget.attrs['class'] = 'form-control'
        self.fields['first_call_satus'].widget.attrs['placeholder'] = 'Статус першого дзвінка'

        self.fields['trial_registration'].widget.attrs['class'] = 'form-control'
        self.fields['trial_registration'].widget.attrs['placeholder'] = 'Реєстрація на пробне'

        self.fields['trial_status'].widget.attrs['class'] = 'form-control'
        self.fields['trial_status'].widget.attrs['placeholder'] = 'Cтатус Пробного'



        self.fields['second_call'].widget.attrs['class'] = 'form-control'
        self.fields['second_call'].widget.attrs['placeholder'] = 'Другий Дзвінок'

        self.fields['second_call_satus'].widget.attrs['class'] = 'form-control'
        self.fields['second_call_satus'].widget.attrs['placeholder'] = 'Статус другого дзвінка'

        self.fields['add_to_group'].widget.attrs['class'] = 'form-control'
        self.fields['add_to_group'].widget.attrs['placeholder'] = 'Додати до групи'

        self.fields['comment_second_call'].widget.attrs['class'] = 'form-control'
        self.fields['comment_second_call'].widget.attrs['placeholder'] = 'Коментар до другого дзвінка'



    def clean(self):
        optional_fields = ['first_call', 'first_call_status', 'trial_registration', 'comment_first_call',
                           'second_call', 'second_call_status', 'add_to_group', 'comment_second_call']
        data = self.cleaned_data
        for field_name in optional_fields:
            if field_name in data and not data[field_name]:
                data[field_name] = ''
        student_full_name = data.get('student_full_name')
        qs = Student.objects.filter(student_full_name__icontains=student_full_name)
        if qs.exists():
            self.add_error("student_full_name", f'\"{student_full_name}\" already in use.')
        return data


class CreateGroupTrialForm(forms.ModelForm):
    group_name = forms.CharField(required=True, max_length=80, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Group Name'}), label="")
    center = forms.ModelChoiceField(queryset=Center.objects.all(), to_field_name='center_name', widget=forms.Select(attrs={'class': 'form-control'}), label="")

    class Meta:
        model = GroupTrial
        fields = ['group_name', 'center']

    def clean(self):
        data = self.cleaned_data
        group_name = data.get('group_name')
        qs = GroupTrial.objects.filter(group_name__icontains=group_name)
        if qs.exists():
            self.add_error("group_name", f'\"{group_name}\" already in use.')
        return data


class CreateGroupForm(forms.ModelForm):
    group_name = forms.CharField(required=True, max_length=80, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Group Name'}), label="")
    center = forms.ModelChoiceField(queryset=Center.objects.all(), to_field_name='center_name', widget=forms.Select(attrs={'class': 'form-control'}), label="")

    class Meta:
        model = Group
        fields = ['group_name', 'center']

    def clean(self):
        data = self.cleaned_data
        group_name = data.get('group_name')
        qs = Group.objects.filter(group_name__icontains=group_name)
        if qs.exists():
            self.add_error("group_name", f'\"{group_name}\" already in use.')
        return data