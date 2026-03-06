from django.db import migrations


def assign_audit_permission_to_hod(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    CustomUser = apps.get_model('student_management_app', 'CustomUser')

    try:
        content_type = ContentType.objects.get(
            app_label='student_management_app',
            model='actionaudit',
        )
        permission = Permission.objects.get(
            content_type=content_type,
            codename='view_actionaudit',
        )
    except (ContentType.DoesNotExist, Permission.DoesNotExist):
        return

    hod_group, _ = Group.objects.get_or_create(name='HOD')
    hod_group.permissions.add(permission)

    for user in CustomUser.objects.filter(user_type='1'):
        user.groups.add(hod_group)


def rollback_audit_permission_from_hod(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    try:
        hod_group = Group.objects.get(name='HOD')
        content_type = ContentType.objects.get(
            app_label='student_management_app',
            model='actionaudit',
        )
        permission = Permission.objects.get(
            content_type=content_type,
            codename='view_actionaudit',
        )
    except (Group.DoesNotExist, ContentType.DoesNotExist, Permission.DoesNotExist):
        return

    hod_group.permissions.remove(permission)


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0007_alter_navigationconfig_menu_json'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(
            assign_audit_permission_to_hod,
            rollback_audit_permission_from_hod,
        ),
    ]
