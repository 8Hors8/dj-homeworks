from django.core.exceptions import ValidationError
from django.db import models

from django_testing import settings


class Student(models.Model):

    name = models.TextField()

    birth_date = models.DateField(
        null=True,
    )


class Course(models.Model):

    name = models.TextField()

    students = models.ManyToManyField(
        Student,
        blank=True,
    )

    def clean(self):
        if self.students.count() > 20:
            raise ValidationError(f"Cannot have more than {settings.MAX_STUDENTS_PER_COURSE} students in a course.")
