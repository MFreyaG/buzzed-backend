from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import Contact, User
from user.serializer import (
    ContactSerializer,
    LoginSerializer,
    SignupSerializer,
    UserSerializer,
)


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "User created",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        if user.pk != request.user.pk:
            return Response(
                {"detail": "You do not have permission to edit other users data."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        contacts = Contact.objects.filter(user1__pk=request.user.pk)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            try:
                contact = serializer.save()
                return Response(
                    ContactSerializer(contact).data, status=status.HTTP_201_CREATED
                )
            except ValidationError as e:
                return Response(
                    {"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        contact = get_object_or_404(
            Contact, user1_id=request.user.id, user2=request.data["user2"]
        )
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
