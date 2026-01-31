from django.contrib.auth.models import BaseUserManager


############ ---- Notepad Summary: Password Logic ---- #################
# 💥 password=None: Just a placeholder in the function to prevent errors if a password isn't passed immediately.
# 💥 set_password(): The "Workhorse." It hashes the string and saves it to the password field in the DB.
# 💥 Social Auth (allauth): When you sign up via GitHub, allauth calls create_user but doesn't provide a password. Django sets it to an unusable "None" hash, keeping the account secure.
# 💥 Security Rule: Never save the password directly like user.password = password. Always use set_password().
#########################################################################


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        
        # set-default syntax in Python dictionaries #
        
        # The setdefault() method is a handy dictionary tool that handles the "look before you leap" logic for you. It essentially checks if a key exists; if it does, it returns the value, and if it doesn't, it inserts the key with a specified value.
        
        extra_fields.setdefault('is_staff', True) # Don't set TRUE if explicitly mentioned FALSE in the function call.
        extra_fields.setdefault('is_superuser', True) # Don't set TRUE if explicitly mentioned FALSE in the function call.

        # Logic to check if is_staff and is_superuser are True #
        # Because a superuser must have both these fields set to True. #
        # Basically, the create_superuser function should not be misused to create a non-superuser (Normal User). #
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)