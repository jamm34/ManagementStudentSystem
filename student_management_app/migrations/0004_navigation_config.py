from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0003_notification_is_read'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavigationConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('1', 'HOD'), ('2', 'Staff'), ('3', 'Student')], max_length=10, unique=True)),
                ('brand', models.CharField(blank=True, default='', max_length=100)),
                ('home_url_name', models.CharField(blank=True, default='', max_length=100)),
                ('menu_json', models.TextField(help_text='JSON valido con la estructura de menu por rol')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
