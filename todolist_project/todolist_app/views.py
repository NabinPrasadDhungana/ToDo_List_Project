from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, DeleteView
from .forms import *

from .models import *
# Create your views here.

# def home(request):
#     return render(request, 'index.html')

class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')

        if query:
            context['todo_items'] = ToDoItem.objects.filter(title__icontains=query)
        else:
            context['todo_items'] = ToDoItem.objects.all()

        return context
    
class ItemDetailView(DetailView):
    model = ToDoItem
    context_object_name = 'todo_item'
    template_name = 'todolist_app/item_detail.html'

class ItemUpdateView(UpdateView):
    model = ToDoItem
    form_class = ItemUpdateForm
    template_name = 'item_update.html'
    context_object_name = 'todo_item'
    template_name = 'todolist_app/item_update.html'

    def get_success_url(self):
        todo_list_id = self.object.todo_list.id
        item_id = self.object.id
        return reverse('item_detail', kwargs={'id': todo_list_id, 'pk': item_id})
    
    # def post(self, request, *args, **kwargs):
    #     if "cancel" in request.POST:
    #         return redirect(self.get_success_url())
    #     return super().post(request, *args, **kwargs)

class ToDoListCreateView(CreateView):
    model = ToDoList
    form_class = ToDoListCreateForm
    context_object_name = 'todo_list'
    template_name = 'todolist_app//list_create.html'

    def get_success_url(self):
        return reverse('item_create')

class ItemCreateView(CreateView):
    model = ToDoItem
    form_class = ItemCreateForm
    context_object_name = 'todo_item'
    template_name = 'todolist_app/item_create.html'

    def get_success_url(self):
        todo_list_id = self.object.todo_list.id
        item_id = self.object.id
        return reverse('item_detail', kwargs={'id': todo_list_id, 'pk': item_id})
    
class ItemDeleteView(DeleteView):
    model = ToDoItem
    context_object_name = 'todo_item'
    template_name = 'todolist_app/item_delete.html'
    def get_success_url(self):
        return reverse('home')