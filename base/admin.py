from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(TranslationRequest)
admin.site.register(TextToSpeechRequest)
admin.site.register(SpeechToTextRequest)
admin.site.register(SavedPhrase)