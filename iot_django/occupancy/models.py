from django.db import models

# Create your models here.
class Boundry(models.Model):
    value = models.FloatField()

class MotionScore(models.Model):
    value = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)