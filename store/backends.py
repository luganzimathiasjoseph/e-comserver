from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from store.models import Business, Customer

User = get_user_model()

class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)

            if user.check_password(password):
                # Check if user is active and has appropriate proxy model
                if user.is_active and (Business.objects.filter(pk=user.pk).exists() or Customer.objects.filter(pk=user.pk).exists()):
                    return user
                else:
                    return None  # User does not have appropriate role or is not active
            else:
                return None  # Password incorrect
        except User.DoesNotExist:
            return None  # User does not exist
