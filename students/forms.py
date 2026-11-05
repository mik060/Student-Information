from django import forms


class StudentForm(forms.Form):
    student_number = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "e.g. 2026-0001"}),
    )
    first_name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(attrs={"placeholder": "First name"}),
    )
    last_name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(attrs={"placeholder": "Last name"}),
    )
    course = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "e.g. BS Information Technology"}),
    )
    year_level = forms.IntegerField(
        min_value=1,
        max_value=6,
        widget=forms.NumberInput(attrs={"min": 1, "max": 6, "placeholder": "1"}),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "student@example.com"}),
    )

    def clean_student_number(self):
        student_number = self.cleaned_data["student_number"].strip()
        if not student_number:
            raise forms.ValidationError("Student number is required.")
        return student_number