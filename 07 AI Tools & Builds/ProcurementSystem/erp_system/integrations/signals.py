"""
Post-save signal handlers that automatically sync uploaded files to OneDrive.
Each handler runs inline (try -> catch -> mark pending on failure).
"""
import logging
import os

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


def _read_file_content(file_field):
    """Read content from a Django FileField."""
    file_field.open('rb')
    content = file_field.read()
    file_field.close()
    return content


@receiver(post_save, sender='procurement.PPOAttachment')
def sync_ppo_attachment_to_onedrive(sender, instance, created, **kwargs):
    """Sync newly created PPO attachments to OneDrive."""
    if not created:
        return
    if not instance.file:
        return
    try:
        from integrations.onedrive import sync_ppo_attachment, is_connected
        if not is_connected():
            return
        ppo_number = instance.ppo.ppo_number
        filename = os.path.basename(instance.file.name)
        # Prefix with file type for clarity
        type_label = instance.get_file_type_display().replace(' ', '_')
        prefixed = f'{type_label}_{filename}'
        content = _read_file_content(instance.file)
        sync_ppo_attachment(ppo_number, prefixed, content)
        sender.objects.filter(pk=instance.pk).update(sync_status='synced', sync_error='')
        logger.info(f'Synced PPOAttachment {instance.pk} to OneDrive')
    except Exception as e:
        logger.warning(f'OneDrive sync failed for PPOAttachment {instance.pk}: {e}')
        sender.objects.filter(pk=instance.pk).update(
            sync_status='failed',
            sync_error=str(e)[:500]
        )


@receiver(post_save, sender='procurement.ProformaInvoice')
def sync_proforma_invoice_to_onedrive(sender, instance, created, **kwargs):
    """Sync newly created proforma invoices to OneDrive."""
    if not created:
        return
    if not instance.file:
        return
    try:
        from integrations.onedrive import sync_proforma_invoice, is_connected
        if not is_connected():
            return
        ppo_number = instance.ppo.ppo_number
        filename = os.path.basename(instance.file.name)
        prefixed = f'PI_{instance.pi_number}_{filename}'
        content = _read_file_content(instance.file)
        sync_proforma_invoice(ppo_number, prefixed, content)
        sender.objects.filter(pk=instance.pk).update(sync_status='synced', sync_error='')
        logger.info(f'Synced ProformaInvoice {instance.pk} to OneDrive')
    except Exception as e:
        logger.warning(f'OneDrive sync failed for ProformaInvoice {instance.pk}: {e}')
        sender.objects.filter(pk=instance.pk).update(
            sync_status='failed',
            sync_error=str(e)[:500]
        )


@receiver(post_save, sender='containers.ShippingDocument')
def sync_shipping_doc_to_onedrive(sender, instance, created, **kwargs):
    """Sync newly created shipping documents to OneDrive."""
    if not created:
        return
    if not instance.file:
        return
    try:
        from integrations.onedrive import sync_shipping_doc, is_connected
        if not is_connected():
            return
        container_name = instance.container.container_number or instance.container.plan_number
        doc_type = instance.get_document_type_display().replace(' ', '_')
        filename = os.path.basename(instance.file.name)
        content = _read_file_content(instance.file)
        sync_shipping_doc(container_name, doc_type, filename, content)
        sender.objects.filter(pk=instance.pk).update(sync_status='synced', sync_error='')
        logger.info(f'Synced ShippingDocument {instance.pk} to OneDrive')
    except Exception as e:
        logger.warning(f'OneDrive sync failed for ShippingDocument {instance.pk}: {e}')
        sender.objects.filter(pk=instance.pk).update(
            sync_status='failed',
            sync_error=str(e)[:500]
        )
