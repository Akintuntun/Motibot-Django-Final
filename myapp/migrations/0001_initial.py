# Generated by Django 4.2.10 on 2024-05-11 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('contact_info', models.CharField(max_length=255)),
                ('services', models.TextField()),
            ],
        ),
    ]
