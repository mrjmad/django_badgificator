from django.contrib import admin


from models import DataPresence, HitViewByUser, Badge, UserBadge

admin.site.register(DataPresence)
admin.site.register(HitViewByUser)
admin.site.register(Badge)
admin.site.register(UserBadge)
