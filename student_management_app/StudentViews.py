from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_management_app.models import FeedBackStudent, LeaveReportStudent, NotificationStudent, Students


def _get_student(request):
    return Students.objects.get(admin=request.user.id)


def student_home(request):
    student = _get_student(request)
    pending_leaves = LeaveReportStudent.objects.filter(
        student_id=student,
        leave_approval_status=LeaveReportStudent.LEAVE_STATUS_PENDING,
    ).count()
    pending_feedback = FeedBackStudent.objects.filter(student_id=student).filter(
        Q(feedback_reply__isnull=True) | Q(feedback_reply='')
    ).count()
    return render(
        request,
        'student_template/student_home_template.html',
        {
            'pending_leaves': pending_leaves,
            'pending_feedback': pending_feedback,
        },
    )


def student_apply_leave(request):
    student = _get_student(request)
    leave_data = LeaveReportStudent.objects.filter(student_id=student).order_by('-created_at')
    return render(request, 'student_template/student_apply_leave_template.html', {'leave_data': leave_data})


def student_apply_leave_save(request):
    if request.method != 'POST':
        return HttpResponse('Metodo no permitido')

    leave_date = request.POST.get('leave_date')
    leave_message = request.POST.get('leave_message')

    try:
        student = _get_student(request)
        leave = LeaveReportStudent(
            student_id=student,
            leave_date=leave_date,
            leave_message=leave_message,
            leave_status=False,
            leave_approval_status=LeaveReportStudent.LEAVE_STATUS_PENDING,
        )
        leave.save()
        messages.success(request, 'Solicitud de permiso enviada')
    except Exception:
        messages.error(request, 'No se pudo enviar la solicitud')

    return HttpResponseRedirect(reverse('student_apply_leave'))


def student_feedback(request):
    student = _get_student(request)
    feedback_data = FeedBackStudent.objects.filter(student_id=student).order_by('-created_at')
    return render(request, 'student_template/student_feedback_template.html', {'feedback_data': feedback_data})


def student_feedback_save(request):
    if request.method != 'POST':
        return HttpResponse('Método no permitido')

    feedback_message = request.POST.get('feedback_message')

    try:
        student = _get_student(request)
        feedback = FeedBackStudent(student_id=student, feedback=feedback_message, feedback_reply='')
        feedback.save()
        messages.success(request, 'Feedback enviado correctamente')
    except Exception:
        messages.error(request, 'No se pudo enviar el feedback')

    return HttpResponseRedirect(reverse('student_feedback'))


def student_notification(request):
    student = _get_student(request)
    notifications = NotificationStudent.objects.filter(student_id=student).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    return render(
        request,
        'student_template/student_notification_template.html',
        {
            'notifications': notifications,
            'unread_count': unread_count,
        },
    )


def student_notification_mark_read(request, notification_id):
    student = _get_student(request)
    NotificationStudent.objects.filter(id=notification_id, student_id=student).update(is_read=True)
    return HttpResponseRedirect(reverse('student_notification'))


def student_notification_mark_all_read(request):
    student = _get_student(request)
    NotificationStudent.objects.filter(student_id=student, is_read=False).update(is_read=True)
    return HttpResponseRedirect(reverse('student_notification'))


