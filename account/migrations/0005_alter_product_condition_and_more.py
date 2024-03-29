# Generated by Django 4.0 on 2023-04-06 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_product_condition_alter_product_dimension_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('new', 'new'), ('used', 'used')], default='new', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='prouduct_identifier_type',
            field=models.CharField(blank=True, choices=[('GCID', 'GCID'), ('ASIN', 'ASIN'), ('ISBN', 'ISBN'), ('EAN', 'EAN'), ('UPC', 'UPC')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('Oz', 'Oz'), ('pounds', 'pounds'), ('kilograms', 'kilograms')], max_length=255, null=True),
        ),
    ]
