# Generated by Django 4.2.2 on 2023-07-07 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0012_alter_uploadedfile_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='year_published',
            field=models.PositiveIntegerField(default=2023),
        ),
    ]
