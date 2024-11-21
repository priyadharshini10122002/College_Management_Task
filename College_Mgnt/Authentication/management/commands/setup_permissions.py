from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Set up groups and permissions'

    def handle(self, *args, **kwargs):

        view_student = Permission.objects.get(codename='view_student')
        change_student = Permission.objects.get(codename='change_student')
        add_student = Permission.objects.get(codename='add_student')
        change_staff = Permission.objects.get(codename='change_staff')

        staff_group, _ = Group.objects.get_or_create(name='Staff')
        student_group, _ = Group.objects.get_or_create(name='Users')

        staff_group.permissions.set([view_student, change_student, add_student, change_staff])
        student_group.permissions.set([view_student, change_student])

        self.stdout.write(self.style.SUCCESS("Groups and permissions have been set up successfully."))
