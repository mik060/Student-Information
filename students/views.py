from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from config.settings import db

from .forms import StudentForm
from .models import Student


def _firestore_students():
    if db is None:
        return None

    try:
        return [
            {**doc.to_dict(), "id": doc.id}
            for doc in db.collection("students").stream()
        ]
    except Exception:
        return None


def _matches_query(student, query):
    if not query:
        return True

    searchable = " ".join(
        [
            str(student.get("student_number", "")),
            str(student.get("first_name", "")),
            str(student.get("last_name", "")),
            str(student.get("course", "")),
        ]
    ).lower()
    return query in searchable


def home(request):
    firestore_students = _firestore_students()
    student_count = len(firestore_students) if firestore_students is not None else Student.objects.count()
    return render(request, "students/home.html", {"student_count": student_count})


def student_list(request):
    query = request.GET.get("q", "").strip().lower()

    firestore_students = _firestore_students()
    if firestore_students is not None:
        filtered_students = [student for student in firestore_students if _matches_query(student, query)]
        return render(request, "students/student_list.html", {"students": filtered_students, "query": query})

    students = Student.objects.all()
    if query:
        students = (
            students.filter(first_name__icontains=query)
            | students.filter(last_name__icontains=query)
            | students.filter(student_number__icontains=query)
            | students.filter(course__icontains=query)
        )
    return render(request, "students/student_list.html", {"students": students.distinct(), "query": query})


def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()

            if db is not None:
                try:
                    student_id = str(student.student_number).strip()
                    db.collection("students").document(student_id).set(
                        {
                            "student_number": student.student_number,
                            "first_name": student.first_name,
                            "last_name": student.last_name,
                            "course": student.course,
                            "year_level": student.year_level,
                            "email": student.email,
                        }
                    )
                except Exception:
                    messages.error(request, "Student was saved locally but Firestore sync failed.")
                    return redirect("student_list")

            messages.success(request, "Student added successfully.")
            return redirect("student_list")
    else:
        form = StudentForm()
    return render(request, "students/student_form.html", {"form": form})


def delete_student(request, student_id):
    if request.method == "POST":
        if db is not None:
            try:
                firestore_doc = db.collection("students").document(str(student_id))
                if firestore_doc.get().exists:
                    firestore_doc.delete()
            except Exception:
                pass

        try:
            student = get_object_or_404(Student, id=int(student_id))
            student.delete()
        except (TypeError, ValueError):
            try:
                student = get_object_or_404(Student, student_number=str(student_id))
                student.delete()
            except Exception:
                pass

        messages.success(request, "Student record deleted.")
    return redirect("student_list")
