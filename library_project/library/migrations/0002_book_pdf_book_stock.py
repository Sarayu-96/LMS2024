# Generated by Django 5.1.3 on 2024-12-08 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='book_pdfs/'),
        ),
        migrations.AddField(
            model_name='book',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
