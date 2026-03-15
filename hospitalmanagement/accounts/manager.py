from django.contrib.auth.base_user import BaseUserManager
		
class UserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        if phone == None or password == None:
            raise ValueError("Username or password must have a value")
            
        # Emails lower case
        extra_fields["email"] = self.normalize_email(extra_fields["email"])
        
        # Set user as active
        extra_fields.setdefault('is_active', True)
        
        # Set user
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        
        return user
        
    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)	# Normal dict method(setdefault)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # Use create_user method for DRY
        return self.create_user(phone, password, **extra_fields)