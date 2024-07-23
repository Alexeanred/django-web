from django.contrib import admin

# Register your models here.

from .models import ChatMessage

admin.site.register(ChatMessage)

from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'amount', 'payment_date', 'has_paid')
    list_filter = ('has_paid', 'payment_date')
    search_fields = ('email', 'user__username')
    fields = ('user', 'email', 'amount', 'payment_date', 'has_paid')

admin.site.register(Payment, PaymentAdmin)
