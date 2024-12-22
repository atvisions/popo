# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import UserProfile

User = get_user_model()

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = '用户资料'
    verbose_name_plural = '用户资料'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 修改 list_display，只使用 User 模型中存在的字段
    list_display = ('id', 'phone', 'username', 'is_active', 'is_staff', 'date_joined', 'last_login')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('phone', 'username')  # 修改搜索字段
    ordering = ('-date_joined',)
    
    # 修改 fieldsets，确保所有字段都存在于 User 模型中
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'), {'fields': ('username', 'email')}),  # 修改个人信息字段
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )

    inlines = [UserProfileInline]
    actions = ['deactivate_users', 'activate_users']

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "禁用选中的用户"

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "启用选中的用户"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_phone')
    search_fields = ('user__phone',)

    def get_phone(self, obj):
        return obj.user.phone
    get_phone.short_description = '手机号'