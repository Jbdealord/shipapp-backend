#Author: Debojit Kaushik (7th April 2017)

'''Django imports'''
from django.db import models
import uuid


'''Model Imports'''
from departments.models import Department
from users.models import User

#Database model fror Ships.
class Ship(models.Model):
    ship_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    name = models.CharField(
        max_length = 300,
        null = False, 
        blank = False
    )
    departments = models.ManyToManyField(
        Department,
        symmetrical = False, 
        related_name = 'ships'
    )
    owner = models.OneToOneField(
        User,
        related_name = 'ship',
        default = None
    )

    class Meta:
        verbose_name = 'Ships'
        verbose_name_plural = 'Ships'
        db_table = 'Ships'
    

    def __str__(self):
        return '%s id: %s' %(self.name, self.ship_id)