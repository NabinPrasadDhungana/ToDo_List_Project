from django import forms
from .models import ToDoList, ToDoItem

# To-do item update form
class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['__all__']
