from django.db import models

from course_api.utils.models.base import BaseModel
from course_api.users.models import User
from django.db.models import JSONField

class Board(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User , on_delete=models.CASCADE , null=True,blank=True)
    # Meta Field used to store additional data
    meta = JSONField(null=True, blank=True, verbose_name="Meta", help_text="Additional data for the board")

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
    
    def __str__(self):
        return self.title
class Status(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User , on_delete=models.CASCADE , null=True,blank=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True, related_name="stages")
    is_complete_status = models.BooleanField(default=False)
    order = JSONField(null=True, blank=True, verbose_name="Tasks Order", help_text="task order data")

    def __str__(self):
        return self.title

class Task(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    board = models.ForeignKey(Board , on_delete=models.CASCADE , null=True,blank=True)
    status = models.ForeignKey(Status , on_delete=models.CASCADE , null=True,blank=True, related_name="tasks")

    def __str__(self):
        return self.title