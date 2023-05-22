# Generated by Django 4.0 on 2023-04-10 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_product_dimension_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('topic', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=255)),
                ('message', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'service_request',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='dimension_type',
            field=models.CharField(blank=True, choices=[('centimeters', 'centimeters'), ('inches', 'inches')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='prouduct_identifier_type',
            field=models.CharField(blank=True, choices=[('GCID', 'GCID'), ('UPC', 'UPC'), ('ISBN', 'ISBN'), ('ASIN', 'ASIN'), ('EAN', 'EAN')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('pounds', 'pounds'), ('Oz', 'Oz'), ('kilograms', 'kilograms')], max_length=255, null=True),
        ),
    ]
