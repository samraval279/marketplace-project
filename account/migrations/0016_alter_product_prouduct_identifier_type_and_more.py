# Generated by Django 4.0 on 2023-04-12 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_alter_product_condition_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prouduct_identifier_type',
            field=models.CharField(blank=True, choices=[('GCID', 'GCID'), ('ISBN', 'ISBN'), ('UPC', 'UPC'), ('EAN', 'EAN'), ('ASIN', 'ASIN')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('kilograms', 'kilograms'), ('pounds', 'pounds'), ('Oz', 'Oz')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='grade',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
    ]
