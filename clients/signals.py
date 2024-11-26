# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import IndividualClient, CorporateClient, ClientList

# # Signals for IndividualClient
# @receiver(post_save, sender=IndividualClient)
# def create_or_update_client_list_individual(sender, instance, created, **kwargs):
#     if created:
#         ClientList.objects.create(client_name=f"{instance.first_name} {instance.surname}", legacy_id=instance.legacy_id, client_type='I')
#     else:
#         if instance.client_list_entry:
#             instance.client_list_entry.client_name = f"{instance.first_name} {instance.surname}"
#             instance.client_list_entry.save()

# # Signals for CorporateClient
# @receiver(post_save, sender=CorporateClient)
# def create_or_update_client_list_corporate(sender, instance, created, **kwargs):
#     if created:
#         ClientList.objects.create(client_name=instance.registered_name, legacy_id=instance.legacy_id, client_type='C')
#     else:
#         if instance.client_list_entry:
#             instance.client_list_entry.client_name = instance.registered_name
#             instance.client_list_entry.legacy_id = instance.legacy_id
#             instance.client_list_entry.save()
