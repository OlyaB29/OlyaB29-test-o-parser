# Generated by Django 4.2.4 on 2023-08-04 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ozon_products', '0003_products_code_alter_products_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='link',
            field=models.CharField(max_length=600, unique=True, verbose_name='Ссылка'),
        ),
    ]
