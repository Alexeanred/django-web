from django.urls import path
from . import views
from django.contrib import admin
from .views import send_message, list_messages, new_chat
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('monthlysub/', views.monthlysub, name='monthlysub'),
    path('checkout/', views.checkout, name='checkout'),
    path('logout/', views.logout_view, name='logout'),  # Logout function
    path('admin/', admin.site.urls),
    path('send', send_message, name='send_message'),
    path('chat/', list_messages, name='list_messages'),
    path('chat/send/<int:chat_id>/', send_message, name='send_message_with_id'),
    path('chat/<int:chat_id>/', list_messages, name='list_messages_with_id'),
    path('new_chat/', new_chat, name='new_chat'),
    path('chat/delete/<int:chat_id>/', views.delete_chat, name='delete_chat'),
]
