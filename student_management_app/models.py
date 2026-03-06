from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_type_data = ((1, 'HOD'), (2, 'Staff'), (3, 'Student'))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    LEAVE_STATUS_PENDING = 0
    LEAVE_STATUS_APPROVED = 1
    LEAVE_STATUS_REJECTED = 2
    LEAVE_STATUS_CHOICES = (
        (LEAVE_STATUS_PENDING, 'Pendiente'),
        (LEAVE_STATUS_APPROVED, 'Aprobado'),
        (LEAVE_STATUS_REJECTED, 'Rechazado'),
    )

    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    leave_approval_status = models.PositiveSmallIntegerField(
        choices=LEAVE_STATUS_CHOICES,
        default=LEAVE_STATUS_PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    LEAVE_STATUS_PENDING = 0
    LEAVE_STATUS_APPROVED = 1
    LEAVE_STATUS_REJECTED = 2
    LEAVE_STATUS_CHOICES = (
        (LEAVE_STATUS_PENDING, 'Pendiente'),
        (LEAVE_STATUS_APPROVED, 'Aprobado'),
        (LEAVE_STATUS_REJECTED, 'Rechazado'),
    )

    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    leave_approval_status = models.PositiveSmallIntegerField(
        choices=LEAVE_STATUS_CHOICES,
        default=LEAVE_STATUS_PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NavigationConfig(models.Model):
    ROLE_CHOICES = (
        ('1', 'HOD'),
        ('2', 'Staff'),
        ('3', 'Student'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, unique=True)
    brand = models.CharField(max_length=100, blank=True, default='')
    home_url_name = models.CharField(max_length=100, blank=True, default='')
    menu_json = models.TextField(help_text='JSON valido con la estructura de menu por rol')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Config navegacion rol {self.role}'

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        cache.delete(f'sidebar_role_config:{self.role}')
        return result

    def delete(self, *args, **kwargs):
        role = self.role
        result = super().delete(*args, **kwargs)
        cache.delete(f'sidebar_role_config:{role}')
        return result


class ActionAudit(models.Model):
    ACTION_CHOICES = (
        ('feedback_reply_student', 'Respuesta feedback estudiante'),
        ('feedback_reply_staff', 'Respuesta feedback personal'),
        ('leave_approve_student', 'Aprobar permiso estudiante'),
        ('leave_reject_student', 'Rechazar permiso estudiante'),
        ('leave_approve_staff', 'Aprobar permiso personal'),
        ('leave_reject_staff', 'Rechazar permiso personal'),
    )

    id = models.AutoField(primary_key=True)
    actor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='action_audits',
    )
    action_type = models.CharField(max_length=64, choices=ACTION_CHOICES)
    target_type = models.CharField(max_length=64, blank=True, default='')
    target_id = models.CharField(max_length=64, blank=True, default='')
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['action_type'], name='student_man_action__06924f_idx'),
            models.Index(fields=['created_at'], name='student_man_created_72f57f_idx'),
        ]

    def __str__(self):
        return f'{self.action_type} - {self.target_type}:{self.target_id}'


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance, address='')
        if instance.user_type == 3:
            Students.objects.create(
                admin=instance,
                course_id=Courses.objects.get(id=1),
                session_start_year='2020-01-01',
                session_end_year='2021-01-01',
                address='',
                profile_pic='',
                gender='',
            )


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()

