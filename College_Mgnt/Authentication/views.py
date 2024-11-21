from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from .serializers import RegisterSerializer,LoginSerializer

class RegisterView(APIView):  
    def post(self,request):
        try:
            data=request.data
            serializer=RegisterSerializer(data=data)

            if not serializer.is_valid():
                return Response({'data':serializer.errors,
                                'message':'Something went wrong while data validation !'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'message':'Your Account has Created Successfully!'},
                             status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({'message':'Something went wrong!'},
                            status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    def post(self, request):
        try:
            data=request.data
            serializer=LoginSerializer(data=data)
            if not serializer.is_valid():
                return Response({'data':serializer.errors,
                                'message':'Something went wrong! Serializer is not valid'},
                                status=status.HTTP_400_BAD_REQUEST)
            response =serializer.get_jwt_token(serializer.data)
            return Response(response,status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'data':{e},
                            'message':'Something went wrong!'},
                            status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out!'}, status=200)

        except InvalidToken:
            return Response({'message': 'Invalid token!'}, status=400)
        