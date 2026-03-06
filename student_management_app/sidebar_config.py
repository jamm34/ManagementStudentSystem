"""Configuracion central del sidebar por rol.

Cada item puede definir:
- label, icon, url_name, active_prefixes
- badge_key, badge_class, show_zero
- permission: 'perm:app_label.codename' o 'role:<tipo>'
- permissions_all: lista de permisos/reglas requeridas
- permissions_any: lista de permisos/reglas, cumple con al menos uno
- children: lista de items
"""

SIDEBAR_CONFIG = {
    '1': {
        'brand': 'Gestion Academica',
        'home_url_name': 'admin_home',
        'menu': [
            {
                'label': 'Inicio',
                'icon': 'fas fa-home',
                'url_name': 'admin_home',
            },
            {
                'header': 'Modulos',
            },
            {
                'label': 'Gestion de personal',
                'icon': 'fas fa-user-tie',
                'children': [
                    {
                        'label': 'Agregar personal',
                        'icon': 'far fa-circle',
                        'url_name': 'add_staff',
                    },
                    {
                        'label': 'Gestionar personal',
                        'icon': 'far fa-circle',
                        'url_name': 'manage_staff',
                        'active_prefixes': ['/edit_staff/'],
                    },
                ],
            },
            {
                'label': 'Gestion de estudiantes',
                'icon': 'fas fa-user-graduate',
                'children': [
                    {
                        'label': 'Agregar estudiante',
                        'icon': 'far fa-circle',
                        'url_name': 'add_student',
                    },
                    {
                        'label': 'Gestionar estudiantes',
                        'icon': 'far fa-circle',
                        'url_name': 'manage_student',
                        'active_prefixes': ['/edit_student/'],
                    },
                ],
            },
            {
                'label': 'Cursos',
                'icon': 'fas fa-book-open',
                'children': [
                    {
                        'label': 'Agregar curso',
                        'icon': 'far fa-circle',
                        'url_name': 'add_course',
                    },
                    {
                        'label': 'Gestionar cursos',
                        'icon': 'far fa-circle',
                        'url_name': 'manage_course',
                        'active_prefixes': ['/edit_course/'],
                    },
                ],
            },
            {
                'label': 'Asignaturas',
                'icon': 'fas fa-chalkboard-teacher',
                'children': [
                    {
                        'label': 'Agregar asignatura',
                        'icon': 'far fa-circle',
                        'url_name': 'add_subject',
                    },
                    {
                        'label': 'Gestionar asignaturas',
                        'icon': 'far fa-circle',
                        'url_name': 'manage_subject',
                        'active_prefixes': ['/edit_subject/'],
                    },
                ],
            },
            {
                'label': 'Seguimiento',
                'icon': 'fas fa-clipboard-check',
                'children': [
                    {
                        'label': 'Ver asistencia',
                        'icon': 'far fa-circle',
                        'url_name': 'view_attendance_hod',
                        'badge_key': 'hod_attendance_today',
                        'badge_class': 'badge-info',
                    },
                    {
                        'label': 'Feedback estudiantes',
                        'icon': 'far fa-circle',
                        'url_name': 'student_feedback_message',
                        'badge_key': 'hod_student_feedback_pending',
                        'badge_class': 'badge-danger',
                    },
                    {
                        'label': 'Feedback personal',
                        'icon': 'far fa-circle',
                        'url_name': 'staff_feedback_message',
                        'badge_key': 'hod_staff_feedback_pending',
                        'badge_class': 'badge-danger',
                    },
                    {
                        'label': 'Permisos estudiantes',
                        'icon': 'far fa-circle',
                        'url_name': 'student_leave_view',
                        'badge_key': 'hod_student_leaves_pending',
                        'badge_class': 'badge-warning',
                    },
                    {
                        'label': 'Permisos personal',
                        'icon': 'far fa-circle',
                        'url_name': 'staff_leave_view',
                        'badge_key': 'hod_staff_leaves_pending',
                        'badge_class': 'badge-warning',
                    },
                    {
                        'label': 'Bitacora de acciones',
                        'icon': 'far fa-circle',
                        'url_name': 'audit_log',
                        'permission': 'perm:student_management_app.view_actionaudit',
                    },
                ],
            },
        ],
    },
    '2': {
        'brand': 'Panel de Personal',
        'home_url_name': 'staff_home',
        'menu': [
            {
                'label': 'Inicio',
                'icon': 'fas fa-home',
                'url_name': 'staff_home',
            },
            {
                'header': 'Gestion',
            },
            {
                'label': 'Mi seguimiento',
                'icon': 'fas fa-user-tie',
                'children': [
                    {
                        'label': 'Solicitar permiso',
                        'icon': 'far fa-circle',
                        'url_name': 'staff_apply_leave',
                        'badge_key': 'staff_my_leaves_pending',
                        'badge_class': 'badge-warning',
                    },
                    {
                        'label': 'Enviar feedback',
                        'icon': 'far fa-circle',
                        'url_name': 'staff_feedback',
                        'badge_key': 'staff_my_feedback_pending',
                        'badge_class': 'badge-danger',
                    },
                    {
                        'label': 'Notificaciones',
                        'icon': 'far fa-circle',
                        'url_name': 'staff_notification',
                        'badge_key': 'staff_notifications_unread',
                        'badge_class': 'badge-info',
                    },
                ],
            },
        ],
    },
    '3': {
        'brand': 'Panel de Estudiante',
        'home_url_name': 'student_home',
        'menu': [
            {
                'label': 'Inicio',
                'icon': 'fas fa-home',
                'url_name': 'student_home',
            },
            {
                'header': 'Gestion',
            },
            {
                'label': 'Mi seguimiento',
                'icon': 'fas fa-user-graduate',
                'children': [
                    {
                        'label': 'Solicitar permiso',
                        'icon': 'far fa-circle',
                        'url_name': 'student_apply_leave',
                        'badge_key': 'student_my_leaves_pending',
                        'badge_class': 'badge-warning',
                    },
                    {
                        'label': 'Enviar feedback',
                        'icon': 'far fa-circle',
                        'url_name': 'student_feedback',
                        'badge_key': 'student_my_feedback_pending',
                        'badge_class': 'badge-danger',
                    },
                    {
                        'label': 'Notificaciones',
                        'icon': 'far fa-circle',
                        'url_name': 'student_notification',
                        'badge_key': 'student_notifications_unread',
                        'badge_class': 'badge-info',
                    },
                ],
            },
        ],
    },
}
