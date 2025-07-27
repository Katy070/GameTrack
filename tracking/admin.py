from django.contrib import admin
from .models import TimePlayed

@admin.register(TimePlayed)
class TimePlayedAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'total_minutes', 'total_hours')

    def total_hours(self, obj):
        return obj.total_hours()
