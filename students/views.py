from django.contrib import messages
from django.shortcuts import redirect, render

from config.settings import db

from .forms import StudentForm


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
    student_count = len(firestore_students) if firestore_students is not None else 0
    return render(request, "students/home.html", {"student_count": student_count})


def student_list(request):
    query = request.GET.get("q", "").strip().lower()

    firestore_students = _firestore_students()
    if firestore_students is not None:
        filtered_students = [
            student for student in firestore_students if _matches_query(student, query)
        ]
        return render(
            request,
            "students/student_list.html",
            {"students": filtered_students, "query": query},
        )

    return render(
        request,
        "students/student_list.html",
        {"students": [], "query": query, "firestore_unavailable": True},
    )


def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            if db is not None:
                try:
                    student_data = {
                        "student_number": form.cleaned_data["student_number"].strip(),
                        "first_name": form.cleaned_data["first_name"].strip(),
                        "last_name": form.cleaned_data["last_name"].strip(),
                        "course": form.cleaned_data["course"].strip(),
                        "year_level": form.cleaned_data["year_level"],
                        "email": form.cleaned_data["email"].strip()
                        if form.cleaned_data["email"]
                        else "",
                    }
                    student_id = student_data["student_number"]
                    db.collection("students").document(student_id).set(student_data)
                    messages.success(request, "Student added successfully.")
                    return redirect("student_list")
                except Exception as e:
                    messages.error(request, f"Failed to save student: {e}")
            else:
                messages.error(request, "Firestore is not available.")
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
                    messages.success(request, "Student record deleted.")
                else:
                    messages.error(request, "Student not found.")
            except Exception as e:
                messages.error(request, f"Failed to delete student: {e}")
        else:
            messages.error(request, "Firestore is not available.")
    return redirect("student_list")