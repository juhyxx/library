# Generated by Django 5.1.4 on 2024-12-05 21:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="libuser",
            old_name="username",
            new_name="name",
        ),
        migrations.AlterField(
            model_name="libuser",
            name="email",
            field=models.EmailField(max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name="Loan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("borrowed_date", models.DateField(blank=True, null=True)),
                ("return_date", models.DateField(blank=True, null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.book"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.libuser"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Libload",
        ),
    ]
