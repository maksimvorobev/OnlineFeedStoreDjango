from django.contrib import admin
from users.models import User
from carts.admin import CartTabAdmin
from orders.admin import OrderTabulareAdmin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email",]
    search_fields = ["username", "first_name", "last_name", "email",]

    inlines = [CartTabAdmin, OrderTabulareAdmin]
