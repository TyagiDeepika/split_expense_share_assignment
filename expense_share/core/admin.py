from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Expense, Balance


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('mobile_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('mobile_number',)}),
    )
    list_display = ('username', 'email', 'mobile_number', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'mobile_number')


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('payer', 'amount', 'description', 'split_type', 'date')
    search_fields = ('payer__username', 'description')
    list_filter = ('split_type', 'date')


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'amount')
    search_fields = ('from_user__username', 'to_user__username')
    list_filter = ('from_user', 'to_user')




# Register the models with the custom admin classes
admin.site.register(User, CustomUserAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Balance, BalanceAdmin)
