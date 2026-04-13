# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receiving', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='grpolineitem',
            name='description',
            field=models.CharField(blank=True, default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grpolineitem',
            name='destination',
            field=models.CharField(blank=True, default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='grpolineitem',
            name='quantity_received',
            field=models.IntegerField(default=0),
        ),
    ]
