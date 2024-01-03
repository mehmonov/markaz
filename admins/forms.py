from django import forms
from home.models import Course , Group,PREFERRED_DAYS_OF_WEEK_CHOICES,Applicant, Student

class ApplicantForm(forms.ModelForm):
    preferred_days_of_week = forms.MultipleChoiceField(
        choices= PREFERRED_DAYS_OF_WEEK_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Kunlar',
        required=True
    )

    def clean_preferred_days_of_week(self):
        
            preferred_days_of_week = self.cleaned_data.get('preferred_days_of_week')
            if len(preferred_days_of_week) < 3:
                raise forms.ValidationError(
                'Please select at least 3 days of the week.',
                code='invalid',
                params={'field': 'preferred_days_of_week'}
            )
            return preferred_days_of_week

    class Meta:
        model = Applicant
        fields = ['first_name', 'last_name', 'birth_place', 'preferred_time', 'course', 'preferred_days_of_week', 'phone_number', 'phone_number2']

    def clean(self):
        # if last name is not required, then it will be None
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name') 
        if not last_name:
            last_name = ''
        birth_place = self.cleaned_data.get('birth_place')
        preferred_time = self.cleaned_data.get('preferred_time')
        course = self.cleaned_data.get('course')
        preferred_days_of_week = self.cleaned_data.get('preferred_days_of_week')
        phone_number = self.cleaned_data.get('phone_number')
        phone_number2 = self.cleaned_data.get('phone_number2')
        
        if not first_name:
            raise forms.ValidationError(
                'Please enter your first name.',
                code='invalid',
                params={'field': 'first_name'}
            )
        if not preferred_time:
            raise forms.ValidationError(
                'Please enter your preferred time.',
                code='invalid',
                params={'field': 'preferred_time'}
            )
        if not course:
            raise forms.ValidationError(
                'Please enter your course.',
                code='invalid',
                params={'field': 'course'}
            )
        if not preferred_days_of_week:
            raise forms.ValidationError(
                'Please enter your preferred days of week.',
                code='invalid',
                params={'field': 'preferred_days_of_week'}
            )
        if not phone_number:
            raise forms.ValidationError(
                'Please enter your phone number.',
                code='invalid',
                params={'field': 'phone_number'}
            )
        return self.cleaned_data 
            
class GroupForm(forms.ModelForm):
    day_of_week = forms.MultipleChoiceField(
        choices=PREFERRED_DAYS_OF_WEEK_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Kunlar',
        required=True
    )
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.filter(group__isnull=True).order_by('-applicant__registered_time'),
        label='eng oxirgi 5 ta student',
        widget=forms.CheckboxSelectMultiple
    )



    class Meta:
        model = Group
        fields = ['name', 'course', 'price', 'time', 'duration', 'start_date','day_of_week','students','teacher']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'name': forms.TextInput(attrs={'placeholder': 'guruh nomi'}),
            'course': forms.Select(attrs={'placeholder': 'kurs'}),
            'price': forms.NumberInput(attrs={'placeholder': 'guruh narxi'}),
            'start_date': forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'})
        }


class StudentGroupChangeForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['group']

class GroupEditForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['duration', 'teacher', 'name', 'course', 'price', 'students', 'time', 'day_of_week', 'start_date', 'end_date']
        
