# Generated by Django 5.0.6 on 2024-10-09 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('russiancities', '0005_city_moderarated'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
        ),
    ]
