from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_number",
            "first_name",
            "last_name",
            "course",
            "year_level",
            "email",
        ]
        widgets = {
            "student_number": forms.TextInput(attrs={"placeholder": "e.g. 2026-0001"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "course": forms.TextInput(attrs={"placeholder": "e.g. BS Information Technology"}),
            "year_level": forms.NumberInput(attrs={"min": 1, "max": 6, "placeholder": "1"}),
            "email": forms.EmailInput(attrs={"placeholder": "student@example.com"}),
        }
