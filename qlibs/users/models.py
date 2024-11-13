from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile_photo = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
       managed = False  # Prevent migrations for this model
       db_table = 'users'

    def __str__(self):
        return self.name
