from django import forms
from .models import Student

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        # Don't include admission_date because it is auto generated
        exclude = ['admission_date']

        widgets = {

            'roll_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Roll Number'
            }),

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),

            'department': forms.Select(attrs={
                'class': 'form-select'
            }),

            'semester': forms.Select(attrs={
                'class': 'form-select'
            }),

            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter Address'
            }),

            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'blood_group': forms.Select(attrs={
            'class':'form-select'
            }),

            'emergency_contact': forms.TextInput(attrs={
            'class':'form-control'
            }),

            'student_signature': forms.ClearableFileInput(attrs={
            'class':'form-control'
            }),
        }

        labels = {
            'roll_number': 'Roll Number',
            'date_of_birth': 'Date of Birth',
        }
