# Generated by Django 4.0 on 2023-04-20 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_globlesize_alter_order_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='currency',
            field=models.CharField(blank=True, choices=[('MVR', 'MVR'), ('UAH', 'UAH'), ('RUB', 'RUB'), ('GTQ', 'GTQ'), ('CVE', 'CVE'), ('BIF', 'BIF'), ('SGD', 'SGD'), ('COP', 'COP'), ('ETB', 'ETB'), ('YER', 'YER'), ('AMD', 'AMD'), ('HKD', 'HKD'), ('BAM', 'BAM'), ('SVC', 'SVC'), ('CLP', 'CLP'), ('TTD', 'TTD'), ('HRK', 'HRK'), ('KGS', 'KGS'), ('BTN', 'BTN'), ('INR', 'INR'), ('UZS', 'UZS'), ('PEN', 'PEN'), ('BSD', 'BSD'), ('VUV', 'VUV'), ('NZD', 'NZD'), ('LSL', 'LSL'), ('DOP', 'DOP'), ('XAF', 'XAF'), ('OMR', 'OMR'), ('MDL', 'MDL'), ('ALL', 'ALL'), ('EGP', 'EGP'), ('TRY', 'TRY'), ('ILS', 'ILS'), ('UYU', 'UYU'), ('SLE', 'SLE'), ('TOP', 'TOP'), ('KMF', 'KMF'), ('SBD', 'SBD'), ('SHP', 'SHP'), ('GIP', 'GIP'), ('JOD', 'JOD'), ('MNT', 'MNT'), ('CDF', 'CDF'), ('GYD', 'GYD'), ('CNY', 'CNY'), ('CRC', 'CRC'), ('JPY', 'JPY'), ('VEF', 'VEF'), ('SRD', 'SRD'), ('MUR', 'MUR'), ('HTG', 'HTG'), ('SOS', 'SOS'), ('SAR', 'SAR'), ('ZMW', 'ZMW'), ('VND', 'VND'), ('GMD', 'GMD'), ('NIO', 'NIO'), ('GHS', 'GHS'), ('NGN', 'NGN'), ('AFN', 'AFN'), ('CHF', 'CHF'), ('AED', 'AED'), ('QAR', 'QAR'), ('EEK', 'EEK'), ('XOF', 'XOF'), ('BHD', 'BHD'), ('PLN', 'PLN'), ('MYR', 'MYR'), ('FKP', 'FKP'), ('BMD', 'BMD'), ('BND', 'BND'), ('TJS', 'TJS'), ('MGA', 'MGA'), ('ARS', 'ARS'), ('BGN', 'BGN'), ('NPR', 'NPR'), ('IDR', 'IDR'), ('BRL', 'BRL'), ('PAB', 'PAB'), ('PHP', 'PHP'), ('MOP', 'MOP'), ('LRD', 'LRD'), ('AWG', 'AWG'), ('TZS', 'TZS'), ('DJF', 'DJF'), ('MRO', 'MRO'), ('HNL', 'HNL'), ('SZL', 'SZL'), ('KRW', 'KRW'), ('MWK', 'MWK'), ('WST', 'WST'), ('HUF', 'HUF'), ('LBP', 'LBP'), ('RON', 'RON'), ('GBP', 'GBP'), ('MKD', 'MKD'), ('AUD', 'AUD'), ('JMD', 'JMD'), ('NAD', 'NAD'), ('USDC', 'USDC'), ('KWD', 'KWD'), ('XCD', 'XCD'), ('BYN', 'BYN'), ('EUR', 'EUR'), ('DKK', 'DKK'), ('BDT', 'BDT'), ('GEL', 'GEL'), ('SLL', 'SLL'), ('PKR', 'PKR'), ('AOA', 'AOA'), ('KZT', 'KZT'), ('TWD', 'TWD'), ('BZD', 'BZD'), ('KES', 'KES'), ('BOB', 'BOB'), ('BWP', 'BWP'), ('TND', 'TND'), ('LKR', 'LKR'), ('LAK', 'LAK'), ('DZD', 'DZD'), ('SEK', 'SEK'), ('XPF', 'XPF'), ('USD', 'USD'), ('PGK', 'PGK'), ('GNF', 'GNF'), ('ANG', 'ANG'), ('MZN', 'MZN'), ('LTL', 'LTL'), ('PYG', 'PYG'), ('THB', 'THB'), ('NOK', 'NOK'), ('RSD', 'RSD'), ('LVL', 'LVL'), ('ZAR', 'ZAR'), ('BBD', 'BBD'), ('UGX', 'UGX'), ('FJD', 'FJD'), ('ISK', 'ISK'), ('MMK', 'MMK'), ('RWF', 'RWF'), ('MAD', 'MAD'), ('MXN', 'MXN'), ('CAD', 'CAD'), ('CZK', 'CZK'), ('KYD', 'KYD'), ('KHR', 'KHR'), ('SCR', 'SCR'), ('AZN', 'AZN'), ('STD', 'STD')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('new', 'new'), ('used', 'used')], default='new', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='dimension_type',
            field=models.CharField(blank=True, choices=[('inches', 'inches'), ('centimeters', 'centimeters')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='prouduct_identifier_type',
            field=models.CharField(blank=True, choices=[('UPC', 'UPC'), ('GCID', 'GCID'), ('ISBN', 'ISBN'), ('ASIN', 'ASIN'), ('EAN', 'EAN')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('pounds', 'pounds'), ('Oz', 'Oz'), ('kilograms', 'kilograms')], max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='SiteReview',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('grade', models.DecimalField(decimal_places=1, max_digits=4)),
                ('title', models.CharField(max_length=255)),
                ('review', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_site_reviews', to='account.user')),
            ],
            options={
                'db_table': 'site_review',
            },
        ),
    ]
