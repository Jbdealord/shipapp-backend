from django.contrib import admin
from .models import Issue, Solution, Image
# Register your models here.

admin.site.register(Image)
admin.site.register(Issue)
admin.site.register(Solution)
