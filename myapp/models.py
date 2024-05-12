from django.db import models

class Directory(models.Model):
    address = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    services = models.TextField()

    def __str__(self):
        return self.name