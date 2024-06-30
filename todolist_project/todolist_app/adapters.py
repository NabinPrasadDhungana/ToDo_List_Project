from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount, SocialApp
from .models import CustomUser
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        path = "/"
        return path
    
    # def get_signup_redirect_url(self, request):
    #     return "/accounts/login/"

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        logger.debug("pre_social_login called")

        if sociallogin.is_existing:
            logger.debug("Existing social login")
            return

        email = sociallogin.account.extra_data.get('email', '').lower()
        if not email:
            logger.warning("No email address found in social login data")
            return

        try:
            user = CustomUser.objects.get(email=email)
            logger.info(f"Existing user found with email: {email}")

            social_accounts = SocialAccount.objects.filter(user=user, provider=sociallogin.account.provider)
            if social_accounts.exists():
                logger.warning(f"Multiple social accounts found for user: {user} and provider: {sociallogin.account.provider}")
                return

            sociallogin.connect(request, user)
            user.save()
        except CustomUser.DoesNotExist:
            logger.info(f"No existing user with email: {email}")
        except CustomUser.MultipleObjectsReturned:
            logger.error(f"Multiple users found with email: {email}")
        except SocialAccount.MultipleObjectsReturned:
            logger.error(f"Multiple social accounts found for email: {email} and provider: {sociallogin.account.provider}")

    def get_app(self, request, provider, client_id=None):
        logger.debug(f"Getting app for provider: {provider}")
        try:
            app = SocialApp.objects.get(provider=provider, sites__id=settings.SITE_ID)
            logger.debug(f"Found app: {app}")
            return app
        except SocialApp.MultipleObjectsReturned:
            logger.error(f"Multiple SocialApp entries found for provider: {provider} and site: {settings.SITE_ID}")
            raise
        except SocialApp.DoesNotExist:
            logger.error(f"No SocialApp entry found for provider: {provider} and site: {settings.SITE_ID}")
            raise