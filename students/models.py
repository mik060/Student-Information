from django.db import models

class Student(models.Model):
    student_number = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    course = models.CharField(max_length=100)
    year_level = models.PositiveSmallIntegerField()
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.student_number} - {self.first_name} {self.last_name}"
