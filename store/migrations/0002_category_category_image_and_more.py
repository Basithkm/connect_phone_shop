# Generated by Django 4.2.2 on 2023-06-21 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_image',
            field=models.ImageField(default='1', upload_to='photos/category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sub_category',
            name='sub_category_image',
            field=models.ImageField(default='1', upload_to='photos/sub_category'),
            preserve_default=False,
        ),
    ]