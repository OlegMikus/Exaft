# Generated by Django 3.2.4 on 2021-06-09 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210609_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topmanagers',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]