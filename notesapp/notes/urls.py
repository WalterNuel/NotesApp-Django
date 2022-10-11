from django.urls import path

from notes.models import Note
from .views import InfoView, NoteUpdate, NoteCreate, CustomLoginView, NoteList, RegisterPage, NoteDelete

from django.contrib.auth.views import LogoutView

app_name =  'notes'

urlpatterns = [
  #User auth
  path("accounts/login/", CustomLoginView.as_view(), name="login"),
  path("logout/", LogoutView.as_view(next_page = 'notes:login'), name="logout"),
  path("register/", RegisterPage.as_view(), name="register"),

  #Functionalities
  path("notes/", NoteList.as_view(), name="dashboard"),
  path("notes/<int:pk>/", InfoView.as_view(), name="details"),
  path('notes/delete/<int:pk>/', NoteDelete.as_view(), name='note-delete'),
  path("notes/edit/<int:pk>/", NoteUpdate.as_view(), name="note-update"),
  path("addnote/", NoteCreate.as_view(), name="new-note")
]
