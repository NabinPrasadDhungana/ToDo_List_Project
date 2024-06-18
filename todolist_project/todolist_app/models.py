from django.db import models

from django.utils import timezone
from datetime import datetime, timedelta
from django.urls import reverse
# Create your models here.

def one_week_hence():
        return datetime.now() + timedelta(weeks=1)

class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])
    
    def __str__(self):
        return self.title

class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_week_hence)
    completed = models.BooleanField(default=False)
    todo_list = models.ForeignKey('ToDoList', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("item-update", args=[str(self.todo_list.id), str(self.pk)])
    
    def __str__(self):
        return self.title
    