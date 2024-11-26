# from rest_framework.views import APIView
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
# from ..serializers.custom_user_serializers import CustomUserReadSerializer
# from rest_framework.response import Response
# from accounts.models import CustomUser
# from django.contrib.auth import authenticate,login
# from rest_framework_simplejwt.tokens import RefreshToken

# class LoginView(APIView):
#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'email': openapi.Schema(type=openapi.TYPE_STRING),
#                 'password': openapi.Schema(type=openapi.TYPE_STRING),
#             },
#             required=['email', 'password']
#         ),
#         # responses={200: MyResponseSerializer},
#         operation_summary="Login and get token",
#         operation_description="Login and get token",
#     )
#     @csrf_exempt
#     def post(self, request):
#         username_or_email = request.data.get('email')
#         password = request.data.get('password')

#         # Authenticate the user using either username or email
#         user = authenticate(request, username=username_or_email, password=password)
#         if user is None:
#             user = authenticate(request, email=username_or_email, password=password)

#         # If the user is authenticated, log them in and generate tokens
#         if user is not None:
#             if user.is_active == False:
#                 return Response({'error': 'Your Account is inactive'}, status=status.HTTP_401_UNAUTHORIZED)
#             login(request, user)
#             refresh = RefreshToken.for_user(user)
#             refresh['remember_me'] = request.data.get('remember_me',False)
#             user_obj = CustomUserReadSerializer(request.user,context={'request': request}) 
#             return Response({
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh),
#                 'user': user_obj.data,
#                 'message': 'Login successful',
#             }, status=status.HTTP_200_OK)

#         # If the user is not authenticated, return an error message
#         else:
#             from django.db.models import Q
#             user_obj = CustomUser.objects.filter(Q(username=username_or_email) | Q(email=username_or_email))
#             if user_obj.exists():
#                 return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
#             else:
#                 return Response({'error': 'Invalid username/email'}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from ..serializers.custom_user_serializers import CustomUserReadSerializer
from rest_framework.response import Response
from accounts.models import CustomUser
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email or username of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user'),
                'remember_me': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Remember me (optional)', default=False),
            },
            required=['email', 'password'],
        ),
        responses={
            200: openapi.Response(description="Login successful with tokens and user details"),
            401: openapi.Response(description="Invalid credentials or inactive account"),
        },
        operation_summary="User Login",
        operation_description="Authenticate user credentials and return JWT tokens along with user details.",
    )
    @csrf_exempt
    def post(self, request):
        # Extract credentials from request data
        username_or_email = request.data.get('email')
        password = request.data.get('password')
        remember_me = request.data.get('remember_me', False)

        print(f"Received login request for: {username_or_email}")  # Log received credentials (email/username)

        # Authenticate user by email or username
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            print(f"Initial authentication with username failed for: {username_or_email}")
            user = authenticate(request, email=username_or_email, password=password)

        # Handle successful authentication
        if user:
            print(f"Authentication successful for: {username_or_email}")  # Log successful authentication
            if not user.is_active:
                print(f"Inactive account for: {username_or_email}")  # Log inactive account
                return Response({'error': 'Your account is inactive.'}, status=status.HTTP_401_UNAUTHORIZED)

            # Log the user in
            login(request, user)
            print(f"User {username_or_email} logged in successfully.")  # Log login action

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            refresh['remember_me'] = remember_me

            # Serialize user details
            user_data = CustomUserReadSerializer(user, context={'request': request}).data

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_data,
                'message': 'Login successful',
            }, status=status.HTTP_200_OK)

        # Handle authentication failure
        user_exists = CustomUser.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).exists()
        if user_exists:
            print(f"Authentication failed for {username_or_email}: Invalid password.")  # Log invalid password
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            print(f"Authentication failed for {username_or_email}: User does not exist.")  # Log non-existent user
            return Response({'error': 'Invalid username/email'}, status=status.HTTP_401_UNAUTHORIZED)
