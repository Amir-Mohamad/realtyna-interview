from django.contrib import admin
from .models import Listing, Reservation


class ReservationInline(admin.StackedInline):
    model = Reservation
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    inlines = [ReservationInline]
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'name', 'start_date', 'end_date')
    search_fields = ('name', 'listing__name')
    list_filter = ('listing', 'start_date')