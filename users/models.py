# from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.template.defaultfilters import default
from django.conf import settings
from sorl.thumbnail import ImageField

class UserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		
		user = self.model(email=self.normalize_email(email),)
		user.is_active = True
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		user = self.create_user(email=email, password=password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser, PermissionsMixin):
	FEMALE = 'f'
	MALE = 'm'
	OTHER = 'o'
	UNKNOWN = 'u'
	GENDER_CHOICES = (
		(FEMALE, 'female'),
		(MALE, 'male'),
		(OTHER, 'other'),
		(UNKNOWN, 'unknown'),
	)
	### Redefine the basic fields that would normally be defined in User ###
	email = models.EmailField(verbose_name='email address', unique=True, max_length=255)
	first_name = models.CharField(max_length=30, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True, null=False)
	is_staff = models.BooleanField(default=False, null=False)

	### Our own fields ###
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=UNKNOWN)
	date_of_birth = models.DateField(null=False, blank=False)
	profile_image = ImageField(upload_to=settings.UPLOAD_ROOT, blank=False, null=False, default="defaultuserimage.png")
	location = models.PointField(null=True)

	objects = UserManager()
	geo = models.GeoManager()
	
	USERNAME_FIELD = 'email'
	
	def get_full_name(self):
		fullname = self.first_name + " " + self.last_name
		return fullname

	def get_short_name(self):
		return self.email
	
	'''def create_thumbnail(self):
		# original code for this method came from
		# http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

		# If there is no image associated with this.
		# do not create thumbnail
		if not self.profile_image:
			return

		from PIL import Image
		from io import BytesIO
		from django.core.files.uploadedfile import SimpleUploadedFile
		import os

		# Set our max thumbnail size in a tuple (max width, max height)
		THUMBNAIL_SIZE = (300, 300)

		DJANGO_TYPE = None		
		try:
			DJANGO_TYPE = self.profile_image.file.content_type
		except:
			return
		
		if DJANGO_TYPE == 'image/jpeg':
			PIL_TYPE = 'jpeg'
			FILE_EXTENSION = 'jpg'
		elif DJANGO_TYPE == 'image/png':
			PIL_TYPE = 'png'
			FILE_EXTENSION = 'png'
			
		# Open original photo which we want to thumbnail using PIL's Image
		r = BytesIO(self.profile_image.read())  # Using BytesIO instead of StringIO
		fullsize_image = Image.open(r)
		image = fullsize_image.copy()

		# Convert to RGB if necessary
		# Thanks to Limodou on DjangoSnippets.org
        # http://www.djangosnippets.org/snippets/20/
		#
		# We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
		# Additionally, we use Image.ANTIALIAS to make the image look better.
		# Without antialiasing the image pattern artifacts may result.
		image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
		
		# Save the thumbnail
		temp_handle = BytesIO()
		image.save(temp_handle, PIL_TYPE)
		temp_handle.seek(0)


		# Save image to a SimpleUploadedFile which can be saved into
		# ImageField
		suf = SimpleUploadedFile(os.path.split(self.profile_image.name)[-1],
				 temp_handle.read(), content_type=DJANGO_TYPE)
		# Save SimpleUploadedFile into image field
		self.thumbnail.save('{}_thumbnail.{}'.format(os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)

	def save(self):
		# create a thumbnail
		self.create_thumbnail()

		super(User, self).save()'''

	def __str__(self):
		return self.email
		
