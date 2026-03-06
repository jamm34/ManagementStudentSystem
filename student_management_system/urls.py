from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from student_management_system import settings

from student_management_app import HodViews, StaffViews, StudentViews, views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ShowLoginPage, name='show_login'),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user, name='logout'),
    path('doLogin', views.doLogin, name='do_login'),

    # HOD
    path('admin_home', HodViews.admin_home, name='admin_home'),
    path('add_staff', HodViews.add_staff, name='add_staff'),
    path('add_staff_save', HodViews.add_staff_save, name='add_staff_save'),
    path('add_course', HodViews.add_course, name='add_course'),
    path('add_course_save', HodViews.add_course_save, name='add_course_save'),
    path('add_student', HodViews.add_student, name='add_student'),
    path('add_student_save', HodViews.add_student_save, name='add_student_save'),
    path('add_subject', HodViews.add_subject, name='add_subject'),
    path('add_subject_save', HodViews.add_subject_save, name='add_subject_save'),
    path('manage_staff', HodViews.manage_staff, name='manage_staff'),
    path('manage_student', HodViews.manage_student, name='manage_student'),
    path('manage_course', HodViews.manage_course, name='manage_course'),
    path('manage_subject', HodViews.manage_subject, name='manage_subject'),
    path('edit_staff/<str:staff_id>', HodViews.edit_staff, name='edit_staff'),
    path('edit_staff_save', HodViews.edit_staff_save, name='edit_staff_save'),
    path('edit_student/<str:student_id>', HodViews.edit_student, name='edit_student'),
    path('edit_student_save', HodViews.edit_student_save, name='edit_student_save'),
    path('edit_subject/<str:subject_id>', HodViews.edit_subject, name='edit_subject'),
    path('edit_subject_save', HodViews.edit_subject_save, name='edit_subject_save'),
    path('edit_course/<str:course_id>', HodViews.edit_course, name='edit_course'),
    path('edit_course_save', HodViews.edit_course_save, name='edit_course_save'),

    # HOD Seguimiento
    path('view_attendance_hod', HodViews.view_attendance_hod, name='view_attendance_hod'),
    path('student_feedback_message', HodViews.student_feedback_message, name='student_feedback_message'),
    path(
        'student_feedback_message_replied',
        HodViews.student_feedback_message_replied,
        name='student_feedback_message_replied',
    ),
    path('staff_feedback_message', HodViews.staff_feedback_message, name='staff_feedback_message'),
    path(
        'staff_feedback_message_replied',
        HodViews.staff_feedback_message_replied,
        name='staff_feedback_message_replied',
    ),
    path('student_leave_view', HodViews.student_leave_view, name='student_leave_view'),
    path('student_leave_approve/<int:leave_id>', HodViews.student_leave_approve, name='student_leave_approve'),
    path('student_leave_reject/<int:leave_id>', HodViews.student_leave_reject, name='student_leave_reject'),
    path('staff_leave_view', HodViews.staff_leave_view, name='staff_leave_view'),
    path('staff_leave_approve/<int:leave_id>', HodViews.staff_leave_approve, name='staff_leave_approve'),
    path('staff_leave_reject/<int:leave_id>', HodViews.staff_leave_reject, name='staff_leave_reject'),
    path('audit_log', HodViews.audit_log_view, name='audit_log'),

    # Staff
    path('staff_home', StaffViews.staff_home, name='staff_home'),
    path('staff_apply_leave', StaffViews.staff_apply_leave, name='staff_apply_leave'),
    path('staff_apply_leave_save', StaffViews.staff_apply_leave_save, name='staff_apply_leave_save'),
    path('staff_feedback', StaffViews.staff_feedback, name='staff_feedback'),
    path('staff_feedback_save', StaffViews.staff_feedback_save, name='staff_feedback_save'),
    path('staff_notification', StaffViews.staff_notification, name='staff_notification'),
    path(
        'staff_notification_mark_read/<int:notification_id>',
        StaffViews.staff_notification_mark_read,
        name='staff_notification_mark_read',
    ),
    path(
        'staff_notification_mark_all_read',
        StaffViews.staff_notification_mark_all_read,
        name='staff_notification_mark_all_read',
    ),

    # Student
    path('student_home', StudentViews.student_home, name='student_home'),
    path('student_apply_leave', StudentViews.student_apply_leave, name='student_apply_leave'),
    path('student_apply_leave_save', StudentViews.student_apply_leave_save, name='student_apply_leave_save'),
    path('student_feedback', StudentViews.student_feedback, name='student_feedback'),
    path('student_feedback_save', StudentViews.student_feedback_save, name='student_feedback_save'),
    path('student_notification', StudentViews.student_notification, name='student_notification'),
    path(
        'student_notification_mark_read/<int:notification_id>',
        StudentViews.student_notification_mark_read,
        name='student_notification_mark_read',
    ),
    path(
        'student_notification_mark_all_read',
        StudentViews.student_notification_mark_all_read,
        name='student_notification_mark_all_read',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)




