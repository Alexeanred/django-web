from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    name = models.CharField(max_length=100, default='New Chat')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat'

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Đổi tên created_at thành timestamp

    class Meta:
        db_table = 'chat_message'

    def __str__(self):
        return f"User: {self.user_message}, Bot: {self.bot_response}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateTimeField()
    has_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.payment_date}"
