# Generated by Django 5.1.3 on 2024-12-08 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_book_pdf_book_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='duration_months',
            new_name='duration_days',
        ),
        migrations.AddField(
            model_name='plan',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
