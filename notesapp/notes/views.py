from turtle import title
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.urls import reverse_lazy

from .models import Note

# Note list view
# class IndexView(ListView):
#   template_name = 'notes/dashboard.html'
#   context_object_name = 'latest_notes'

#   def get_queryset(self):
#     return Note.objects.order_by('-entry_date')[:5]

'''Notes info view
  -Note title
  -Note body
  -Entry date'''


class InfoView(DetailView):
    model = Note
    template_name = 'notes/details.html'

# Create note function


class NoteCreate(CreateView):
    model = Note
    template_name = 'notes/new_note.html'
    fields = ['title', 'note_text']
    context_object_name = 'notes'
    success_url = reverse_lazy('notes:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(NoteCreate, self).form_valid(form)


# Note update or changing
class NoteUpdate(UpdateView):
    model = Note
    template_name = 'notes/note_edit.html'
    fields = ['title', 'note_text']
    success_url = reverse_lazy('notes:dashboard')

# Login page for user
class CustomLoginView(LoginView):
    template_name = 'notes/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('notes:dashboard')


# Register page for new users

class RegisterPage(FormView):
    template_name = 'notes/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('notes:dashboard')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes:dashboard')
        return super(RegisterPage, self).get(*args, **kwargs)

# Showing the notes for the present user


class NoteList(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'notes/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].order_by('-entry_date')
        context['notes'] = context['notes'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area')
        if search_input:
            if search_input.lower() == 'oldest':
              context['notes'] = context['notes'].order_by('entry_date')
              return context
            context['notes'] = context['notes'].filter(title__icontains=search_input)
            return context
        else:
          return context

# Notes delete functionality


class NoteDelete(DeleteView):
    model = Note
    context_object_name = 'notes'
    template_name = 'notes/delete.html'
    success_url = reverse_lazy('notes:dashboard')
