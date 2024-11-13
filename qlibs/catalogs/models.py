from django.db import models

class Catalog(models.Model):
    # Match the existing catalog table columns
    id = models.IntegerField(primary_key=True)
    pdf_file = models.CharField(max_length=255)
    image_folder_path = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    released_year = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.IntegerField()  # Assuming user_id in catalog is an integer

    class Meta:
        managed = False  # Prevent migrations for this model
        db_table = 'catalog'  # Specify the existing table name

    def __str__(self):
        return self.title


class Favorited(models.Model):
    # Match the existing favorited table columns
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    catalog_id = models.IntegerField()

    class Meta:
        managed = False  # Prevent migrations for this model
        db_table = 'favorited'  # Specify the existing table name

    def __str__(self):
        return f"User {self.user_id} favorited Catalog {self.catalog_id}"