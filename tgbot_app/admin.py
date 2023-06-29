from django.contrib import admin

from .models import AviaCity, AviaCountry, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('tgid', 'username')


@admin.register(AviaCountry)
class AviaCountryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'priority')
    list_editable = ('priority', )
    search_fields = ('title', )


@admin.register(AviaCity)
class AviaCityAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'priority')
    list_editable = ('priority',)
    search_fields = ('title',)
