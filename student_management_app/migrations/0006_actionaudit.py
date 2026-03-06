from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0005_alter_navigationconfig_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionAudit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                (
                    'action_type',
                    models.CharField(
                        choices=[
                            ('feedback_reply_student', 'Respuesta feedback estudiante'),
                            ('feedback_reply_staff', 'Respuesta feedback personal'),
                            ('leave_approve_student', 'Aprobar permiso estudiante'),
                            ('leave_reject_student', 'Rechazar permiso estudiante'),
                            ('leave_approve_staff', 'Aprobar permiso personal'),
                            ('leave_reject_staff', 'Rechazar permiso personal'),
                        ],
                        max_length=64,
                    ),
                ),
                ('target_type', models.CharField(blank=True, default='', max_length=64)),
                ('target_id', models.CharField(blank=True, default='', max_length=64)),
                ('description', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'actor',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='action_audits',
                        to='student_management_app.customuser',
                    ),
                ),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddIndex(
            model_name='actionaudit',
            index=models.Index(fields=['action_type'], name='student_man_action__06924f_idx'),
        ),
        migrations.AddIndex(
            model_name='actionaudit',
            index=models.Index(fields=['created_at'], name='student_man_created_72f57f_idx'),
        ),
    ]
