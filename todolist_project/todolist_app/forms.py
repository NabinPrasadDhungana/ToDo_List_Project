from django import forms
from .models import ToDoList, ToDoItem

# To-do item update form
class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        exclude = ['created_date']
        widgets = {
            'todo_list': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
# To-do item creation form
class ItemCreateForm(ItemUpdateForm):
    class Meta(ItemUpdateForm.Meta):
        exclude = ItemUpdateForm.Meta.exclude + ['completed']
