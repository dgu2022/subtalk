from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_id, password, **extra_fields):
        if not user_id:
            raise ValueError('ID를 입력해주세요.')
        user_id = self.model.normalize_username(user_id)
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_user(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_id, password,  **extra_fields)

    def create_superuser(self, user_id, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff=True일 필요가 있습니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser=True일 필요가 있습니다.')
        return self._create_user(user_id, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    #username_validator = UnicodeUsernameValidator()

    user_id = models.CharField(_("user id"), max_length=20, blank=False, unique=True)
    #, validators=[username_validator]
    password = models.CharField(_("password"), max_length=20, blank=False)
    #패스워드 정보는 db에 기록하지 않는다. 유저 생성에서 set_password로 암호화된 내용으로 바꾸기 때문.
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    sex = models.CharField(_("sex"),max_length=20,blank=False)
    age = models.IntegerField(_("age"),blank=False)
    topic = models.CharField(_("topic"),max_length=200, blank=True)
    job = models.CharField(_("job"),max_length=50, blank=True)

    objects = UserManager()
    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ['password']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")