from django.contrib import admin
from wanikani.models import WKUser,Sentence

# Register your models here.
admin.site.register(WKUser)
admin.site.register(Sentence)
