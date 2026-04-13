from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('containers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('bol', 'Bill of Lading'), ('signed_bol', 'Signed Bill of Lading'), ('packing_list', 'Packing List'), ('commercial_invoice', 'Commercial Invoice'), ('customs_entry', 'Customs Entry'), ('other', 'Other')], max_length=25)),
                ('file', models.FileField(upload_to='shipping_documents/')),
                ('description', models.CharField(blank=True, max_length=300)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('sync_status', models.CharField(choices=[('not_synced', 'Not Synced'), ('synced', 'Synced'), ('failed', 'Failed')], default='not_synced', max_length=15)),
                ('sync_error', models.TextField(blank=True, default='')),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_documents', to='containers.containerplan')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
