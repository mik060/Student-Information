from django.test import TestCase
from django.urls import reverse
from .models import Student

class StudentWebsiteTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student Information System")

    def test_add_student_page_loads(self):
        response = self.client.get(reverse("add_student"))
        self.assertEqual(response.status_code, 200)

    def test_student_can_be_added(self):
        response = self.client.post(reverse("add_student"), {
            "student_number": "2026-0001",
            "first_name": "Jamie",
            "last_name": "Santos",
            "course": "BS Information Technology",
            "year_level": 3,
            "email": "jamie@example.com",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Student.objects.count(), 1)
