from django.contrib import admin
from .models import Employee


# Register your models here.

# class LineAdmin(admin.ModelAdmin):
#     list_display = ("id", "user_id")


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ( "employee_id",)


admin.site.register(Employee, EmployeeAdmin)
# admin.site.register(Line, LineAdmin)