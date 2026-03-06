from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

from student_management_app.models import (
    Attendance,
    FeedBackStaffs,
    FeedBackStudent,
    LeaveReportStaff,
    LeaveReportStudent,
    NotificationStaffs,
    NotificationStudent,
    Staffs,
    Students,
)
from student_management_app.navigation_service import get_role_navigation_config


def _safe_reverse(name, fallback='#'):
    try:
        return reverse(name)
    except Exception:
        return fallback


def _is_active(path, url=None, prefixes=None):
    prefixes = prefixes or []
    if url and path == url:
        return True
    return any(path.startswith(prefix) for prefix in prefixes)


def _has_permission(user, permission):
    if not permission:
        return True

    if permission.startswith('perm:'):
        return user.has_perm(permission[5:])

    if permission.startswith('role:'):
        return str(getattr(user, 'user_type', '')) == permission[5:]

    return True


def _has_menu_access(user, item_cfg):
    if not _has_permission(user, item_cfg.get('permission')):
        return False

    permissions_all = item_cfg.get('permissions_all', [])
    if permissions_all and not all(_has_permission(user, perm) for perm in permissions_all):
        return False

    permissions_any = item_cfg.get('permissions_any', [])
    if permissions_any and not any(_has_permission(user, perm) for perm in permissions_any):
        return False

    return True


def _get_badge_counts(user):
    counts = {
        'hod_attendance_today': 0,
        'hod_student_feedback_pending': 0,
        'hod_staff_feedback_pending': 0,
        'hod_student_leaves_pending': 0,
        'hod_staff_leaves_pending': 0,
        'staff_my_leaves_pending': 0,
        'staff_my_feedback_pending': 0,
        'staff_notifications_unread': 0,
        'student_my_leaves_pending': 0,
        'student_my_feedback_pending': 0,
        'student_notifications_unread': 0,
    }

    user_type = str(getattr(user, 'user_type', ''))

    try:
        if user_type == '1':
            today = timezone.localdate()
            counts.update(
                {
                    'hod_attendance_today': Attendance.objects.filter(attendance_date__date=today).count(),
                    'hod_student_feedback_pending': FeedBackStudent.objects.filter(
                        Q(feedback_reply__isnull=True) | Q(feedback_reply='')
                    ).count(),
                    'hod_staff_feedback_pending': FeedBackStaffs.objects.filter(
                        Q(feedback_reply__isnull=True) | Q(feedback_reply='')
                    ).count(),
                    'hod_student_leaves_pending': LeaveReportStudent.objects.filter(
                        leave_approval_status=LeaveReportStudent.LEAVE_STATUS_PENDING
                    ).count(),
                    'hod_staff_leaves_pending': LeaveReportStaff.objects.filter(
                        leave_approval_status=LeaveReportStaff.LEAVE_STATUS_PENDING
                    ).count(),
                }
            )

        elif user_type == '2':
            staff = Staffs.objects.get(admin=user.id)
            counts.update(
                {
                    'staff_my_leaves_pending': LeaveReportStaff.objects.filter(
                        staff_id=staff,
                        leave_approval_status=LeaveReportStaff.LEAVE_STATUS_PENDING,
                    ).count(),
                    'staff_my_feedback_pending': FeedBackStaffs.objects.filter(staff_id=staff).filter(
                        Q(feedback_reply__isnull=True) | Q(feedback_reply='')
                    ).count(),
                    'staff_notifications_unread': NotificationStaffs.objects.filter(
                        staff_id=staff,
                        is_read=False,
                    ).count(),
                }
            )

        elif user_type == '3':
            student = Students.objects.get(admin=user.id)
            counts.update(
                {
                    'student_my_leaves_pending': LeaveReportStudent.objects.filter(
                        student_id=student,
                        leave_approval_status=LeaveReportStudent.LEAVE_STATUS_PENDING,
                    ).count(),
                    'student_my_feedback_pending': FeedBackStudent.objects.filter(student_id=student).filter(
                        Q(feedback_reply__isnull=True) | Q(feedback_reply='')
                    ).count(),
                    'student_notifications_unread': NotificationStudent.objects.filter(
                        student_id=student,
                        is_read=False,
                    ).count(),
                }
            )
    except Exception:
        return counts

    return counts


def _resolve_badge(item_cfg, badge_counts):
    badge_key = item_cfg.get('badge_key')
    if not badge_key:
        return None

    value = badge_counts.get(badge_key)
    if value is None:
        return None

    if value == 0 and not item_cfg.get('show_zero', False):
        return None

    return value


def _build_menu_item(item_cfg, path, badge_counts, user):
    if not _has_menu_access(user, item_cfg):
        return None

    children_cfg = item_cfg.get('children', [])
    built_children = []
    for child_cfg in children_cfg:
        child_item = _build_menu_item(child_cfg, path, badge_counts, user)
        if child_item is not None:
            built_children.append(child_item)

    if children_cfg and not built_children:
        return None

    url_name = item_cfg.get('url_name')
    url = _safe_reverse(url_name) if url_name else '#'
    active_prefixes = item_cfg.get('active_prefixes', [])

    is_active = _is_active(path, url=url, prefixes=active_prefixes)
    if built_children:
        is_active = is_active or any(child.get('active') for child in built_children)

    return {
        'label': item_cfg.get('label', ''),
        'icon': item_cfg.get('icon', 'far fa-circle'),
        'url': url,
        'active': is_active,
        'children': built_children,
        'menu_open': bool(built_children and is_active),
        'badge': _resolve_badge(item_cfg, badge_counts),
        'badge_class': item_cfg.get('badge_class', 'badge-info'),
    }


def _build_menu(role_config, path, badge_counts, user):
    menu = []
    for item_cfg in role_config.get('menu', []):
        if 'header' in item_cfg:
            menu.append({'header': item_cfg['header']})
            continue

        built_item = _build_menu_item(item_cfg, path, badge_counts, user)
        if built_item is not None:
            menu.append(built_item)

    return menu


def sidebar_navigation(request):
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return {}

    user_type = str(getattr(user, 'user_type', ''))
    role_config = get_role_navigation_config(user_type)
    if not role_config:
        return {}

    path = request.path
    badge_counts = _get_badge_counts(user)
    sidebar_menu = _build_menu(role_config, path, badge_counts, user)

    return {
        'sidebar_brand': role_config.get('brand', 'Panel'),
        'sidebar_home_url': _safe_reverse(role_config.get('home_url_name', ''), fallback='#'),
        'sidebar_menu': sidebar_menu,
    }
