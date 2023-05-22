# Generated by Django 4.0 on 2023-04-10 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_servicerequest_alter_product_dimension_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prouduct_identifier_type',
            field=models.CharField(blank=True, choices=[('UPC', 'UPC'), ('EAN', 'EAN'), ('ISBN', 'ISBN'), ('GCID', 'GCID'), ('ASIN', 'ASIN')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('kilograms', 'kilograms'), ('Oz', 'Oz'), ('pounds', 'pounds')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='productspecification',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='account.product'),
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='account.product')),
            ],
            options={
                'db_table': 'product_attribute',
            },
        ),
    ]
