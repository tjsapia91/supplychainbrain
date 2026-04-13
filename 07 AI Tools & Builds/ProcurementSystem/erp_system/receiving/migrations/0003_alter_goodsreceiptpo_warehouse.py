# Generated manually

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receiving', '0002_grpolineitem_description_destination'),
        ('vendors', '0002_branch_threeplprovider_alter_vendor_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsreceiptpo',
            name='warehouse',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='vendors.threeplprovider',
                verbose_name='Receiving 3PL',
            ),
        ),
    ]
