from django.db.models.signals import post_save
from django.dispatch import receiver

# @receiver(post_save, sender=TestSignalsInsert)
# def handle_save(sender, instance, created, **kwargs):
#     if created:
#         test_signal = TestSignals(signal_text=instance)
#         test_signal.save()
