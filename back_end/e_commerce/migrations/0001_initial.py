# Generated by Django 4.2.8 on 2023-12-15 23:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('username', models.CharField(max_length=255)),
                ('bio', models.CharField(blank=True, max_length=255)),
                ('is_verified', models.BooleanField(default=False)),
                ('items_count', models.IntegerField(default=0)),
                ('cash', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('up_votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('in_stock', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(to='e_commerce.items')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_wishlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Up_votes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_up_votes', to='e_commerce.comments')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_up_votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5)])),
                ('item', models.ManyToManyField(to='e_commerce.items')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='item',
            field=models.ManyToManyField(to='e_commerce.items'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('item', models.ManyToManyField(to='e_commerce.items')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('items_count', models.IntegerField(default=0)),
                ('items', models.ManyToManyField(to='e_commerce.items')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
