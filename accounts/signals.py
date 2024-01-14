# signals are used to perform some task after the model is saved
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        
    else:
        # see is User is created / delete 
        try:
        # User updated the profile
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # Create the UserProfile if not existed
            UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
