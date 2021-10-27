from django.db import models

# Create your models here.
class Author(models.Model):
    one_to_one_relation = models.OneToOneField('User')