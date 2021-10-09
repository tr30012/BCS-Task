# Generated by Django 3.2.8 on 2021-10-08 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=64)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('value', models.DecimalField(decimal_places=10, max_digits=16)),
                ('description', models.TextField()),
            ],
        ),
    ]