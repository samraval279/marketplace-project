# Generated by Django 4.0 on 2023-04-10 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_product_prouduct_identifier_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('used', 'used'), ('new', 'new')], default='new', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='prouduct_identifier_type',
            field=models.CharField(blank=True, choices=[('ISBN', 'ISBN'), ('ASIN', 'ASIN'), ('EAN', 'EAN'), ('UPC', 'UPC'), ('GCID', 'GCID')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('pounds', 'pounds'), ('kilograms', 'kilograms'), ('Oz', 'Oz')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to='account.user'),
        ),
    ]
