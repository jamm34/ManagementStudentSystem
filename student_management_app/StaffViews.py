from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_management_app.models import FeedBackStaffs, LeaveReportStaff, NotificationStaffs, Staffs


def _get_staff(request):
    return Staffs.objects.get(admin=request.user.id)


def staff_home(request):
    staff = _get_staff(request)
    pending_leaves = LeaveReportStaff.objects.filter(
        staff_id=staff,
        leave_approval_status=LeaveReportStaff.LEAVE_STATUS_PENDING,
    ).count()
    pending_feedback = FeedBackStaffs.objects.filter(staff_id=staff).filter(
        Q(feedback_reply__isnull=True) | Q(feedback_reply='')
    ).count()
    return render(
        request,
        'staff_template/staff_home_template.html',
        {
            'pending_leaves': pending_leaves,
            'pending_feedback': pending_feedback,
        },
    )


def staff_apply_leave(request):
    staff = _get_staff(request)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff).order_by('-created_at')
    return render(request, 'staff_template/staff_apply_leave_template.html', {'leave_data': leave_data})


def staff_apply_leave_save(request):
    if request.method != 'POST':
        return HttpResponse('Metodo no permitido')

    leave_date = request.POST.get('leave_date')
    leave_message = request.POST.get('leave_message')

    try:
        staff = _get_staff(request)
        leave = LeaveReportStaff(
            staff_id=staff,
            leave_date=leave_date,
            leave_message=leave_message,
            leave_status=False,
            leave_approval_status=LeaveReportStaff.LEAVE_STATUS_PENDING,
        )
        leave.save()
        messages.success(request, 'Solicitud de permiso enviada')
    except Exception:
        messages.error(request, 'No se pudo enviar la solicitud')

    return HttpResponseRedirect(reverse('staff_apply_leave'))


def staff_feedback(request):
    staff = _get_staff(request)
    feedback_data = FeedBackStaffs.objects.filter(staff_id=staff).order_by('-created_at')
    return render(request, 'staff_template/staff_feedback_template.html', {'feedback_data': feedback_data})


def staff_feedback_save(request):
    if request.method != 'POST':
        return HttpResponse('Método no permitido')

    feedback_message = request.POST.get('feedback_message')

    try:
        staff = _get_staff(request)
        feedback = FeedBackStaffs(staff_id=staff, feedback=feedback_message, feedback_reply='')
        feedback.save()
        messages.success(request, 'Feedback enviado correctamente')
    except Exception:
        messages.error(request, 'No se pudo enviar el feedback')

    return HttpResponseRedirect(reverse('staff_feedback'))


def staff_notification(request):
    staff = _get_staff(request)
    notifications = NotificationStaffs.objects.filter(staff_id=staff).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    return render(
        request,
        'staff_template/staff_notification_template.html',
        {
            'notifications': notifications,
            'unread_count': unread_count,
        },
    )


def staff_notification_mark_read(request, notification_id):
    staff = _get_staff(request)
    NotificationStaffs.objects.filter(id=notification_id, staff_id=staff).update(is_read=True)
    return HttpResponseRedirect(reverse('staff_notification'))


def staff_notification_mark_all_read(request):
    staff = _get_staff(request)
    NotificationStaffs.objects.filter(staff_id=staff, is_read=False).update(is_read=True)
    return HttpResponseRedirect(reverse('staff_notification'))


