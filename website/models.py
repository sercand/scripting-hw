from django.db import models

class Design(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    data = models.TextField()