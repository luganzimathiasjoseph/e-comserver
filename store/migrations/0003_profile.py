# Generated by Django 5.0.3 on 2024-03-29 23:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_custompermission_user_custom_fields_for_business_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='profile_pics/default_pic.jpg', upload_to='profile_pics')),
                ('gender', models.CharField(default='', max_length=10)),
                ('contact', models.CharField(max_length=10)),
                ('telephone', models.CharField(max_length=10)),
                ('website', models.CharField(max_length=70)),
                ('business_name', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=50)),
                ('address_line_1', models.CharField(max_length=100)),
                ('address_line_2', models.CharField(max_length=100)),
                ('pobox', models.CharField(max_length=10)),
                ('street', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=10)),
                ('bio', models.CharField(blank=True, default='', max_length=400)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
