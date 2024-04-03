from django.contrib import admin
from . models import Category,Listing,User,Comment
# Register your models here.
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Comment)