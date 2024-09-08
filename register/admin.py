from django.contrib import admin
from .models import User, Doctor, Student, Admin
# Register your models here.

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Student)
admin.site.register(Admin)