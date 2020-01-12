from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier for authentication instead of usernames.
    """
    def create_user(self, email, password=None):
        """
        Create and save a User with the given email,level and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))

        user = self.model(
            email=self.normalize_email(email),
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Create and save a Superuser with the given email, level and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user