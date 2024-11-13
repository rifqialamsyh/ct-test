from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.http import JsonResponse
# from django.views import View
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import json

class Register(APIView):
    @csrf_exempt
    def post(self, request):
        # Handle the POST request for registration
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        profile_photo = data.get('profile_photo', None)

        if not name or not email or not password:
            return JsonResponse({"error": "Name, email, and password are required!"}, status=400)

        # Hash the password
        hashed_password = make_password(password)

        try:
            user = User.objects.create(
                name=name,
                email=email,
                password=hashed_password,
                profile_photo=profile_photo
            )
            user.save()
            return JsonResponse({"message": "User created successfully!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

class Login(APIView):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({"error": "Email and password are required!"}, status=400)
        
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Return the JWT token along with a success message
                return JsonResponse({
                    "message": "Login successful!",
                    "access_token": access_token
                }, status=200)
            else:
                return JsonResponse({"error": "Invalid password!"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"error": "User not found!"}, status=404)

# List all users or create a new user
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = UserUpdateSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(password=make_password(request.data['password']))
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve a single user by ID
class UserDetailView(APIView):
    # permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, user_id):
        # Ensure the user is updating their own profile
        # if request.user.id != user_id:
        #     return Response({"detail": "You do not have permission to edit this profile."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(id=user_id)  # Get the user instance
        except User.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Create the serializer with the data from the request body (allow partial updates)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            # If password is in the data, hash it before saving
            if 'password' in request.data:
                user.password = make_password(request.data['password'])
            # Save the updated data to the user instance
            serializer.save()  

            # Return the updated user data
            return Response(serializer.data)
        
        # If there are validation errors in the serializer, return a bad request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return Response({"detail": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
