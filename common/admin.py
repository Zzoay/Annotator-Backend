from django.contrib import admin

from common.models import User, Task, Process

# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Process)