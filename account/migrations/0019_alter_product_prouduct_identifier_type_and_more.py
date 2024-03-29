# Generated by Django 4.0 on 2023-04-12 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_rename_labdmark_address_landmark_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prouduct_identifier_type',
            field=models.CharField(blank=True, choices=[('ISBN', 'ISBN'), ('EAN', 'EAN'), ('ASIN', 'ASIN'), ('UPC', 'UPC'), ('GCID', 'GCID')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('pounds', 'pounds'), ('kilograms', 'kilograms'), ('Oz', 'Oz')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
