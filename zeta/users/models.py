from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User, unique=True, related_name = "profile")
	mobile_number = models.CharField(max_length=10)
	pin = models.CharField(max_length=4)
	points = models.IntegerField(default = 0)

	def __unicode__(self):
		return self.user.username

	def save(self, *args, **kwargs):
		if self.pk is None:
			pin_length = 4
			self.pin = User.objects.make_random_password(length = pin_length)
		return super(Profile, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.user.delete()
		return super(Profile, self).delete(*args, **kwargs)

class Transcation(models.Model):
	user = models.ForeignKey(User)
	amount = models.IntegerField()
	created = models.DateTimeField(auto_now_add=True)