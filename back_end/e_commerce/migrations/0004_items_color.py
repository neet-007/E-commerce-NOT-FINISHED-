# Generated by Django 4.2.8 on 2024-01-10 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0003_alter_items_shoe_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='color',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]