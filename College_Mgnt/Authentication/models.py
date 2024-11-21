from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

class Subject_Info(models.Model):
    SUBJECT_CHOICES = [
        ('Tamil', 'Tamil'),
        ('English', 'English'),
        ('Maths', 'Maths'),
        ('Politics', 'Politics'),
        ('Economics', 'Economics'),
        ('History', 'History'),
        ('Geography', 'Geography'),
        ('Computer Science', 'Computer Science'),
        ('Chemistry', 'Chemistry'),
        ('Physics', 'Physics'),
        ('Botany', 'Botany'),
        ('Zoology', 'Zoology')
    ]
    subject_name=models.CharField(choices=SUBJECT_CHOICES,null=True)

    def __str__(self):
         return f"{self.id}"


class BaseUser(AbstractUser):
    class Meta:
        abstract = False  
    
    email = models.EmailField(unique=True) 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 
    groups = models.ManyToManyField(
        Group, 
        related_name='%(app_label)s_%(class)s_groups',  
        blank=True )

class Student(BaseUser):
    class Meta:
        verbose_name = 'Student User'
        verbose_name_plural = 'Student Users'
    phone_number = models.CharField(max_length=15,  null=True)     
    address = models.TextField( null=True)  
    blood_group=models.CharField(max_length=3,null=True)    
    gender=models.CharField(max_length=6,null=True)
    date_of_birth = models.DateField(null=True)
    profile=models.ImageField(null=True)
    subject = models.ManyToManyField(Subject_Info, related_name="students")

    def __str__(self):
         return f"{self.first_name} {self.last_name}"    

class Staff(BaseUser):
    class Meta:
        verbose_name = 'Staff User'
        verbose_name_plural = 'Staff User'
    subject = models.OneToOneField(Subject_Info,related_name="allocated_subject",on_delete=models.CASCADE)
    students = models.ManyToManyField(
        Student,
        related_name="staff_members",  
    )
    def __str__(self):
         return f"{self.first_name} {self.last_name}"

