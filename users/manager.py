from django.db import models
from django.db.models import Q

class UserProfileManager(models.Manager):

    def get_active_profiles(self):
        user = self.filter(user__is_active=True)
        return user
    
    def get_user_profile(self,user):
        profile = self.get(user=user)
        return profile
    
    def search_profile(self,query):
        profile = self.filter(
            Q(bio__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
        return profile

    