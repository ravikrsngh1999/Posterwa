# Generated by Django 3.2.9 on 2021-11-29 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_product_out_of_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='couponname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_receipt',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='razorpay_order_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='razorpay_payment_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='razorpay_signature',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_charges',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='subtotal',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.CharField(max_length=50),
        ),
    ]