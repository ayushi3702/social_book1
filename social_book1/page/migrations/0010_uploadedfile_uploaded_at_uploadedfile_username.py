# Generated by Django 4.2.2 on 2023-07-06 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0009_alter_customuser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='username',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
