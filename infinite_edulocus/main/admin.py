from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Email_Body)
admin.site.register(EmailLog)


