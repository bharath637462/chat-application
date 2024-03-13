import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from core.mixins.models import BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    GENDERS = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))

    first_name = models.CharField(_('First Name'), max_length=255, db_index=True)
    middle_name = models.CharField(_('Middle Name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('Last Name'), max_length=255, null=True)
    email = models.EmailField(_('Email'), unique=True, db_index=True)
    phone = models.CharField(_('Phone'), db_index=True, blank=True, null=True, max_length=13)

    # Personal
    gender = models.CharField(_('Gender'), choices=GENDERS, max_length=10, blank=True, null=True)
    photo = models.ImageField(_('Photo'), upload_to='user', blank=True, null=True)
    dob = models.DateField(_('DOB'), null=True, blank=True)

    is_staff = models.BooleanField(verbose_name=_('Is staff user?'), default=False)
    is_superuser = models.BooleanField(verbose_name=_('Is superuser?'), default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def profile(self):
        profile = Profile.objects.get(user=self)

    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('-created_at',)


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000)
    bio = models.CharField(max_length=100)
    image = models.ImageField(upload_to="user_images", default="default.jpg")
    verified = models.BooleanField(default=False)

    def create_user_profile(self, sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def save_user_profile(self, sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
        ordering = ('created_at',)
        verbose_name_plural = _("Profiles")
        db_table = 'Profile'


class ChatMessage(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')

    message = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('created_at',)
        verbose_name_plural = "Message"

    def __str__(self):
        return f"{self.sender} - {self.receiver}"

    @property
    def sender_profile(self):
        sender_profile = Profile.objects.get(user=self.sender)
        return sender_profile

    @property
    def receiver_profile(self):
        receiver_profile = Profile.objects.get(user=self.receiver)
        return receiver_profile
