# api/views.py
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import UserBalance
from .serializers import UserRegistrationSerializer, UserBalanceSerializer

def frontend_view(request):
    return render(request, 'api/index.html')

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserRegistrationSerializer(user, context=self.get_serializer_context()).data,
            "message": "User registered successfully",
        }, status=status.HTTP_201_CREATED)


class UserBalanceView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_balance = UserBalance.objects.get(user=request.user)
        serializer = UserBalanceSerializer(user_balance)
        return Response(serializer.data)


