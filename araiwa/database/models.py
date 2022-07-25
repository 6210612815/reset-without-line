from pyexpat import model
from django.forms import ModelForm
from django.db import models

# Create your models here.

# class Line(models.Model):
#     user_id = models.CharField(max_length=100)

#     def __str__(self):
#         return self.user_id


class Employee(models.Model):
    # line_id = models.OneToOneField(Line, on_delete=models.CASCADE, primary_key=True)
    employee_id = models.CharField(max_length=10)
    name = models.CharField(max_length=50, default=None)
    title = models.CharField(max_length=50, default=None)

    def __str__(self):
        return f"{self.title} {self.name} ID:{self.employee_id}"


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id']
        labels = {
            'employee_id': 'employee_id',
        }