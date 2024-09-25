from django.db import models

from etica_y_valores.base.models import BaseModel
from etica_y_valores.enterprises.models import EnterpriseModel

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group


class UserLevelCategory(BaseModel):

    user_level = models.CharField(max_length=30, null=False, blank=False)

    class Meta:
        app_label = 'users'
        verbose_name = 'User Level Category'
        verbose_name_plural = 'User Level Categories'

    def __repr__(self):
        return f'UserLevelCategory(id={self.id}, user_level={self.user_level}, created_at={self.created_at}, updated_at={self.updated_at})'

    def __str__(self):
        return f'{self.user_level}'


class UserManager(BaseUserManager):

    def create_user(self, first_name, middle_name, last_name, username, password, email, is_staff, is_active, is_superuser=False):
        user = self.model(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, middle_name, last_name, username, password, email):
        return self.create_user(first_name, middle_name, last_name, username, password, email, True, True, True)


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    This model define an user

    Attributes:
        email (str): email of the user
        username (str): username of the user
        created_at (datetime): creation date
    """

    class Meta:
        app_label = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(name='user_id_idx', fields=['id']),
        ]

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name', 'email']

    objects = UserManager()
    first_name = models.CharField(max_length=50, null=False, blank=False)
    middle_name = models.CharField(max_length=50, null=False, blank=False,)
    last_name = models.CharField(max_length=50, null=False, blank=False,)
    username = models.CharField(
        unique=True, max_length=20, null=False, blank=False,)
    email = models.EmailField(unique=True, null=False, blank=False,)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_level_id = models.ForeignKey(
        UserLevelCategory, null=True, blank=True, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordinates',)
    enterprise_id = models.ForeignKey(EnterpriseModel, null=True, blank=True,
                                      related_name='user_enterprise', on_delete=models.DO_NOTHING)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",
        related_query_name="custom_user",
    )

    def __str__(self):
        return self.username

    def __repr__(self):
        return (f'UserModel('
                f'id={self.id}, '
                f'first_name={self.first_name}, '
                f'middle_name={self.middle_name}, '
                f'last_name={self.last_name}, '
                f'username={self.username}, '
                f'email={self.email}, '
                f'is_staff={self.is_staff}, '
                f'is_active={self.is_active}, '
                f'user_level_id={self.user_level_id}, '
                f'enterprise_id={self.enterprise_id}, '
                f'created_at={self.created_at}, '
                f'updated_at={self.updated_at})')
