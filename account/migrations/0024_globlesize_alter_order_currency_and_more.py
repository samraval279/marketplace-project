# Generated by Django 4.0 on 2023-04-19 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0023_alter_order_currency_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobleSize',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=255)),
                ('subcategory', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(max_length=255)),
                ('details', models.CharField(blank=True, max_length=255, null=True)),
                ('size', models.JSONField()),
            ],
            options={
                'db_table': 'globle_size',
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='currency',
            field=models.CharField(blank=True, choices=[('BGN', 'BGN'), ('SLE', 'SLE'), ('OMR', 'OMR'), ('GTQ', 'GTQ'), ('CNY', 'CNY'), ('XAF', 'XAF'), ('RON', 'RON'), ('LTL', 'LTL'), ('LAK', 'LAK'), ('AED', 'AED'), ('ANG', 'ANG'), ('UYU', 'UYU'), ('DJF', 'DJF'), ('MKD', 'MKD'), ('BIF', 'BIF'), ('DOP', 'DOP'), ('PGK', 'PGK'), ('BRL', 'BRL'), ('MYR', 'MYR'), ('AWG', 'AWG'), ('TWD', 'TWD'), ('EGP', 'EGP'), ('MWK', 'MWK'), ('MAD', 'MAD'), ('BTN', 'BTN'), ('HUF', 'HUF'), ('INR', 'INR'), ('MOP', 'MOP'), ('ETB', 'ETB'), ('DKK', 'DKK'), ('RUB', 'RUB'), ('SRD', 'SRD'), ('YER', 'YER'), ('BZD', 'BZD'), ('TND', 'TND'), ('KYD', 'KYD'), ('GHS', 'GHS'), ('SEK', 'SEK'), ('BDT', 'BDT'), ('KGS', 'KGS'), ('PYG', 'PYG'), ('ISK', 'ISK'), ('CLP', 'CLP'), ('NIO', 'NIO'), ('PAB', 'PAB'), ('PEN', 'PEN'), ('NOK', 'NOK'), ('PLN', 'PLN'), ('ZMW', 'ZMW'), ('GEL', 'GEL'), ('RWF', 'RWF'), ('ARS', 'ARS'), ('MXN', 'MXN'), ('CRC', 'CRC'), ('WST', 'WST'), ('MZN', 'MZN'), ('NAD', 'NAD'), ('LSL', 'LSL'), ('TRY', 'TRY'), ('LBP', 'LBP'), ('SCR', 'SCR'), ('ZAR', 'ZAR'), ('JPY', 'JPY'), ('ALL', 'ALL'), ('FKP', 'FKP'), ('CAD', 'CAD'), ('AUD', 'AUD'), ('AZN', 'AZN'), ('VUV', 'VUV'), ('KZT', 'KZT'), ('USD', 'USD'), ('CZK', 'CZK'), ('CDF', 'CDF'), ('CHF', 'CHF'), ('SVC', 'SVC'), ('PHP', 'PHP'), ('XPF', 'XPF'), ('KES', 'KES'), ('SGD', 'SGD'), ('ILS', 'ILS'), ('SZL', 'SZL'), ('AMD', 'AMD'), ('EEK', 'EEK'), ('HNL', 'HNL'), ('THB', 'THB'), ('GMD', 'GMD'), ('IDR', 'IDR'), ('HTG', 'HTG'), ('AFN', 'AFN'), ('STD', 'STD'), ('LVL', 'LVL'), ('BHD', 'BHD'), ('DZD', 'DZD'), ('UGX', 'UGX'), ('SOS', 'SOS'), ('NPR', 'NPR'), ('MUR', 'MUR'), ('BYN', 'BYN'), ('TZS', 'TZS'), ('NGN', 'NGN'), ('SBD', 'SBD'), ('NZD', 'NZD'), ('BMD', 'BMD'), ('RSD', 'RSD'), ('LKR', 'LKR'), ('UZS', 'UZS'), ('VND', 'VND'), ('CVE', 'CVE'), ('BWP', 'BWP'), ('UAH', 'UAH'), ('QAR', 'QAR'), ('XCD', 'XCD'), ('GYD', 'GYD'), ('GIP', 'GIP'), ('TOP', 'TOP'), ('BAM', 'BAM'), ('AOA', 'AOA'), ('MMK', 'MMK'), ('BND', 'BND'), ('VEF', 'VEF'), ('SLL', 'SLL'), ('PKR', 'PKR'), ('FJD', 'FJD'), ('JOD', 'JOD'), ('EUR', 'EUR'), ('JMD', 'JMD'), ('KHR', 'KHR'), ('MVR', 'MVR'), ('MGA', 'MGA'), ('USDC', 'USDC'), ('XOF', 'XOF'), ('LRD', 'LRD'), ('HRK', 'HRK'), ('MNT', 'MNT'), ('GNF', 'GNF'), ('TJS', 'TJS'), ('SAR', 'SAR'), ('COP', 'COP'), ('MDL', 'MDL'), ('KWD', 'KWD'), ('BOB', 'BOB'), ('TTD', 'TTD'), ('KRW', 'KRW'), ('BBD', 'BBD'), ('KMF', 'KMF'), ('HKD', 'HKD'), ('GBP', 'GBP'), ('SHP', 'SHP'), ('BSD', 'BSD'), ('MRO', 'MRO')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='dimension_type',
            field=models.CharField(blank=True, choices=[('centimeters', 'centimeters'), ('inches', 'inches')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='prouduct_identifier_type',
            field=models.CharField(blank=True, choices=[('GCID', 'GCID'), ('ASIN', 'ASIN'), ('EAN', 'EAN'), ('UPC', 'UPC'), ('ISBN', 'ISBN')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('Oz', 'Oz'), ('pounds', 'pounds'), ('kilograms', 'kilograms')], max_length=255, null=True),
        ),
    ]
