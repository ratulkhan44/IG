# Django Imports
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    """
        User model manager where email is the unique identifier
        for authentication instead of usernames.
    """
    def _create_user(self, email, password, mobile, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not mobile:
            raise ValueError("Users must have an mobile")
        
        user = self.model(
            email=self.normalize_email(email), 
            mobile=mobile,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, mobile=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(email, password, mobile, **extra_fields)
    
    
    
    def create_superuser(self, email, password, mobile = None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, mobile, **extra_fields)



# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
    """
        This is User Model 
    """
    username = models.CharField(
        verbose_name = _("username"),
        max_length = 150,
        unique = True,
        null = True,
        blank = True,
        error_messages = {
            "unique" : _("A user with that username already exists.")
        }
    )
    email = models.CharField(
        verbose_name = _("email address"),
        max_length = 255,
        unique = True,
        blank = False,
        error_messages = {
            "unique": _("A user with that email already exists.")
        }
    )
    mobile = models.CharField(
        verbose_name = _("contact no"),
        max_length = 20,
        blank = False
    )
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True,editable = False)
    updated_at = models.DateTimeField(auto_now = True,editable = False)
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile"]

    
    class Meta:
        ordering = ("-created_at",)
        
    def __str__(self) -> str:
        return str(self.email)
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


