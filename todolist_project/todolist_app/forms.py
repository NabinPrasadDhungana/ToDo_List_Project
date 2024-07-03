from django import forms
from .models import ToDoList, ToDoItem
from .models import *
from allauth.account.forms import SignupForm, LoginForm

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    middle_name = forms.CharField(max_length=30, required=False, label='Middle Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'middle_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.middle_name = self.cleaned_data.get('middle_name', '')
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
    
# class CustomLoginForm(LoginForm):


# To-do item update form
class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        exclude = ['created_date']
        widgets = {
            'todo_list': forms.Select(attrs={'class': 'form-control w-75'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
# To-do item creation form
class ItemCreateForm(ItemUpdateForm):
    class Meta(ItemUpdateForm.Meta):
        exclude = ItemUpdateForm.Meta.exclude + ['completed']

class ToDoListCreateForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ToDoListUpdateForm(ToDoListCreateForm):
    pass