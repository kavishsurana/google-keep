from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Note
from .serializers import NoteSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

class NoteListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        image = self.request.data.get('image', None)
        if image:
            serializer.save(image=image, user=self.request.user)
        else:
            serializer.save(user=self.request.user)

class NoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    
class UserSignup(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, password=password)
            token, _ = Token.objects.get_or_create(user=user)  
            return Response({'success': 'User created successfully', 'user_id': user.id, 'token': token.key}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UploadImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        card_id = request.data.get('card_id')
        image_file = request.data.get('image')

        if not card_id:
            return Response({'error': 'Card ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not image_file:
            return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            note = Note.objects.get(pk=card_id)

            note.image = image_file
            note.save()

            return Response({'success': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)
        except Note.DoesNotExist:
            return Response({'error': 'Note does not exist'}, status=status.HTTP_404_NOT_FOUND)

    
class UserNoteList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Note.objects.filter(user_id=user_id)
    
    queryset = Note.objects.select_related('user').prefetch_related('tags')