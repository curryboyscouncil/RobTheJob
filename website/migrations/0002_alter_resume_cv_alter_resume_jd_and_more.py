# Generated by Django 5.0.7 on 2024-07-11 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='cv',
            field=models.TextField(max_length=15000),
        ),
        migrations.AlterField(
            model_name='resume',
            name='jd',
            field=models.TextField(max_length=15000),
        ),
        migrations.AlterField(
            model_name='resume',
            name='resume_text',
            field=models.TextField(max_length=15000),
        ),
    ]