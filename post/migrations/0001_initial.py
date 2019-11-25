# Generated by Django 2.1.7 on 2019-06-17 06:34

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import post.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aexperts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expert_name', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opinion_type', models.CharField(choices=[('S', 'Suggestion'), ('C', 'Comment')], max_length=1)),
                ('opinion', models.CharField(max_length=300)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('Notification_id', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('like_ratio', models.CharField(choices=[('N', 'Nice'), ('G', 'Good'), ('V', 'Very Good'), ('E', 'Excellent')], max_length=1)),
                ('Notification_id', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Mygroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group')),
                ('Admin_id', models.IntegerField(blank=True, null=True)),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('L', 'liked'), ('C', 'comment'), ('S', 'share'), ('F', 'follow')], max_length=1)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('Message_to_creater_for_share', models.BooleanField(default=False)),
                ('action_by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('notice_for_user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='notice_for_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField(max_length=500)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('edited_time', models.DateTimeField(auto_now=True)),
                ('photo', models.FileField(blank=True, null=True, upload_to=post.models.user_directory_path)),
                ('points', models.IntegerField(default=0)),
                ('ask_with_public', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_name', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('is_expert', 'expert'),),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to=post.models.profile_directory_path)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_name_for_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('group_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Mygroup')),
                ('requestor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='requestor_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('Notification_id', models.IntegerField(default=1)),
                ('post_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_name', to='post.Post')),
                ('share_by_user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='share_by_user', to=settings.AUTH_USER_MODEL)),
                ('share_to_group', models.ManyToManyField(blank=True, to='post.Mygroup')),
                ('share_to_user', models.ManyToManyField(blank=True, related_name='share_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='post_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='post.Post'),
        ),
        migrations.AddField(
            model_name='like',
            name='like_on_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Post'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='aexperts',
            name='post_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='post.Post'),
        ),
        migrations.AlterUniqueTogether(
            name='request',
            unique_together={('requestor', 'group_name')},
        ),
        migrations.AlterUniqueTogether(
            name='follower',
            unique_together={('follower', 'following')},
        ),
    ]
