from datetime import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_management_app.forms import AddStudentForm, EditStudentForm
from student_management_app.models import (
    ActionAudit,
    Attendance,
    AttendanceReport,
    Courses,
    CustomUser,
    FeedBackStaffs,
    FeedBackStudent,
    LeaveReportStaff,
    LeaveReportStudent,
    NotificationStaffs,
    NotificationStudent,
    Staffs,
    Students,
    Subjects,
)

def admin_home(request):
    staff_count = int(Staffs.objects.count())
    return render(request, 'hod_template/home_content.html', {'staff_count': staff_count})
def _log_action_audit(request, action_type, target_type, target_id, description):
    try:
        actor = request.user if getattr(request, 'user', None) and request.user.is_authenticated else None
        ActionAudit.objects.create(
            actor=actor,
            action_type=action_type,
            target_type=target_type,
            target_id=str(target_id),
            description=description,
        )
    except Exception:
        # Audit should never block the main business action.
        pass


def add_staff(request):
    return render(request, 'hod_template/add_staff_template.html')


def add_staff_save(request):
    if request.method != 'POST':
        return HttpResponse('Metodo no permitido')

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    address = request.POST.get('address')

    if CustomUser.objects.filter(username=username).exists():
        messages.error(request, 'El nombre de usuario ya existe')
        return HttpResponseRedirect(reverse('add_staff'))
    if CustomUser.objects.filter(email=email).exists():
        messages.error(request, 'El correo electronico ya existe')
        return HttpResponseRedirect(reverse('add_staff'))

    try:
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            last_name=last_name,
            first_name=first_name,
            user_type=2,
        )
        user.staffs.address = address
        user.save()
        messages.success(request, 'Personal agregado correctamente')
        return HttpResponseRedirect(reverse('manage_staff'))
    except Exception:
        messages.error(request, 'No se pudo agregar el personal')
        return HttpResponseRedirect(reverse('add_staff'))


def add_course(request):
    return render(request, 'hod_template/add_course_template.html')


def add_course_save(request):
    if request.method != 'POST':
        return HttpResponse('Metodo no permitido')

    course = request.POST.get('course')
    try:
        course_model = Courses(course_name=course)
        course_model.save()
        messages.success(request, 'Curso agregado correctamente')
        return HttpResponseRedirect(reverse('add_course'))
    except Exception:
        messages.error(request, 'No se pudo agregar el curso')
        return HttpResponseRedirect(reverse('add_course'))


def add_student(request):
    form = AddStudentForm()
    return render(request, 'hod_template/add_student_template.html', {'form': form})


def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse('Metodo no permitido')

    form = AddStudentForm(request.POST, request.FILES)
    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        address = form.cleaned_data['address']
        session_start = form.cleaned_data['session_start']
        session_end = form.cleaned_data['session_end']
        course_id = form.cleaned_data['course']
        sex = form.cleaned_data['sex']

        profile_pic = request.FILES.get('profile_pic')
        if profile_pic is None:
            messages.error(request, 'La foto de perfil es requerida')
            return render(request, 'hod_template/add_student_template.html', {'form': form})
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return render(request, 'hod_template/add_student_template.html', {'form': form})
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'El correo electronico ya existe')
            return render(request, 'hod_template/add_student_template.html', {'form': form})

        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        try:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                last_name=last_name,
                first_name=first_name,
                user_type=3,
            )
            user.students.address = address
            course_obj = Courses.objects.get(id=course_id)
            user.students.course_id = course_obj
            user.students.session_start_year = session_start
            user.students.session_end_year = session_end
            user.students.gender = sex
            user.students.profile_pic = profile_pic_url
            user.save()
            messages.success(request, 'Estudiante agregado correctamente')
            return HttpResponseRedirect(reverse('add_student'))
        except Exception:
            messages.error(request, 'No se pudo agregar el estudiante')
            return HttpResponseRedirect(reverse('add_student'))

    form = AddStudentForm(request.POST)
    return render(request, 'hod_template/add_student_template.html', {'form': form})


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'hod_template/add_subject_template.html', {'staffs': staffs, 'courses': courses})


