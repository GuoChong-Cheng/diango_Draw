# Generated by Django 4.2.4 on 2023-08-08 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_rename_professer_profe"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="profe",
            new_name="cgc",
        ),
        migrations.RenameField(
            model_name="cgc",
            old_name="age",
            new_name="ages",
        ),
        migrations.RenameField(
            model_name="cgc",
            old_name="name",
            new_name="names",
        ),
        migrations.RenameField(
            model_name="cgc",
            old_name="password",
            new_name="passwords",
        ),
    ]
