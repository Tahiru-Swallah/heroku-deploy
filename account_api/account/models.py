from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
#from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('User should enter either email or phone number')
        if email:
            email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        Profile.objects.create(user=user)

        return user
    
    def create_superuser(self, email, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, phone_number, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(unique=True, max_length=20)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()
    
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set_perm',
        blank=True
    )

    def __str__(self):
        return self.email or str(self.phone_number)
    
    """ def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj =None):
        return True """
    
class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    profile_image = models.ImageField(upload_to="profile/%Y/%m/%d", null=True, blank=True)
    bio = models.CharField(max_length=50, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username 