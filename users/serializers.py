from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .models import UserProfile

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('phone', 'password', 'code')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['code']
        cached_code = cache.get(f'register_{phone}')
        
        if not cached_code or cached_code != code:
            raise serializers.ValidationError("验证码无效或已过期")
            
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("该手机号已注册")
            
        return attrs

    def create(self, validated_data):
        validated_data.pop('code')
        return User.objects.create_user(
            username=validated_data['phone'],
            **validated_data
        )

class PasswordLoginSerializer(serializers.Serializer):
    """密码登录序列化器"""
    phone = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        phone = attrs['phone']
        password = attrs['password']
        
        user = User.objects.filter(phone=phone).first()
        if not user:
            raise serializers.ValidationError("用户不存在")
            
        if not user.check_password(password):
            raise serializers.ValidationError("手机号或密码错误")
            
        self.user = user
        return attrs
        
    def get_user(self):
        return self.user

class CodeLoginSerializer(serializers.Serializer):
    """验证码登录序列化器"""
    phone = serializers.CharField()
    code = serializers.CharField()
    
    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['code']
        
        cached_code = cache.get(f'login_{phone}')
        if not cached_code or cached_code != code:
            raise serializers.ValidationError("验证码无效或已过期")
        
        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={
                'username': phone,
                'password': User.objects.make_random_password()
            }
        )
        
        self.user = user
        self.is_new_user = created
        return attrs
        
    def get_user(self):
        return self.user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'name',
            'nickname',
            'avatar',
            'gender',
            'birthday',
            'phone',
            'email',
            'location',
            'profession',
            'company',
            'position',
            'bio',
            'wechat'
        ]