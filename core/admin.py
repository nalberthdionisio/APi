from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Recommendation)
admin.site.register(Procedure)
admin.site.register(Users)
admin.site.register(UserProcedure)