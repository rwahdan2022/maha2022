# Generated by Django 4.0 on 2022-03-08 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_alter_order_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
