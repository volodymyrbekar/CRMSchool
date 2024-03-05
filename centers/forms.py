from django import forms
from .models import Center, Student, GroupTrial, GroupPermanent
from .choices import CHOICES_FIRST_CALL_OPERATOR, CHOICES_FIRST_CALL_STATUS, CHOICES_SECOND_CALL_STATUS, CHOICES_TRIAL_STATUS


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

    class Meta:
        model = Student
        fields = ['student_full_name', 'student_phone_number', 'parent_phone_number', 'school', 'class_number', 'center']

    def __init__(self, *args, **kwargs):
        super(CreateStudentForm, self).__init__(*args, **kwargs)

        self.fields['student_full_name'].widget.attrs['class'] = 'form-control'
        self.fields['student_full_name'].widget.attrs['placeholder'] = 'Повне Ім\'я'

        self.fields['student_phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['student_phone_number'].widget.attrs['placeholder'] = 'Номер Телефону Учня'

        self.fields['parent_phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['parent_phone_number'].widget.attrs['placeholder'] = 'Номер Телефону Батьків'

        self.fields['school'].widget.attrs['class'] = 'form-control'
        self.fields['school'].widget.attrs['placeholder'] = 'Назва Школи'

        self.fields['class_number'].widget.attrs['class'] = 'form-control'
        self.fields['class_number'].widget.attrs['placeholder'] = 'Клас'


    def clean(self):
        optional_fields = ['first_call', 'first_call_status', 'trial_registration', 'comment_first_call',
                           'second_call', 'second_call_status', 'add_to_group', 'comment_second_call']
        data = self.cleaned_data
        for field_name in optional_fields:
            if field_name in data and not data[field_name]:
                data[field_name] = ''
        student_phone_number = data.get('student_full_name')
        qs = Student.objects.filter(student_phone_number__icontains=student_phone_number)
        if qs.exists():
            self.add_error("student_phone_number", f'\"{student_phone_number}\" already in use.')
        return data


class UpdateStudentForm(forms.ModelForm):
    student_full_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}), label="")
    student_phone_number = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}), label="")
    parent_phone_number = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent Phone Number'}), label="")
    school = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School'}), label="")
    class_number = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'max': 11, 'min': 1, 'placeholder': 'Class Number'}), label="")
    center = forms.ModelChoiceField(required=True, queryset=Center.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}), label="")

    first_call = forms.ChoiceField(choices=CHOICES_FIRST_CALL_OPERATOR, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Перший Дзвінок'}), label="")
    first_call_satus = forms.ChoiceField(choices=CHOICES_FIRST_CALL_STATUS, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Статус першого дзвінка'}), label="")
    trial_registration = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Запис на пробне'}), label="")
    trial_status = forms.ChoiceField(choices=CHOICES_TRIAL_STATUS, widget=forms.Select(attrs={'class': 'form-control'}),label="")
    comment_first_call = forms.CharField(required=False, max_length=250, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Коментар'}), label="")

    def __init__(self, *args, **kwargs):
        super(UpdateStudentForm, self).__init__(*args, **kwargs)
        self.fields.pop('center')
        self.fields['trial_registration'] = forms.ModelChoiceField(queryset=GroupTrial.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Реєстрація на пробне'}), label="")
        self.fields['trial_status'].widget.attrs['class'] = 'form-control'
        self.fields['trial_status'].widget.attrs['placeholder'] = 'Статус Пробного'

    class Meta:
        model = Student
        fields = '__all__'


class UpdateStudentSecondForm(forms.ModelForm):
    second_call = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Другий дзвінок'}), label="")
    second_call_satus = forms.ChoiceField(choices=CHOICES_SECOND_CALL_STATUS, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Статус другого дзвінка'}), label="")
    add_to_group = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Додати до групи'}), label="")
    comment_second_call = forms.CharField(required=False, max_length=250, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Коментар'}), label="")

    def __init__(self, *args, **kwargs):
        super(UpdateStudentSecondForm, self).__init__(*args, **kwargs)
        self.fields.pop('center')
        self.fields['add_to_group'] = forms.ModelChoiceField(queryset=GroupPermanent.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Обрати групу'}), label="")

    class Meta:
        model = Student
        fields = '__all__'


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
    group_name = forms.CharField(required=True, max_length=80, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва Групи'}), label="")
    center = forms.ModelChoiceField(queryset=Center.objects.all(), to_field_name='center_name', widget=forms.Select(attrs={'class': 'form-control'}), label="")

    class Meta:
        model = GroupPermanent
        fields = ['group_name', 'center']

    def clean(self):
        data = self.cleaned_data
        group_name = data.get('group_name')
        qs = GroupPermanent.objects.filter(group_name__icontains=group_name)
        if qs.exists():
            self.add_error("group_name", f'\"{group_name}\" already in use.')
        return data