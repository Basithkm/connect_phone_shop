# Generated by Django 4.2.2 on 2023-06-22 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_account_block_number_account_house_building_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='street_avenue_number',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='house_building_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
