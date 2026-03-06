import json

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from student_management_app.models import ActionAudit, CustomUser, NavigationConfig


class UserModel(UserAdmin):
    pass


class NavigationConfigAdminForm(forms.ModelForm):
    class Meta:
        model = NavigationConfig
        fields = '__all__'

    def clean_menu_json(self):
        value = self.cleaned_data.get('menu_json', '')
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise forms.ValidationError(f'JSON inválido: {exc}')

        if not isinstance(parsed, list):
            raise forms.ValidationError('menu_json debe ser una lista JSON de items.')

        return value


admin.site.register(CustomUser, UserModel)


@admin.register(NavigationConfig)
class NavigationConfigAdmin(admin.ModelAdmin):
    form = NavigationConfigAdminForm
    list_display = ('role', 'is_active', 'updated_at')
    list_filter = ('role', 'is_active')
    search_fields = ('role', 'brand', 'home_url_name')


@admin.register(ActionAudit)
class ActionAuditAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'action_type', 'actor', 'target_type', 'target_id')
    list_filter = ('action_type', 'created_at')
    search_fields = ('description', 'target_id', 'target_type', 'actor__username', 'actor__email')
    readonly_fields = ('created_at', 'action_type', 'actor', 'target_type', 'target_id', 'description')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
