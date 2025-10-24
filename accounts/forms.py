from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import (
    validate_password,
    password_validators_help_text_html,
)
from django.core.exceptions import ValidationError

from .models import Funcionario

User = get_user_model()


class FuncionarioForm(forms.ModelForm):
    """Form for Funcionario model"""
    
    class Meta:
        model = Funcionario
        fields = [
            'nome', 'rg', 'cpf', 'email', 'cargo', 'nivel_acesso',
            'telefone', 'celular', 'cep', 'endereco', 'numero',
            'complemento', 'bairro', 'cidade', 'estado'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '000.000.000-00'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'nivel_acesso': forms.Select(
                choices=[
                    ('Administrador', 'Administrador'),
                    ('Usuario', 'Usuário'),
                ],
                attrs={'class': 'form-select'}
            ),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '(00) 0000-0000'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '(00) 00000-0000'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'id': 'cep', 'data-mask': '00000-000'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'id': 'endereco'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'id': 'bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'id': 'cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'id': 'estado', 'maxlength': '2'}),
        }


class FuncionarioSearchForm(forms.Form):
    """Search form for employees"""
    search = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome, CPF ou E-mail...'
        })
    )


class FuncionarioCreateForm(FuncionarioForm):
    """Form used to register a new employee and issue user credentials."""

    username = forms.CharField(
        label='Nome de Usuário',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'As senhas informadas não conferem.')
            return cleaned_data

        if password1:
            user_for_validation = User(
                username=cleaned_data.get('username') or '',
                email=cleaned_data.get('email') or ''
            )
            try:
                validate_password(password1, user_for_validation)
            except ValidationError as exc:
                self.add_error('password1', exc)

        return cleaned_data

    def save(self, commit=True):
        funcionario = super().save(commit=False)
        username = self.cleaned_data['username']
        password = self.cleaned_data['password1']

        user = User(
            username=username,
            email=funcionario.email,
            first_name=funcionario.nome,
            is_staff=funcionario.nivel_acesso == 'Administrador',
            is_active=True,
        )
        user.set_password(password)

        if commit:
            user.save()
            funcionario.user = user
            funcionario.save()
        else:
            funcionario.user = user

        return funcionario


class FuncionarioUpdateForm(FuncionarioForm):
    """Form used to maintain employee data and linked user account."""

    username = forms.CharField(
        label='Nome de Usuário',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.instance, 'user', None)
        if user:
            self.fields['username'].initial = user.username

    def clean_username(self):
        username = self.cleaned_data['username']
        user = getattr(self.instance, 'user', None)
        existing = User.objects.filter(username=username)
        if user:
            existing = existing.exclude(pk=user.pk)
        if existing.exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username

    def save(self, commit=True):
        funcionario = super().save(commit=False)
        username = self.cleaned_data['username']

        user = getattr(funcionario, 'user', None)
        generated_password = None

        if user is None:
            generated_password = User.objects.make_random_password(length=12)
            user = User(
                username=username,
                email=funcionario.email,
                first_name=funcionario.nome,
                is_staff=funcionario.nivel_acesso == 'Administrador',
                is_active=True,
            )
            user.set_password(generated_password)
        else:
            user.username = username
            user.email = funcionario.email
            user.first_name = funcionario.nome
            user.is_staff = funcionario.nivel_acesso == 'Administrador'

        if commit:
            user.save()
            funcionario.user = user
            funcionario.save()
        else:
            funcionario.user = user

        self.generated_password = generated_password
        return funcionario
