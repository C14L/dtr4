from django.contrib import admin

from dtrprofile.models_flag import UserFlag
from dtrprofile.models_usermsg import UserMsg
from dtrprofile.models_profile import UserProfile

admin.site.register(UserFlag)
admin.site.register(UserMsg)
admin.site.register(UserProfile)
