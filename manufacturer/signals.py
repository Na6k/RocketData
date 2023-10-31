from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee, Network


@receiver(post_save, sender=Employee)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance.user)


#@receiver(post_save, sender=Network)
#def attach_network_to_user(sender, instance, created, **kwargs):
#    if created and instance.user:
#        employee = Employee.objects.get(user=instance.employee_id)
#        if employee:
#            instance.employee_id = employee.id
#            instance.save()