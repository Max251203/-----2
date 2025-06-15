from django.contrib import admin
from .models import (
    Position,
    Department,
    Client,
    Employee,
    Service,
    Order,
    PaymentOrder,
    Profile,
)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "salary")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "head", "employee_count")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person", "phone", "email")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "position",
                    "department", "birth_date")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "unit", "material")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("client", "service", "employee",
                    "date_received", "date_executed", "quantity", "discount")


@admin.register(PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "date_paid")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "linked_client", "linked_employee")
    list_filter = ("role",)
