from rest_framework import serializers
from django.contrib.auth.models import Group

from Authentication.models import Student,Staff,Subject_Info

class StudentSerializer(serializers.ModelSerializer):
     class Meta:
          model=Student
          fields = ['first_name','last_name','email','phone_number','password','address','blood_group','gender','date_of_birth','profile']
    
     def validate(self,data):
        request_method = self.context.get('request_method')
        if self.instance is None:
         if request_method =='POST':
            required_fields = ['first_name', 'last_name', 'email', 'password']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError({field: f"This field is required to the  user!."})
            if Student.objects.filter(email=data['email']).exists():
                    raise serializers.ValidationError({'eamil': 'This email is already taken by a student.'})  
        
        elif self.instance is not None:    
          if request_method == 'PATCH':  
                required_fields = ['email']  
                for field in required_fields:
                    if not data.get(field):
                        raise serializers.ValidationError({field: f"This field is required to update the specific user!."})
                if not Student.objects.filter(email=data['email']).exists():
                    raise serializers.ValidationError({'email': 'There is no user with this email.'}) 

        return data
             
     def update(self,instance,validated_data,):
        email = validated_data.get('email')
        if 'username' not in validated_data:
            validated_data['username'] = email
        subjects = validated_data.pop('subject', [])   
        for field, value in validated_data.items():
            if field == 'password':
                instance.set_password(value)
            elif field =='subject':
                instance.subject.set(subjects) 
            else:
                setattr(instance, field, value)
        instance.save()
        return validated_data
     
     def create(self,validated_data):
        email = validated_data.get('email')
        if 'username' not in validated_data:
            validated_data['username'] = email
        password = validated_data.pop('password')
        subjects = validated_data.pop('subject', [])
        user = Student.objects.create(**validated_data)
        user.set_password(password)
        user.subject.set(subjects) 
        user.save()
        users_group = Group.objects.get(name='Users')
        user.groups.add(users_group)
        return validated_data
     

class StaffSerializer(serializers.ModelSerializer):
     class Meta:
          model=Staff
          fields=['email','students']
          students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(),required=False,many=True)

     def validate(self,data):
            if isinstance(self.instance, Staff):
                required_fields=['email','students']
                for field in required_fields:
                        if not data.get(field):
                            raise serializers.ValidationError({field: f"This field is required to update the specific user!."})  
                
                student_ids = [student.id for student in data['students']]
                students_to_set = Student.objects.filter(id__in=student_ids)
 
                data['students']=students_to_set
                if not Student.objects.filter(id__in=student_ids).exists():
                    raise serializers.ValidationError({'email': 'There is no user with this email.'}) 
            return data
     

     def update(self,instance,validated_data,):
        email = validated_data.get('email')
        if 'username' not in validated_data:
            validated_data['username'] = email
            students_to_update=validated_data['students']
        for field, value in validated_data.items():
            if field == 'password':
                instance.set_password(value)
            elif field=='students':
                instance.students.set(students_to_update)
            else:
                setattr(instance, field, value)
        instance.save()
        return validated_data
  

class SubjectSerializer(serializers.ModelSerializer):
     class Meta:
          model=Subject_Info
          fields='__all__'