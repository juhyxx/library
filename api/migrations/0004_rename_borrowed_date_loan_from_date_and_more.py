# Generated by Django 5.1.4 on 2024-12-05 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_book_active_libuser_active"),
    ]

    operations = [
        migrations.RenameField(
            model_name="loan",
            old_name="borrowed_date",
            new_name="from_date",
        ),
        migrations.RenameField(
            model_name="loan",
            old_name="return_date",
            new_name="to_date",
        ),
    ]
