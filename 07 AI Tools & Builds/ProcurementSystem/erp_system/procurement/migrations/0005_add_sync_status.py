from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0004_plannedpurchaseorder_ceo_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='proformainvoice',
            name='sync_status',
            field=models.CharField(choices=[('not_synced', 'Not Synced'), ('synced', 'Synced'), ('failed', 'Failed')], default='not_synced', max_length=15),
        ),
        migrations.AddField(
            model_name='proformainvoice',
            name='sync_error',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ppoattachment',
            name='sync_status',
            field=models.CharField(choices=[('not_synced', 'Not Synced'), ('synced', 'Synced'), ('failed', 'Failed')], default='not_synced', max_length=15),
        ),
        migrations.AddField(
            model_name='ppoattachment',
            name='sync_error',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
