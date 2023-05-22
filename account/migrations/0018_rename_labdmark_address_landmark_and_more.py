# Generated by Django 4.0 on 2023-04-12 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_remove_user_address_user_profile_picture_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='labdmark',
            new_name='landmark',
        ),
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('used', 'used'), ('new', 'new')], default='new', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='prouduct_identifier_type',
            field=models.CharField(blank=True, choices=[('EAN', 'EAN'), ('ASIN', 'ASIN'), ('UPC', 'UPC'), ('GCID', 'GCID'), ('ISBN', 'ISBN')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('Oz', 'Oz'), ('kilograms', 'kilograms'), ('pounds', 'pounds')], max_length=255, null=True),
        ),
    ]