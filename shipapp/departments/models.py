#Author: Debojit Kaushik ( 7th April 2017 )

from django.db import models
import uuid

#Database model for Departmenst. 
class Department(models.Model):
    dept_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    name = models.CharField(
        max_length = 300,
        null = False, 
        blank = False
    )


    class Meta:
        verbose_name = 'Departments'
        verbose_name_plural = 'Departments'
        db_table = 'Departments'


    def __str__(self):
        return '%s  id:%s' %(self.name , self.dept_id)