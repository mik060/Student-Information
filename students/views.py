from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import StudentForm
from .models import Student

def home(request):
    return render(request, "students/home.html", {
        "student_count": Student.objects.count(),
    })

def student_list(request):
    query = request.GET.get("q", "").strip()
    students = Student.objects.all()
    if query:
        students = students.filter(
            first_name__icontains=query
        ) | students.filter(
            last_name__icontains=query
        ) | students.filter(
            student_number__icontains=query
        ) | students.filter(
            course__icontains=query
        )
    return render(request, "students/student_list.html", {
        "students": students.distinct(),
        "query": query,
    })

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully.")
            return redirect("student_list")
    else:
        form = StudentForm()
    return render(request, "students/student_form.html", {"form": form})

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student record deleted.")
    return redirect("student_list")
