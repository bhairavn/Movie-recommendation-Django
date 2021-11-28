from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from time import timezone
# from django.core.mail import send_mail

class UserProfile(models.Model):
	firstname = models.CharField(max_length=10)
	lastname = models.CharField( max_length=10)
	phone = models.CharField(max_length=15)
	gender = models.CharField( max_length=8)
	genre = models.CharField( max_length=100)
	email = models.EmailField()
	password = models.CharField(max_length=20)    
	class Meta:
		db_table = "user"


# class CustomUserManager(BaseUserManager):
	
#     def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         now = timezone.now()
        
#         if not email:
#             raise ValueError('The given email must be set')
        
#         email = self.normalize_email(email)
#         # user = self.model(email=email,
#         #                   is_staff=is_staff, is_active=True,
#         #                   is_superuser=is_superuser,date_joined=now, **extra_fields)
#         user=self.model(email=email,**extra_fields)
#         user.set_password(password)
        
#         user.save(using=self._db)
#         return user

#     def create_user(self, email, password=None, **extra_fields):
#         return self._create_user(email, password, False, False, **extra_fields)

#     def create_superuser(self, email, password, **extra_fields):
#         return self._create_user(email, password, True, True, **extra_fields)
    	
# 	# class Meta:
# 	# 	db_table = "user"

# class CustomUser(AbstractBaseUser):
# 	firstname = models.CharField(max_length=100)
# 	lastname = models.CharField( max_length=100)
# 	phone = models.CharField(max_length=150)
# 	gender = models.CharField( max_length=20)
# 	genre = models.CharField( max_length=100)
# 	email = models.EmailField(unique=True)
# 	# passw = models.CharField(max_length=20)  

# 	# date_joined  = models.DateTimeField(('date joined'), default=timezone.now)
# 	is_active    = models.BooleanField(default=True)
# 	is_admin     = models.BooleanField(default=False)
# 	is_staff     = models.BooleanField(default=False)
# 	is_superuser = models.BooleanField(default=False)
    
# 	USERNAME_FIELD = 'email'
# 	REQUIRED_FIELDS = ['email','firstname', 'lastname', 'phone', 'gender','genre']

# 	objects = CustomUserManager()
    
# 	class Meta:
# 		verbose_name = 'user'
# 		verbose_name_plural = 'users'
# 		db_table = "user"    
  
# 	def get_absolute_url(self):
# 		return "/users/%s/" % urlquote(self.email)
		
# 	def get_full_name(self):
# 		"""
# 		Returns the first_name plus the last_name, with a space in between.
# 		"""
# 		full_name = '%s %s' % (self.firstname, self.lastname)
# 		return full_name.strip()
		
# 	def get_short_name(self):
# 		"Returns the short name for the user."
# 		return self.firstname

# 	def email_user(self, subject, message, from_email=None):
# 		"""
# 		Sends an email to this User.
# 		"""
# 		send_mail(subject, message, from_email, [self.email])  


	# USERNAME_FIELD='email'
	
	# REQUIRED_FIELDS=[]
 
	# def get_full_name(self):
    #  	return self.email
    
    # def get_short_name(self):
	# 	return self.email
    # def get_full_name(self):
	# 	return self.email
    # @property
    # def is_staff(self):
	# 	return self.staff
    # @property
    # def is_admin(self):
    # 	return self.admin
    # @property
	# def is_active(self):
	# 	return self.active