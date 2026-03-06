from django import forms

from student_management_app.models import Courses


class DateInput(forms.DateInput):
    input_type = 'date'


class AddStudentForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        max_length=50,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Contraseña',
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    first_name = forms.CharField(
        label='Nombre', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Apellido', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='Usuario', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label='Dirección', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    gender_choice = (
        ('Male', 'Masculino'),
        ('Female', 'Femenino'),
    )

    course = forms.ChoiceField(
        label='Curso', choices=[], widget=forms.Select(attrs={'class': 'form-control'})
    )
    sex = forms.ChoiceField(
        label='Sexo', choices=gender_choice, widget=forms.Select(attrs={'class': 'form-control'})
    )
    session_start = forms.DateField(
        label='Inicio de período', widget=DateInput(attrs={'class': 'form-control'})
    )
    session_end = forms.DateField(
        label='Fin de período', widget=DateInput(attrs={'class': 'form-control'})
    )
    profile_pic = forms.FileField(
        label='Foto de perfil',
        max_length=50,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].choices = [(c.id, c.course_name) for c in Courses.objects.all()]


class EditStudentForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        max_length=50,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    first_name = forms.CharField(
        label='Nombre', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Apellido', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='Usuario', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label='Dirección', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    gender_choice = (
        ('Male', 'Masculino'),
        ('Female', 'Femenino'),
    )

    course = forms.ChoiceField(
        label='Curso', choices=[], widget=forms.Select(attrs={'class': 'form-control'})
    )
    sex = forms.ChoiceField(
        label='Sexo', choices=gender_choice, widget=forms.Select(attrs={'class': 'form-control'})
    )
    session_start = forms.DateField(
        label='Inicio de período', widget=DateInput(attrs={'class': 'form-control'})
    )
    session_end = forms.DateField(
        label='Fin de período', widget=DateInput(attrs={'class': 'form-control'})
    )
    profile_pic = forms.FileField(
        label='Foto de perfil',
        max_length=50,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].choices = [(c.id, c.course_name) for c in Courses.objects.all()]
