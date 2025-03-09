from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)

    def update_user_password(self, user, new_password):
        user.set_password(new_password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True, db_index=True)
    first_name = models.CharField(_("first name"), max_length=255, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=255, blank=True, null=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_superuser = models.BooleanField(_("superuser status"), default=False)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    is_verified = models.BooleanField(_("verified"), default=False)
    verification_token = models.CharField(
        _("verification token"), max_length=64, blank=True, null=True
    )
    token_expiration = models.DateTimeField(_("token expiration"), blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def generate_verification_token(self):
        self.verification_token = get_random_string(length=64)
        self.token_expiration = timezone.now() + timezone.timedelta(days=1)
        self.save()


# Use signals to handle non-critical updates asynchronously
@receiver(post_save, sender=CustomUser)
def update_last_login(sender, instance, **kwargs):
    # Update last_login or perform other non-critical operations
    pass
