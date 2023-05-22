# Generated by Django 4.0 on 2023-04-12 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_alter_product_prouduct_identifier_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='dimension_type',
            field=models.CharField(blank=True, choices=[('centimeters', 'centimeters'), ('inches', 'inches')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='net_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='original_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='package_heigth',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='package_length',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='package_width',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='prouduct_identifier_type',
            field=models.CharField(blank=True, choices=[('EAN', 'EAN'), ('ASIN', 'ASIN'), ('GCID', 'GCID'), ('UPC', 'UPC'), ('ISBN', 'ISBN')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='publish_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('kilograms', 'kilograms'), ('Oz', 'Oz'), ('pounds', 'pounds')], max_length=255, null=True),
        ),
    ]
