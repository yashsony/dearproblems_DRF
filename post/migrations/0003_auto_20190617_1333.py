# Generated by Django 2.1.7 on 2019-06-17 08:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0002_auto_20190617_1234'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='aexperts',
            unique_together={('post_name', 'expert_name')},
        ),
    ]