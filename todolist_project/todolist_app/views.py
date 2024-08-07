from typing import Any
from django.urls import reverse_lazy
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from allauth.account.views import SignupView, LoginView
# Create your views here.
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailAddress
from django.shortcuts import redirect
from django.http import HttpResponse

class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        # Log the execution
        print("CustomConfirmEmailView get method called")
        # Call the parent get method
        response = super().get(*args, **kwargs)
        return response
    
    def post(self, *args, **kwargs):
        # Log the execution
        print("CustomConfirmEmailView post method called")
        # Call the parent post method
        response = super().post(*args, **kwargs)
        return response


class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'account/signup.html'

    def get_success_url(self):
        return reverse('account_login')

class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        # Custom logic after form is valid
        return response



class Home(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        user = self.request.user

        if query:
            # Filter `ToDoList` and `ToDoItem` based on the search query and current user
            todo_lists = ToDoList.objects.filter(user=user, title__icontains=query)
            todo_items = ToDoItem.objects.filter(todo_list__user=user, title__icontains=query)
        else:
            todo_lists = ToDoList.objects.filter(user=user)
            todo_items = ToDoItem.objects.filter(todo_list__user=user)

        # Group `ToDoItem` objects by their associated `ToDoList`
        todo_list_items = {}
        for todo_list in todo_lists:
            todo_list_items[todo_list] = todo_list.todoitem_set.filter(todo_list__user=user)

        context['todo_lists'] = todo_list_items
        context['query'] = query
        context['todo_items'] = todo_items
        return context



    
class ItemDetailView(LoginRequiredMixin, DetailView):
    model = ToDoItem
    context_object_name = 'todo_item'
    template_name = 'todolist_app/item_detail.html'
    login_url = 'account_login'

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list__user=self.request.user)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDoItem
    form_class = ItemUpdateForm
    template_name = 'item_update.html'
    context_object_name = 'todo_item'
    template_name = 'todolist_app/item_update.html'
    login_url = 'account_login'

    def get_success_url(self):
        todo_list_id = self.object.todo_list.id
        item_id = self.object.id
        return reverse('item_detail', kwargs={'id': todo_list_id, 'pk': item_id})
    
    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list__user=self.request.user)
    
    # def post(self, request, *args, **kwargs):
    #     if "cancel" in request.POST:
    #         return redirect(self.get_success_url())
    #     return super().post(request, *args, **kwargs)

class ToDoListCreateView(LoginRequiredMixin, CreateView):
    model = ToDoList
    form_class = ToDoListCreateForm
    context_object_name = 'todo_list'
    template_name = 'todolist_app//list_create.html'
    login_url = 'account_login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            with transaction.atomic():
                self.object = form.save()
                return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            form.add_error(None, str(e))  # Add a non-field error to the form
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('item_create')
    
class ToDoListDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDoList
    context_object_name = 'todo_list'
    template_name = 'todolist_app/list_delete.html'
    login_url = 'account_login'

    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('home')
    
class ToDoListUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDoList
    form_class = ToDoListUpdateForm
    context_object_name = 'todo_list'
    template_name = 'todolist_app/list_update.html'
    login_url = 'account_login'

    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('home')
    
    # def form_valid(self, form):
    #     try:
    #         with transaction.atomic():
    #             self.object = form.save()
    #             return HttpResponseRedirect(self.get_success_url())
    #     except Exception as e:
    #         form.add_error(None, str(e))  # Add a non-field error to the form
    #         return self.form_invalid(form)

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = ToDoItem
    form_class = ItemCreateForm
    context_object_name = 'todo_item'
    template_name = 'todolist_app/item_create.html'

    def get_login_url(self):
        return reverse('account_login')
    
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         # User is not logged in, redirect to login page with a query string
    #         next_url = request.path_info  # Capture the current URL path
    #         return redirect(reverse('account_login') + f'?next={next_url}')
    #     return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            with transaction.atomic():
                self.object = form.save()
                return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            form.add_error(None, str(e))  # Add a non-field error to the form
            return self.form_invalid(form)

    def get_success_url(self):
        todo_list_id = self.object.todo_list.id
        item_id = self.object.id
        return reverse('item_detail', kwargs={'id': todo_list_id, 'pk': item_id})
    
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDoItem
    context_object_name = 'todo_item'
    template_name = 'todolist_app/item_delete.html'
    login_url = 'account_login'

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list__user=self.request.user)
    
    def get_success_url(self):
        return reverse('home')