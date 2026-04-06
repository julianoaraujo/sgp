from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'perfil', 'setor', 'ativo', 'data_criacao']
    list_filter = ['perfil', 'ativo', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'matricula']
    ordering = ['-data_criacao']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('perfil', 'setor', 'telefone', 'matricula', 'ativo')
        }),
    )
