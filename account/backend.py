from django.conf import settings
from django.contrib.auth.backends  import BaseBackend
from django.contrib.auth.hashers import check_password
# from django.contrib.auth.models import User
from .models import User


class Backend(BaseBackend):
	def authenticate(self, email=None, password=None):
		try:
			user = User.objects.get(email=email)
		except:
			return None

		if getattr(user, 'is_active') and user.check_password(password):
			return user
		return None


	def get_user(self, email):
		try:
			return User.objects.get(pk=email)
		except:
			return None



