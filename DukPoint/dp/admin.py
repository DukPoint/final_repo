from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import User, Store, Menu, Payment, Review

# Register your models here.
admin.site.register(Store)
#admin.site.register(User)
admin.site.register(Menu)
admin.site.register(Payment)
admin.site.register(Review)


class CustomUserAdmin(ModelAdmin):
    model = User
    list_display = ('email', 'name', 'is_staff', 'is_superuser', 'points')  # 원하는 필드를 표시
    list_filter = ('is_staff', 'is_superuser')  # 슈퍼유저와 일반 유저로 필터링

    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)