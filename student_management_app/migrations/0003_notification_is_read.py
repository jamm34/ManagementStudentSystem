from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0002_leave_approval_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationstudent',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notificationstaffs',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
