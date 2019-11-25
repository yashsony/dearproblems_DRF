# Generated by Django 2.1.7 on 2019-08-20 13:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('post', '0007_auto_20190808_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to=post.models.profile_directory_path55)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('group', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='group_for_profile', to='auth.Group')),
            ],
        ),
    ]
