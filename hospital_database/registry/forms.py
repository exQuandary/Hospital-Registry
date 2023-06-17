from .models import Patient
from django import forms
from .models import Patient, Visit


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['reason', 'patient', 'nurse', 'provider', 'status']


class PatientEditForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['last_name', 'first_name', 'dob',
                  'address', 'city', 'state', 'phone', 'insurance']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
