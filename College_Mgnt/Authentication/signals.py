 # Ensures the app registry is ready
from django.apps import AppConfig
from django.contrib.auth.models import  Permission,Group


def create_default_groups(sender, **kwargs):
        from django.apps import apps 
        if not apps.ready:
            return 
        
        group = Group.objects.get(name="Staff")  # Replace with the desired group name
        permissions = group.permissions.all()
        for perm in permissions:
            print(f"Codename: {perm.codename}, Name: {perm.name}")


        
        group = Group.objects.get(name="Users")  # Replace with the desired group name
        permissions = group.permissions.all()
        for perm in permissions:
            print(f"Codename: {perm.codename}, Name: {perm.name}")



        view_student = Permission.objects.get(codename='view_student')
        edit_student = Permission.objects.get(codename='change_student')
        add_student = Permission.objects.get(codename='add_student')
        edit_staff = Permission.objects.get(codename='change_staff')

        student_group = Group.objects.get(name="Users")
        staff_group = Group.objects.get(name="Staff")
        
        staff_permissions=[view_student,edit_student,add_student,edit_staff]
        student_permissions=[view_student,edit_student]

        staff_group.permissions.set(staff_permissions) 
        student_group.permissions.set(student_permissions) 








# Permissions
# Codename: add_logentry, Model: logentry
# Codename: change_logentry, Model: logentry
# Codename: delete_logentry, Model: logentry
# Codename: view_logentry, Model: logentry
# Codename: add_group, Model: group
# Codename: change_group, Model: group
# Codename: delete_group, Model: group
# Codename: view_group, Model: group
# Codename: add_permission, Model: permission
# Codename: change_permission, Model: permission
# Codename: delete_permission, Model: permission
# Codename: view_permission, Model: permission
# Codename: add_baseuser, Model: baseuser
# Codename: change_baseuser, Model: baseuser
# Codename: delete_baseuser, Model: baseuser
# Codename: view_baseuser, Model: baseuser
# Codename: add_staff, Model: staff
# Codename: change_staff, Model: staff
# Codename: delete_staff, Model: staff
# Codename: view_staff, Model: staff
# Codename: add_student, Model: student
# Codename: change_student, Model: student
# Codename: delete_student, Model: student
# Codename: view_student, Model: student
# Codename: add_subject, Model: subject
# Codename: change_subject, Model: subject
# Codename: delete_subject, Model: subject
# Codename: view_subject, Model: subject
# Codename: add_contenttype, Model: contenttype
# Codename: change_contenttype, Model: contenttype
# Codename: delete_contenttype, Model: contenttype
# Codename: view_contenttype, Model: contenttype
# Codename: add_session, Model: session
# Codename: change_session, Model: session
# Codename: delete_session, Model: session
# Codename: view_session, Model: session