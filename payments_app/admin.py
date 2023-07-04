from django.contrib import admin

from payments_app.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_paid', 'prev_order')
    search_fields = ('id', 'user__tgid')
    readonly_fields = ('is_paid', 'created_at', 'updated_at')
