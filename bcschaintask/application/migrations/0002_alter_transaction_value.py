# Generated by Django 3.2.8 on 2021-10-09 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='value',
            field=models.DecimalField(decimal_places=8, max_digits=16),
        ),
    ]