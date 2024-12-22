from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 添加微信相关字段
    wechat_openid = models.CharField('微信OpenID', max_length=64, null=True, blank=True, unique=True)
    wechat_unionid = models.CharField('微信UnionID', max_length=64, null=True, blank=True, unique=True)
    wechat_nickname = models.CharField('微信昵称', max_length=255, null=True, blank=True)
    wechat_avatar_url = models.URLField('微信头像URL', max_length=1000, null=True, blank=True)
    is_wechat_bound = models.BooleanField('是否绑定微信', default=False)
    wechat_bound_at = models.DateTimeField('微信绑定时间', null=True, blank=True)
    # 会员相关字段
    is_member = models.BooleanField('是否是会员', default=False)
    member_level = models.IntegerField('会员等级', default=0)
    member_expire_time = models.DateTimeField('会员过期时间', null=True, blank=True)
    member_join_time = models.DateTimeField('成为会员时间', null=True, blank=True)
    member_auto_renew = models.BooleanField('自动续费', default=False)
    member_points = models.IntegerField('会员积分', default=0)
    member_status = models.CharField('会员状态', max_length=20, choices=(
        ('inactive', '未激活'),
        ('active', '正常'),
        ('expired', '已过期'),
        ('cancelled', '已取消')
    ), default='inactive')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['wechat_openid']),
            models.Index(fields=['wechat_unionid']),
            models.Index(fields=['member_status', 'member_expire_time']),
        ]
    def __str__(self):
        return self.phone
    def bind_wechat(self, wechat_info):
        """绑定微信账号"""
        self.wechat_openid = wechat_info.get('openid')
        self.wechat_unionid = wechat_info.get('unionid')
        self.wechat_nickname = wechat_info.get('nickname')
        self.wechat_avatar_url = wechat_info.get('headimgurl')
        self.is_wechat_bound = True
        self.wechat_bound_at = timezone.now()
        self.save()

    def unbind_wechat(self):
        """解绑微信账号"""
        self.wechat_openid = None
        self.wechat_unionid = None
        self.wechat_nickname = None
        self.wechat_avatar_url = None
        self.is_wechat_bound = False
        self.wechat_bound_at = None
        self.save()

    def update_wechat_info(self, wechat_info):
        """更新微信信息"""
        self.wechat_nickname = wechat_info.get('nickname')
        self.wechat_avatar_url = wechat_info.get('headimgurl')
        self.save()
    # 会员相关方法
    def activate_membership(self, level=1, duration_days=30, auto_renew=False):
        """激活会员"""
        now = timezone.now()
        self.is_member = True
        self.member_level = level
        self.member_status = 'active'
        self.member_join_time = self.member_join_time or now
        self.member_expire_time = now + timezone.timedelta(days=duration_days)
        self.member_auto_renew = auto_renew
        self.save()
        
        # 记录会员变更历史
        MembershipLog.objects.create(
            user=self,
            action='activate',
            level=level,
            duration_days=duration_days,
            auto_renew=auto_renew
        )

    def cancel_membership(self):
        """取消会员"""
        self.is_member = False
        self.member_status = 'cancelled'
        self.member_auto_renew = False
        self.save()
        
        MembershipLog.objects.create(
            user=self,
            action='cancel'
        )

    def renew_membership(self, duration_days=30):
        """续费会员"""
        if self.member_expire_time:
            self.member_expire_time += timezone.timedelta(days=duration_days)
        else:
            self.member_expire_time = timezone.now() + timezone.timedelta(days=duration_days)
        
        self.is_member = True
        self.member_status = 'active'
        self.save()
        
        MembershipLog.objects.create(
            user=self,
            action='renew',
            duration_days=duration_days
        )

    def add_member_points(self, points, reason=''):
        """添加会员积分"""
        self.member_points += points
        self.save()
        
        MemberPointLog.objects.create(
            user=self,
            points=points,
            reason=reason,
            balance=self.member_points
        )

    @property
    def is_membership_valid(self):
        """检查会员是否有效"""
        return (
            self.is_member and 
            self.member_status == 'active' and 
            (self.member_expire_time is None or self.member_expire_time > timezone.now())
        )
class MembershipLog(models.Model):
    """会员变更日志"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='membership_logs', verbose_name='用户')
    action = models.CharField('操作类型', max_length=20, choices=(
        ('activate', '激活'),
        ('renew', '续费'),
        ('cancel', '取消'),
        ('expire', '过期'),
        ('upgrade', '升级'),
        ('downgrade', '降级')
    ))
    level = models.IntegerField('会员等级', null=True, blank=True)
    duration_days = models.IntegerField('期限(天)', null=True, blank=True)
    auto_renew = models.BooleanField('自动续费', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    operator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='operated_membership_logs',
        verbose_name='操作人'
    )
    remark = models.CharField('备注', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'membership_log'
        verbose_name = '会员变更日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

class MemberPointLog(models.Model):
    """会员积分变更日志"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='point_logs', verbose_name='用户')
    points = models.IntegerField('积分变更')
    reason = models.CharField('变更原因', max_length=255)
    balance = models.IntegerField('变更后余额')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'member_point_log'
        verbose_name = '积分变更日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
class UserProfile(models.Model):
    """用户档案信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    name = models.CharField('姓名', max_length=50, null=True, blank=True)
    nickname = models.CharField('昵称', max_length=50, null=True, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', null=True, blank=True)
    gender = models.CharField('性别', max_length=10, choices=(
        ('male', '男'),
        ('female', '女'),
        ('other', '其他')
    ), default='other')
    birthday = models.DateField('生日', null=True, blank=True)
    phone = models.CharField('联系电话', max_length=20, null=True, blank=True)
    email = models.EmailField('联系邮箱', max_length=100, null=True, blank=True)
    location = models.CharField('所在地', max_length=100, null=True, blank=True)
    profession = models.CharField('职业', max_length=100, null=True, blank=True)
    company = models.CharField('公司', max_length=100, null=True, blank=True)
    position = models.CharField('职位', max_length=100, null=True, blank=True)
    bio = models.TextField('个人简介', max_length=500, null=True, blank=True)
    wechat = models.CharField('微信号', max_length=100, null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户档案'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name or self.nickname or '基本信息'}"

class WeChatLoginLog(models.Model):
    """微信登录日志"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wechat_login_logs', verbose_name='用户')
    openid = models.CharField('OpenID', max_length=64)
    login_time = models.DateTimeField('登录时间', auto_now_add=True)
    login_ip = models.GenericIPAddressField('登录IP', null=True, blank=True)
    user_agent = models.CharField('用户代理', max_length=500, null=True, blank=True)
    status = models.CharField('登录状态', max_length=20, choices=(
        ('success', '成功'),
        ('failed', '失败')
    ))
    error_message = models.CharField('错误信息', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'wechat_login_log'
        verbose_name = '微信登录日志'
        verbose_name_plural = verbose_name
        ordering = ['-login_time']
        indexes = [
            models.Index(fields=['user', '-login_time']),
            models.Index(fields=['openid']),
        ]

    def __str__(self):
        return f"{self.user.phone} - {self.login_time}"