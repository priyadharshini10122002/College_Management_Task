from .models import Student,Staff,Subject_Info
from rest_framework import serializers
from django.contrib.auth.models import Group,Permission
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
    
class RegisterSerializer(serializers.Serializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user = serializers.CharField()
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject_Info.objects.all(),required=False)

    def validate(self, data):
        if(data['user']=='Student'):
            required_fields = ['first_name', 'last_name', 'email', 'password','user']
            for field in required_fields:
             if not data.get(field):
                raise serializers.ValidationError({field: f"This field is required."})
            if Student.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError({'eamil': 'This email is already taken by a student.'})
        
        elif(data['user']=='Staff'):
            required_fields = ['first_name', 'last_name', 'email', 'password','user','subject']
            for field in required_fields:
                 if not data.get(field):
                    raise serializers.ValidationError({field: f"This field is required."})
            if Staff.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError({'email': 'This email is already taken by a staff member.'})        
        return data   
    
    def create(self,validated_data):
        user_type = validated_data.pop('user', None)
        email = validated_data.get('email')
        if 'username' not in validated_data:
            validated_data['username'] = email

        if(user_type=='Staff'):
                    password = validated_data.pop('password')
                    subject = validated_data.pop('subject')
                    user = Staff.objects.create(**validated_data)
                    user.set_password(password)
                    user.save()
                    staff_instance = Staff.objects.filter(email=email).first()
                    staff_instance.subject=subject 
                    staff_instance.save()
                    staff_group = Group.objects.get(name='Staff')
                    user.groups.add(staff_group)
        
        else:
                    password = validated_data.pop('password')
                    user = Student.objects.create(**validated_data)
                    user.set_password(password)
                    user.save()
                    users_group = Group.objects.get(name='Users')
                    user.groups.add(users_group)
        
        return validated_data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password=serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        student_user=Student.objects.filter(email=email).exists()
        staff_user=Staff.objects.filter(email=email).exists()
        user_type=student_user or staff_user
        if user_type:
            if (student_user):
                student = Student.objects.get(email=email)
                if not student.check_password(password):
                             raise serializers.ValidationError('Password Mismatch!')
                return data
             
            if (staff_user):
                    staff = Staff.objects.get(email=email)
                    if not staff.check_password(password):
                             raise serializers.ValidationError('Password Mismatch!')
                  
                    return data
        else:
              raise serializers.ValidationError('Not a Registered User!')                
        
    def get_jwt_token(self,data):
        user=authenticate(email=data['email'],password=data['password'])
        if not user:
            return {'message':'Invalid Credentials' ,'data':{}}
        
        refresh=RefreshToken.for_user(user)
        return {'message':'Login Success!' ,'data':{'token':
     {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }   }}




