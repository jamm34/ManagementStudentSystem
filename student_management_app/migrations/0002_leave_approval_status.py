from django.db import migrations, models


def migrate_leave_status_forward(apps, schema_editor):
    LeaveReportStudent = apps.get_model('student_management_app', 'LeaveReportStudent')
    LeaveReportStaff = apps.get_model('student_management_app', 'LeaveReportStaff')

    LeaveReportStudent.objects.filter(leave_status=True).update(leave_approval_status=1)
    LeaveReportStudent.objects.filter(leave_status=False).update(leave_approval_status=0)

    LeaveReportStaff.objects.filter(leave_status=True).update(leave_approval_status=1)
    LeaveReportStaff.objects.filter(leave_status=False).update(leave_approval_status=0)


def migrate_leave_status_backward(apps, schema_editor):
    LeaveReportStudent = apps.get_model('student_management_app', 'LeaveReportStudent')
    LeaveReportStaff = apps.get_model('student_management_app', 'LeaveReportStaff')

    LeaveReportStudent.objects.filter(leave_approval_status=1).update(leave_status=True)
    LeaveReportStudent.objects.exclude(leave_approval_status=1).update(leave_status=False)

    LeaveReportStaff.objects.filter(leave_approval_status=1).update(leave_status=True)
    LeaveReportStaff.objects.exclude(leave_approval_status=1).update(leave_status=False)


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavereportstudent',
            name='leave_approval_status',
            field=models.PositiveSmallIntegerField(
                choices=[(0, 'Pendiente'), (1, 'Aprobado'), (2, 'Rechazado')],
                default=0,
            ),
        ),
        migrations.AddField(
            model_name='leavereportstaff',
            name='leave_approval_status',
            field=models.PositiveSmallIntegerField(
                choices=[(0, 'Pendiente'), (1, 'Aprobado'), (2, 'Rechazado')],
                default=0,
            ),
        ),
        migrations.RunPython(migrate_leave_status_forward, migrate_leave_status_backward),
    ]
