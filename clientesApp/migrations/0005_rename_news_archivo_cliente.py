# Generated by Django 4.2 on 2023-12-27 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientesApp', '0004_rename_archivos_archivo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archivo',
            old_name='news',
            new_name='cliente',
        ),
    ]
