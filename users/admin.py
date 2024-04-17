from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User, Profile, Product, ChatMessage

# Register your models here.
class UserAdmin(BaseUserAdmin):
  ordering = ["email"]
  add_form = CustomUserCreationForm
  form = CustomUserChangeForm
  model = User
  list_display = ["email", "username", "is_staff", "is_active", "role"]
  list_filter = ["email", "username", "is_staff", "is_active", "role"]
  list_display_links = ["email"]
  search_fields = ["email", "username", "role"]
  fieldsets = (
    (
        _("Login Credentials"), {
          "fields": ("email", "password", "role",)
        },
    ),
    (
        _("Permissons and Groups"), {
          "fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")
        },
    ),
  )

# class ProfileAdmin(admin.ModelAdmin):
#   list_display = ["bio", "profile_image", "affiliation", "industry", "company"]
#   fieldsets = (
#     (
#         _("Personal Information"), {
#           "fields": ("username", "bio", "profile_image", "affiliation", "industry", "company")
#         },
#     ),
#   )
class ChatMessageAdmin(admin.ModelAdmin):
  list_editable = ['is_read']
  list_display = ['sender', 'receiver', 'message', 'is_read']

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(ChatMessage, ChatMessageAdmin)