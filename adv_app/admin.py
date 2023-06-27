from django.contrib import admin

from adv_app.models import Adv, AdvButton, AdvPhoto


@admin.register(Adv)
class AdvAdmin(admin.ModelAdmin):
    filter_horizontal = ('photos', 'buttons')
    list_display = ('title', 'enabled', 'time_exec')


@admin.register(AdvPhoto)
class AdvPhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(AdvButton)
class AdvButtonAdmin(admin.ModelAdmin):
    pass

