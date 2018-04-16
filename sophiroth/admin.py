from django.contrib import admin
from sophiroth.models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email']
    search_fields = ['user']


class AccountAdmin(admin.ModelAdmin):
    list_display = ['application','username','password','comment']
    search_fields = ['application','username']

admin.site.register(User,UserAdmin)
admin.site.register(Account,AccountAdmin)