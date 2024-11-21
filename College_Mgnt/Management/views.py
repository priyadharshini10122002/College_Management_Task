from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Authentication.models import Staff,Student,Subject_Info
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import StudentSerializer,StaffSerializer,SubjectSerializer

#Handles all the actions of the Staff
class StaffView(APIView):
    #Check Authneticated and Permitted user
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    #Get Method retrives data from db
    def get(self,request):
        try:    
              instance= Student.objects.all()
              serializer=StudentSerializer(instance,many=True)
              return Response({'data':serializer.data,
                             'message':'data fetched Successfully!'},
                             status=status.HTTP_200_OK)        
        except Exception as e:
            print(e)
            return Response({'data':{},
                            'message':'Something went wrong!'},
                            status=status.HTTP_400_BAD_REQUEST)

    #Creating the new Student Instance    
    def post(self, request):
        try:
            data=request.data 
            serializer=StudentSerializer(data=data,context={'request_method': "POST"})
            
            if not serializer.is_valid():
                     return Response({'data':serializer.errors,
                                'message':'Invalid data wrong! serializer not valid'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                             'message':'User has been  Created Successfully!'},
                             status=status.HTTP_201_CREATED)        
        except Exception as e:
            print(e)
            return Response({'data':{},
                            'message':'Error Occured ! Something went wrong!'},
                            status=status.HTTP_400_BAD_REQUEST)         
    #Patch Updates the and Staff and the Student
    def patch(self,request):
        try:
            data=request.data
            student_instance = Student.objects.filter(email=data.get('email')).first()
            staff_instance = Staff.objects.filter(email=data.get('email')).first()
            if not student_instance :
              if not staff_instance:
                return Response({'data':{},
                            'message':'No User exitst for this email!'},
                            status=status.HTTP_400_BAD_REQUEST)

            instance = student_instance if student_instance else staff_instance

            if student_instance:
                serializer=StudentSerializer(instance,data=data,partial=True,
                                             context={'request_method': 'PATCH' ,'user':student_instance})
            else:
                student_ids = list(Student.objects.filter
                           (email__in=data['students']).
                           values_list('id', flat=True))                
                data['students']=student_ids
                serializer=StaffSerializer(instance,data=data,partial=True,
                                           context={'request_method': 'PATCH','user':staff_instance})
        
            if not serializer.is_valid():
                     return Response({'data':{},
                                'message':'Something went wrong Serializer not Valid!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()        
            return Response({'data':serializer.data,
                             'message':'User has been Updated Successfully!'},
                             status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'data':{},
                            'message':'Something went wrong!'},
                            status=status.HTTP_400_BAD_REQUEST)
    
class StudentView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def get(self,request):
        user = request.user
        try:
              student = Student.objects.filter(email=user).first()
              #fields=['first_name', 'email'] we can mention here
              serializer=StudentSerializer(student)
              return Response({'data':serializer.data,
                             'message':'data fetched Successfully!'},
                             status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':{e},
                            'message':'Something went wrong!'},
                            status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self,request):
        try:
            data=request.data
            user = request.user
            student_instance = Student.objects.filter(email=user).first()
            if not student_instance :
                return Response({'data':{},
                            'message':'No User exitst for this email!'},
                            status=status.HTTP_400_BAD_REQUEST)

            if student_instance:
                serializer=StudentSerializer(student_instance,data=data,partial=True,
                                             context={'request_method': 'PATCH' ,'user':student_instance})
                    
            if not serializer.is_valid():
                     return Response({'data':serializer.errors,
                                'message':'Something went wrong Serializer not Valid!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()        
            return Response({'data':serializer.data,
                             'message':'User has been Updated Successfully!'},
                             status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'data':{},
                            'message':'Something went wrong!'},
                            status=status.HTTP_400_BAD_REQUEST)
    
class SubjectView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]   

    def get(self,request):
        user = request.user
        print(user)

        try:
              student = Student.objects.filter(email=user).first()
              subjects = student.subject.all()
              print(subjects)
              serializer= SubjectSerializer(subjects, many=True)
            #   print(serializer.data)
              return Response({'data':serializer.data,
                             'message':'data fetched Successfully!'},
                             status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'data':{},
                            'message':'Something went wrong!'},
                            status=status.HTTP_400_BAD_REQUEST)