def add_subject_save(request):
    if request.method != 'POST':
        return HttpResponse('<h2>Metodo no permitido</h2>')

    subject_name = request.POST.get('subject_name')
    course_id = request.POST.get('course')
    course = Courses.objects.get(id=course_id)
    staff_id = request.POST.get('staff')
    staff = CustomUser.objects.get(id=staff_id)

    try:
        subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
        subject.save()
        messages.success(request, 'Asignatura agregada correctamente')
        return HttpResponseRedirect(reverse('add_subject'))
    except Exception:
        messages.error(request, 'No se pudo agregar la asignatura')
        return HttpResponseRedirect(reverse('add_subject'))


def manage_staff(request):
    query = request.GET.get('q', '').strip()
    staffs_qs = Staffs.objects.select_related('admin').order_by('-created_at')
    if query:
        staffs_qs = staffs_qs.filter(
            Q(admin__first_name__icontains=query)
            | Q(admin__last_name__icontains=query)
            | Q(admin__username__icontains=query)
            | Q(admin__email__icontains=query)
            | Q(address__icontains=query)
        )

    paginator = Paginator(staffs_qs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(
        request,
        'hod_template/manage_staff_template.html',
        {'staffs': page_obj, 'q': query, 'page_obj': page_obj},
    )


def manage_student(request):
    query = request.GET.get('q', '').strip()
    students_qs = Students.objects.select_related('admin', 'course_id').order_by('-created_at')
    if query:
        students_qs = students_qs.filter(
            Q(admin__first_name__icontains=query)
            | Q(admin__last_name__icontains=query)
            | Q(admin__username__icontains=query)
            | Q(admin__email__icontains=query)
            | Q(course_id__course_name__icontains=query)
            | Q(gender__icontains=query)
        )

    paginator = Paginator(students_qs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(
        request,
        'hod_template/manage_student_template.html',
        {'students': page_obj, 'q': query, 'page_obj': page_obj},
    )


def manage_course(request):
    query = request.GET.get('q', '').strip()
    courses_qs = Courses.objects.order_by('-created_at')
    if query:
        courses_qs = courses_qs.filter(course_name__icontains=query)

    paginator = Paginator(courses_qs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(
        request,
        'hod_template/manage_course_template.html',
        {'courses': page_obj, 'q': query, 'page_obj': page_obj},
    )


def manage_subject(request):
    query = request.GET.get('q', '').strip()
    subjects_qs = Subjects.objects.select_related('course_id', 'staff_id').order_by('-created_at')
    if query:
        subjects_qs = subjects_qs.filter(
            Q(subject_name__icontains=query)
            | Q(course_id__course_name__icontains=query)
            | Q(staff_id__first_name__icontains=query)
            | Q(staff_id__last_name__icontains=query)
        )

    paginator = Paginator(subjects_qs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(
        request,
        'hod_template/manage_subject_template.html',
        {'subjects': page_obj, 'q': query, 'page_obj': page_obj},
    )


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request, 'hod_template/edit_staff_template.html', {'staff': staff, 'id': staff_id})


def edit_staff_save(request):
    if request.method != 'POST':
        return HttpResponse('<h2>Metodo no permitido</h2>')

    staff_id = request.POST.get('staff_id')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    username = request.POST.get('username')
    address = request.POST.get('address')

    try:
        user = CustomUser.objects.get(id=staff_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()

        staff_model = Staffs.objects.get(admin=staff_id)
        staff_model.address = address
        staff_model.save()
        messages.success(request, 'Personal editado correctamente')
        return HttpResponseRedirect(reverse('manage_staff'))
    except Exception:
        messages.error(request, 'No se pudo editar el personal')
        return HttpResponseRedirect(reverse('edit_staff', kwargs={'staff_id': staff_id}))


def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.course_id.id
    form.fields['sex'].initial = student.gender
    form.fields['session_start'].initial = student.session_start_year
    form.fields['session_end'].initial = student.session_end_year
    return render(
        request,
        'hod_template/edit_student_template.html',
        {'form': form, 'id': student_id, 'username': student.admin.username},
    )


def edit_student_save(request):
    if request.method != 'POST':
        return HttpResponse('<h2>Metodo no permitido</h2>')

    student_id = request.session.get('student_id')
    if student_id is None:
        return HttpResponseRedirect(reverse('manage_student'))

    form = EditStudentForm(request.POST, request.FILES)
    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        address = form.cleaned_data['address']
        session_start = form.cleaned_data['session_start']
        session_end = form.cleaned_data['session_end']
        course_id = form.cleaned_data['course']
        sex = form.cleaned_data['sex']

        if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            student = Students.objects.get(admin=student_id)
            student.address = address
            student.session_start_year = session_start
            student.session_end_year = session_end
            student.gender = sex
            course = Courses.objects.get(id=course_id)
            student.course_id = course
            if profile_pic_url is not None:
                student.profile_pic = profile_pic_url
            student.save()
            del request.session['student_id']
            messages.success(request, 'Estudiante editado correctamente')
            return HttpResponseRedirect(reverse('edit_student', kwargs={'student_id': student_id}))
        except Exception:
            messages.error(request, 'No se pudo editar el estudiante')
            return HttpResponseRedirect(reverse('edit_student', kwargs={'student_id': student_id}))

    form = EditStudentForm(request.POST)
    student = Students.objects.get(admin=student_id)
    return render(
        request,
        'hod_template/edit_student_template.html',
        {'form': form, 'id': student_id, 'username': student.admin.username},
    )


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(
        request,
        'hod_template/edit_subject_template.html',
        {'subject': subject, 'courses': courses, 'staffs': staffs},
    )


def edit_subject_save(request):
    if request.method != 'POST':
        return HttpResponse('<h2>Metodo no permitido</h2>')

    subject_id = request.POST.get('subject_id')
    subject_name = request.POST.get('subject_name')
    staff_id = request.POST.get('staff')
    course_id = request.POST.get('course')

    try:
        subject = Subjects.objects.get(id=subject_id)
        subject.subject_name = subject_name
        staff = CustomUser.objects.get(id=staff_id)
        subject.staff_id = staff
        course = Courses.objects.get(id=course_id)
        subject.course_id = course
        subject.save()

        messages.success(request, 'Asignatura editada correctamente')
        return HttpResponseRedirect(reverse('edit_subject', kwargs={'subject_id': subject_id}))
    except Exception:
        messages.error(request, 'No se pudo editar la asignatura')
        return HttpResponseRedirect(reverse('edit_subject', kwargs={'subject_id': subject_id}))


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(request, 'hod_template/edit_course_template.html', {'course': course})


def edit_course_save(request):
    if request.method != 'POST':
        return HttpResponse('<h2>Metodo no permitido</h2>')

    course_id = request.POST.get('course_id')
    course_name = request.POST.get('course')

    try:
        course = Courses.objects.get(id=course_id)
        course.course_name = course_name
        course.save()
        messages.success(request, 'Curso editado correctamente')
        return HttpResponseRedirect('edit_course/' + course_id)
    except Exception:
        messages.error(request, 'No se pudo editar el curso')
        return HttpResponseRedirect('edit_course/' + course_id)


def view_attendance_hod(request):
    attendance_count = Attendance.objects.count()
    present_count = AttendanceReport.objects.filter(status=True).count()
    absent_count = AttendanceReport.objects.filter(status=False).count()
    return render(
        request,
        'hod_template/attendance_overview_template.html',
        {
            'attendance_count': attendance_count,
            'present_count': present_count,
            'absent_count': absent_count,
        },
    )



def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None

def student_feedback_message(request):
    status = request.GET.get('status', 'todos')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    feedbacks = FeedBackStudent.objects.select_related('student_id__admin')

    if status == 'pendiente':
        feedbacks = feedbacks.filter(Q(feedback_reply__isnull=True) | Q(feedback_reply=''))
    elif status == 'respondido':
        feedbacks = feedbacks.exclude(Q(feedback_reply__isnull=True) | Q(feedback_reply=''))

    start_date_obj = _parse_date(start_date)
    if start_date_obj:
        feedbacks = feedbacks.filter(created_at__date__gte=start_date_obj)

    end_date_obj = _parse_date(end_date)
    if end_date_obj:
        feedbacks = feedbacks.filter(created_at__date__lte=end_date_obj)

    feedbacks = feedbacks.order_by('-created_at')

    return render(
        request,
        'hod_template/student_feedback_template.html',
        {
            'feedbacks': feedbacks,
            'status_filter': status,
            'start_date_filter': start_date,
            'end_date_filter': end_date,
        },
    )


def student_feedback_message_replied(request):
    if request.method != 'POST':
        return HttpResponse('Metodo no permitido')

    feedback_id = request.POST.get('feedback_id')
    feedback_reply = request.POST.get('feedback_reply')

    try:
        feedback = FeedBackStudent.objects.select_related('student_id').get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()

        NotificationStudent.objects.create(
            student_id=feedback.student_id,
            message='Tu feedback fue respondido por administracion.',
        )
        _log_action_audit(
            request,
            'feedback_reply_student',
            'FeedBackStudent',
            feedback.id,
            f'Respuesta enviada a feedback de estudiante #{feedback.id}',
        )
        messages.success(request, 'Respuesta enviada correctamente')
    except Exception:
        messages.error(request, 'No se pudo enviar la respuesta')

    return HttpResponseRedirect(reverse('student_feedback_message'))


def staff_feedback_message(request):
    status = request.GET.get('status', 'todos')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    feedbacks = FeedBackStaffs.objects.select_related('staff_id__admin')

    if status == 'pendiente':
        feedbacks = feedbacks.filter(Q(feedback_reply__isnull=True) | Q(feedback_reply=''))
    elif status == 'respondido':
        feedbacks = feedbacks.exclude(Q(feedback_reply__isnull=True) | Q(feedback_reply=''))

    start_date_obj = _parse_date(start_date)
    if start_date_obj:
        feedbacks = feedbacks.filter(created_at__date__gte=start_date_obj)

    end_date_obj = _parse_date(end_date)
    if end_date_obj:
        feedbacks = feedbacks.filter(created_at__date__lte=end_date_obj)

    feedbacks = feedbacks.order_by('-created_at')

    return render(
        request,
        'hod_template/staff_feedback_template.html',
        {
            'feedbacks': feedbacks,
            'status_filter': status,
            'start_date_filter': start_date,
            'end_date_filter': end_date,
        },
    )


def staff_feedback_message_replied(request):
    if request.method != 'POST':
        return HttpResponse('Metodo no permitido')

    feedback_id = request.POST.get('feedback_id')
    feedback_reply = request.POST.get('feedback_reply')

    try:
        feedback = FeedBackStaffs.objects.select_related('staff_id').get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()

        NotificationStaffs.objects.create(
            staff_id=feedback.staff_id,
            message='Tu feedback fue respondido por administracion.',
        )
        _log_action_audit(
            request,
            'feedback_reply_staff',
            'FeedBackStaffs',
            feedback.id,
            f'Respuesta enviada a feedback de personal #{feedback.id}',
        )
        messages.success(request, 'Respuesta enviada correctamente')
    except Exception:
        messages.error(request, 'No se pudo enviar la respuesta')

    return HttpResponseRedirect(reverse('staff_feedback_message'))


def student_leave_view(request):
    status = request.GET.get('status', 'todos')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    leaves = LeaveReportStudent.objects.select_related('student_id__admin')

    if status == 'pendiente':
        leaves = leaves.filter(leave_approval_status=LeaveReportStudent.LEAVE_STATUS_PENDING)
    elif status == 'aprobado':
        leaves = leaves.filter(leave_approval_status=LeaveReportStudent.LEAVE_STATUS_APPROVED)
    elif status == 'rechazado':
        leaves = leaves.filter(leave_approval_status=LeaveReportStudent.LEAVE_STATUS_REJECTED)

    start_date_obj = _parse_date(start_date)
    if start_date_obj:
        leaves = leaves.filter(created_at__date__gte=start_date_obj)

    end_date_obj = _parse_date(end_date)
    if end_date_obj:
        leaves = leaves.filter(created_at__date__lte=end_date_obj)

    leaves = leaves.order_by('-created_at')

    return render(
        request,
        'hod_template/student_leave_template.html',
        {
            'leaves': leaves,
            'status_filter': status,
            'start_date_filter': start_date,
            'end_date_filter': end_date,
        },
    )


def student_leave_approve(request, leave_id):
    try:
        leave = LeaveReportStudent.objects.select_related('student_id').get(id=leave_id)
        leave.leave_status = True
        leave.leave_approval_status = LeaveReportStudent.LEAVE_STATUS_APPROVED
        leave.save()

        NotificationStudent.objects.create(
            student_id=leave.student_id,
            message='Tu solicitud de permiso fue aprobada.',
        )
        _log_action_audit(
            request,
            'leave_approve_student',
            'LeaveReportStudent',
            leave.id,
            f'Permiso de estudiante aprobado #{leave.id}',
        )
        messages.success(request, 'Permiso de estudiante aprobado')
    except Exception:
        messages.error(request, 'No se pudo actualizar el permiso')
    return HttpResponseRedirect(reverse('student_leave_view'))


def student_leave_reject(request, leave_id):
    try:
        leave = LeaveReportStudent.objects.select_related('student_id').get(id=leave_id)
        leave.leave_status = False
        leave.leave_approval_status = LeaveReportStudent.LEAVE_STATUS_REJECTED
        leave.save()

        NotificationStudent.objects.create(
            student_id=leave.student_id,
            message='Tu solicitud de permiso fue rechazada.',
        )
        _log_action_audit(
            request,
            'leave_reject_student',
            'LeaveReportStudent',
            leave.id,
            f'Permiso de estudiante rechazado #{leave.id}',
        )
        messages.success(request, 'Permiso de estudiante rechazado')
    except Exception:
        messages.error(request, 'No se pudo actualizar el permiso')
    return HttpResponseRedirect(reverse('student_leave_view'))


def staff_leave_view(request):
    status = request.GET.get('status', 'todos')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    leaves = LeaveReportStaff.objects.select_related('staff_id__admin')

    if status == 'pendiente':
        leaves = leaves.filter(leave_approval_status=LeaveReportStaff.LEAVE_STATUS_PENDING)
    elif status == 'aprobado':
        leaves = leaves.filter(leave_approval_status=LeaveReportStaff.LEAVE_STATUS_APPROVED)
    elif status == 'rechazado':
        leaves = leaves.filter(leave_approval_status=LeaveReportStaff.LEAVE_STATUS_REJECTED)

    start_date_obj = _parse_date(start_date)
    if start_date_obj:
        leaves = leaves.filter(created_at__date__gte=start_date_obj)

    end_date_obj = _parse_date(end_date)
    if end_date_obj:
        leaves = leaves.filter(created_at__date__lte=end_date_obj)

    leaves = leaves.order_by('-created_at')

    return render(
        request,
        'hod_template/staff_leave_template.html',
        {
            'leaves': leaves,
            'status_filter': status,
            'start_date_filter': start_date,
            'end_date_filter': end_date,
        },
    )


def staff_leave_approve(request, leave_id):
    try:
        leave = LeaveReportStaff.objects.select_related('staff_id').get(id=leave_id)
        leave.leave_status = True
        leave.leave_approval_status = LeaveReportStaff.LEAVE_STATUS_APPROVED
        leave.save()

        NotificationStaffs.objects.create(
            staff_id=leave.staff_id,
            message='Tu solicitud de permiso fue aprobada.',
        )
        _log_action_audit(
            request,
            'leave_approve_staff',
            'LeaveReportStaff',
            leave.id,
            f'Permiso de personal aprobado #{leave.id}',
        )
        messages.success(request, 'Permiso de personal aprobado')
    except Exception:
        messages.error(request, 'No se pudo actualizar el permiso')
    return HttpResponseRedirect(reverse('staff_leave_view'))


def staff_leave_reject(request, leave_id):
    try:
        leave = LeaveReportStaff.objects.select_related('staff_id').get(id=leave_id)
        leave.leave_status = False
        leave.leave_approval_status = LeaveReportStaff.LEAVE_STATUS_REJECTED
        leave.save()

        NotificationStaffs.objects.create(
            staff_id=leave.staff_id,
            message='Tu solicitud de permiso fue rechazada.',
        )
        _log_action_audit(
            request,
            'leave_reject_staff',
            'LeaveReportStaff',
            leave.id,
            f'Permiso de personal rechazado #{leave.id}',
        )
        messages.success(request, 'Permiso de personal rechazado')
    except Exception:
        messages.error(request, 'No se pudo actualizar el permiso')
    return HttpResponseRedirect(reverse('staff_leave_view'))

















def audit_log_view(request):
    query = request.GET.get('q', '').strip()
    action_type = request.GET.get('action_type', '').strip()

    audits_qs = ActionAudit.objects.select_related('actor').all()

    if query:
        audits_qs = audits_qs.filter(
            Q(description__icontains=query)
            | Q(target_type__icontains=query)
            | Q(target_id__icontains=query)
            | Q(actor__username__icontains=query)
            | Q(actor__first_name__icontains=query)
            | Q(actor__last_name__icontains=query)
        )

    if action_type:
        audits_qs = audits_qs.filter(action_type=action_type)

    paginator = Paginator(audits_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(
        request,
        'hod_template/audit_log_template.html',
        {
            'audits': page_obj,
            'page_obj': page_obj,
            'q': query,
            'action_type_filter': action_type,
            'action_choices': ActionAudit.ACTION_CHOICES,
        },
    )
