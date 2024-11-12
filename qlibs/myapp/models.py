from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'users'  # Specify the actual table name in PostgreSQL
        managed = False     # Prevent Django from creating/migrating this table
