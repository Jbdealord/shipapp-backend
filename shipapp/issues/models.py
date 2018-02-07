# Author: Debojit Kaushik ( 7th April 2017 )

from django.db import models
from ships.models import Ship
from departments.models import Department
from users.models import User

import uuid


# Database model for Issues.
class Issue(models.Model):

    '''
        Class for Issue containing relations with the following models:
        Department: FK,
        ship: FK,
        solution:FK,
        User:FK
    '''

    ISSUE_STATUSES = (
        ('unassigned','Unassigned'),
        ('pending','Pending'),
        ('submitted','Submitted'),
        ('resolved','Resolved'),
    )

    PRIORITY_LIST = (
        ('unassigned','Unassigned'),
        ('very_low','Very Low'),
        ('low','Low'),
        ('moderate','Moderate'),
        ('high','High'),
        ('very_high','Very High'),
    )

    iss_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    issue_text = models.TextField(
        blank = False
    )
    department = models.ForeignKey(
        Department,
        related_name = 'issues',
        null = True
    )
    status = models.CharField(
        max_length = 50,
        choices = ISSUE_STATUSES,
        default = 'unassigned'
    )
    priority = models.CharField(
        max_length = 20,
        choices = PRIORITY_LIST,
        default = 'unassigned'
    )
    ship = models.ForeignKey(
        Ship,
        related_name = 'issues',
        null = True
    )
    deck_no = models.CharField(
        max_length = 100,
        blank = False
    )
    compartment = models.CharField(
        max_length = 200
    )
    recorded_by = models.ForeignKey(
        User,
        related_name = 'issues_raised',
        null = True
    )
    reported_by = models.CharField(
        max_length = 200,
        blank = True
    )
    resolved_by = models.ForeignKey(
        User,
        related_name = 'issues_resolved',
        null = True,
        blank = True
    )
    created_time = models.DateTimeField(
        auto_now = True
    )
    updated_time = models.DateTimeField(
        auto_now_add = True
    )
    deleted = models.BooleanField(
        default = False
    )

    class Meta:
        verbose_name = 'Issues'
        verbose_name_plural = 'Issues'
        db_table = 'Issues'

    def __str__(self):
        return '%s ID: %s' %(self.issue_text,self.iss_id)


#Database model for posted Solutions.
class Solution(models.Model):
    '''
        Class for Solution to issues raised by workers.
        Relation with Issue model as a Foreign Key.
    '''
    sol_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    solution_text = models.TextField()
    created_time = models.DateTimeField(
        auto_now = True
    )
    updated_time = models.DateTimeField(
        auto_now_add = True
    )
    parent_issue = models.ForeignKey(
        Issue,
        related_name = 'solutions',
        null = True
    )
    poster = models.ForeignKey(
        User,
        related_name = 'solutions',
        null = True
    )
    deleted = models.BooleanField(
        default = False
    )

    class Meta:
        verbose_name = 'Solutions'
        db_table = 'Solutions'
        verbose_name_plural = 'Solutions'

    def __str__(self):
        return '%s' %(self.sol_id)





class Image(models.Model):
    '''
        Class for images stored against resolved issues or solutions.
        DB Relations:
        Issue: FK,
        Solution:FK
    '''


    img_id = models.UUIDField(
        primary_key =  True,
        default = uuid.uuid4,
        editable = False
    )
    parent_issue = models.ForeignKey(
        Issue,
        null = True,
        related_name = 'images'
    )
    parent_solution = models.ForeignKey(
        Solution,
        null = True,
        related_name = 'images'
    )
    image =  models.ImageField(
        upload_to = 'images/'
    )
    signature_of = models.OneToOneField(
        Issue,
        related_name = 'signature',
        null = True,
        blank = True
    )
    created_time = models.DateTimeField(
        auto_now = True
    )
    updated_time = models.DateTimeField(
        auto_now_add = True
    )
    deleted = models.BooleanField(
        default = False
    )

    class Meta:
        verbose_name = 'Images'
        db_table = 'Images'
        verbose_name_plural = 'Images'


    def __str__(self):
        return "%s" %self.img_id
 