from django.contrib import admin

from course_api.tasks.models import Board, Status, Task

admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Board)
