from .models import Tour
from django.contrib import admin
from .models.TourOrganizer import TourOrganizer
from .models.Tour import Tour
# Register your models here.


class TourOrganizerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'evaluation',
                    'joined_at', 'situation')
    list_filter = ('joined_at', 'situation', 'address')


class TourAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'starting_place', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'starting_place')


admin.site.register(TourOrganizer, TourOrganizerAdmin)
admin.site.register(Tour, TourAdmin)
