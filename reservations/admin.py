from django.contrib import admin
from reservations.models import TennisCourt, Reservations, Profile


class TennisCourtsAdmin(admin.ModelAdmin):
    ordering = ("id",)
    list_display = ('id', 'city', 'open_hour', 'close_hour', 'hire_price',)
    list_display_links = ('id',)
    list_per_page = 20
    list_filter = ('city',)
    search_fields = ('city',)


class ReservationsAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = (
        'id',
        'reservation_date',
        'court',
        'reservation_start',
        'reservation_end',
        # 'reservation_cost',
    )
    list_display_links = ('id',)
    list_per_page = 20
    list_filter = ('reservation_date',)
    search_fields = ('court',)
    # fieldsets = [
    #     ("General", {"fields": ["id"], "description": "Id info"}
    #      ),
    # ]
    # readonly_fields = ["id"]


admin.site.register(Reservations, ReservationsAdmin)
admin.site.register(TennisCourt, TennisCourtsAdmin)
admin.site.register(Profile)

