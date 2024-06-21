from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView

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