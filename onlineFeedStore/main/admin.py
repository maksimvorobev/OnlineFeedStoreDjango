from django.contrib import admin

from main.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["first_name", "email", "ip_address", "time_create"]
    readonly_fields = ["time_create"]
