
#Author: Debojit Kaushik ( 7th April 2017 )

'''Django Imports'''
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

'''Model Imports'''
from departments.models import Department



#Database model for Users.
class User(AbstractUser):
    '''
        Abstract user model inherited containing all basic fields such as:
        first and last name, username, email, password etc. Refer to doc for Abstract User fields. 
    '''
    user_id = models.UUIDField(
        primary_key = True, 
        default = uuid.uuid4, 
        editable = False
    )
    department = models.ForeignKey(
        Department, 
        related_name = 'officials',
        null = True
    )

    employee_SAP = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    class Meta:
        managed = True
        db_table = 'Users'
    


    def __str__(self):
        label = self.constructLabel(
            self.first_name, 
            self.last_name,
            self.user_id
        )
        return '%s' % label


    #Constructing a label for admin panel. Format : John Doe ( id: 0123456789 )
    def constructLabel(self, first_name = '' , last_name = '', id = None):
        try:
            assert id is not None
            if first_name is '' and last_name is '':
                return '%s' %id
            else:
                return '%s %s (id: %s)' %(first_name, last_name, id) 
        except Exception as err:
            return "Error fetching label."