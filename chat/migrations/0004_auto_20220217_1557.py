# Generated by Django 2.2.9 on 2022-02-17 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20220217_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='upload',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
