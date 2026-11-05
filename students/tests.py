from django.test import TestCase
from django.urls import reverse


class StudentWebsiteTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student Information System")

    def test_add_student_page_loads(self):
        response = self.client.get(reverse("add_student"))
        self.assertEqual(response.status_code, 200)

    def test_student_list_page_loads(self):
        response = self.client.get(reverse("student_list"))
        self.assertEqual(response.status_code, 200)