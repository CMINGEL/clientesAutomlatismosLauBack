# Generated by Django 4.2 on 2024-01-31 15:29

import clientesApp.models
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ejecutivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('activo', models.BooleanField(default=True)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoServicio', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('numeroContacto', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('tipoContrato', models.CharField(blank=True, max_length=50, null=True)),
                ('fechaInicioContrato', models.DateTimeField(blank=True, null=True)),
                ('fechaFinContrato', models.DateTimeField(blank=True, null=True)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('ejecutivoCierre', models.CharField(blank=True, max_length=50, null=True)),
                ('ejecutivoActual', models.CharField(blank=True, max_length=50, null=True)),
                ('desistido', models.BooleanField(default=False)),
                ('servicios', models.ManyToManyField(to='clientesApp.servicio')),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
            },
        ),
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_content', models.FileField(blank=True, null=True, upload_to=clientesApp.models.user_directory_path)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clientesApp.cliente')),
            ],
            options={
                'verbose_name': 'archivo',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
