# Generated by Django 5.1.3 on 2024-11-17 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0004_alter_staff_subject_delete_subject'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='staff',
            options={'verbose_name': 'Student User', 'verbose_name_plural': 'Student Users'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Student User', 'verbose_name_plural': 'Student Users'},
        ),
    ]
