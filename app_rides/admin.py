from django.contrib import admin
from .models import Ride


# Register your models here.
@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'rider', 'driver', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('rider__username', 'driver__user__username')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('rider', 'driver')