from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import CustomUser

import logging

logger = logging.getLogger(__name__)

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        path = "/"
        return path

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Ensure email address is unique
        if sociallogin.is_existing:
            return
        
        # Fetch the email address
        email = sociallogin.account.extra_data.get('email', '').lower()
        if not email:
            return
        
        try:
            # Check if there is an existing user with this email address
            user = CustomUser.objects.get(email=email)
            sociallogin.connect(request, user)
            user.save()  # Ensure the user instance is saved
        except CustomUser.DoesNotExist:
            logger.info(f"No existing user with email: {email}")

