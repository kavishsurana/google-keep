from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('login/', obtain_auth_token, name='login'),
    path('notes/', views.NoteListCreate.as_view(), name='note-list'),
    path('notes/<int:pk>/', views.NoteRetrieveUpdateDestroy.as_view(), name='note-detail'),
    path('users/<int:user_id>/notes/', views.UserNoteList.as_view(), name='user-note-list'),
    path('upload-image/', views.UploadImageView.as_view(), name='upload-image'),
]