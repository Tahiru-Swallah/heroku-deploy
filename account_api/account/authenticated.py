from django.contrib.auth.backends import ModelBackend
from .models import CustomUser
from django.db.models import Q

User = CustomUser

class EmailorPhonenumber(ModelBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        try:
            user = User.objects.get(Q(email=username) | Q(phone_number=username))

        except User.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None