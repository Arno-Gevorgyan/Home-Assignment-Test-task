from django.contrib import admin
from .models import ExpressionHistory


@admin.register(ExpressionHistory)
class ExpressionHistoryAdmin(admin.ModelAdmin):
    list_display = ('expression', 'result', 'status', 'created_at', 'evaluated_at')
    list_filter = ('status', 'created_at', 'evaluated_at')
    search_fields = ('expression', 'result')

    fieldsets = (
        (None, {
            'fields': ('expression', 'result', 'status')
        }),
        ('Date Information', {
            'fields': ('evaluated_at',),
            'classes': ('collapse',),
        }),
    )
