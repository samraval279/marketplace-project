# Generated by Django 4.0 on 2023-04-11 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_product_condition_alter_product_dimension_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='dimension_type',
            field=models.CharField(blank=True, choices=[('centimeters', 'centimeters'), ('inches', 'inches')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='prouduct_identifier_type',
            field=models.CharField(blank=True, choices=[('EAN', 'EAN'), ('UPC', 'UPC'), ('ASIN', 'ASIN'), ('ISBN', 'ISBN'), ('GCID', 'GCID')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('kilograms', 'kilograms'), ('pounds', 'pounds'), ('Oz', 'Oz')], max_length=255, null=True),
        ),
    ]