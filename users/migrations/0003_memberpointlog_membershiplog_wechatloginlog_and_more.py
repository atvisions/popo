# Generated by Django 4.2.17 on 2024-12-19 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberPointLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(verbose_name='积分变更')),
                ('reason', models.CharField(max_length=255, verbose_name='变更原因')),
                ('balance', models.IntegerField(verbose_name='变更后余额')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '积分变更日志',
                'verbose_name_plural': '积分变更日志',
                'db_table': 'member_point_log',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MembershipLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('activate', '激活'), ('renew', '续费'), ('cancel', '取消'), ('expire', '过期'), ('upgrade', '升级'), ('downgrade', '降级')], max_length=20, verbose_name='操作类型')),
                ('level', models.IntegerField(blank=True, null=True, verbose_name='会员等级')),
                ('duration_days', models.IntegerField(blank=True, null=True, verbose_name='期限(天)')),
                ('auto_renew', models.BooleanField(blank=True, null=True, verbose_name='自动续费')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('remark', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '会员变更日志',
                'verbose_name_plural': '会员变更日志',
                'db_table': 'membership_log',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WeChatLoginLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=64, verbose_name='OpenID')),
                ('login_time', models.DateTimeField(auto_now_add=True, verbose_name='登录时间')),
                ('login_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='登录IP')),
                ('user_agent', models.CharField(blank=True, max_length=500, null=True, verbose_name='用户代理')),
                ('status', models.CharField(choices=[('success', '成功'), ('failed', '失败')], max_length=20, verbose_name='登录状态')),
                ('error_message', models.CharField(blank=True, max_length=255, null=True, verbose_name='错误信息')),
            ],
            options={
                'verbose_name': '微信登录日志',
                'verbose_name_plural': '微信登录日志',
                'db_table': 'wechat_login_log',
                'ordering': ['-login_time'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='is_member',
            field=models.BooleanField(default=False, verbose_name='是否是会员'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_wechat_bound',
            field=models.BooleanField(default=False, verbose_name='是否绑定微信'),
        ),
        migrations.AddField(
            model_name='user',
            name='member_auto_renew',
            field=models.BooleanField(default=False, verbose_name='自动续费'),
        ),
        migrations.AddField(
            model_name='user',
            name='member_expire_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='会员过期时间'),
        ),
        migrations.AddField(
            model_name='user',
            name='member_join_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='成为会员时间'),
        ),
        migrations.AddField(
            model_name='user',
            name='member_level',
            field=models.IntegerField(default=0, verbose_name='会员等级'),
        ),
        migrations.AddField(
            model_name='user',
            name='member_points',
            field=models.IntegerField(default=0, verbose_name='会员积分'),
        ),
        migrations.AddField(
            model_name='user',
            name='member_status',
            field=models.CharField(choices=[('inactive', '未激活'), ('active', '正常'), ('expired', '已过期'), ('cancelled', '已取消')], default='inactive', max_length=20, verbose_name='会员状态'),
        ),
        migrations.AddField(
            model_name='user',
            name='wechat_avatar_url',
            field=models.URLField(blank=True, max_length=1000, null=True, verbose_name='微信头像URL'),
        ),
        migrations.AddField(
            model_name='user',
            name='wechat_bound_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='微信绑定时间'),
        ),
        migrations.AddField(
            model_name='user',
            name='wechat_nickname',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='微信昵称'),
        ),
        migrations.AddField(
            model_name='user',
            name='wechat_openid',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True, verbose_name='微信OpenID'),
        ),
        migrations.AddField(
            model_name='user',
            name='wechat_unionid',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True, verbose_name='微信UnionID'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['wechat_openid'], name='users_user_wechat__640083_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['wechat_unionid'], name='users_user_wechat__976edb_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['member_status', 'member_expire_time'], name='users_user_member__ce1127_idx'),
        ),
        migrations.AddField(
            model_name='wechatloginlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wechat_login_logs', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='membershiplog',
            name='operator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operated_membership_logs', to=settings.AUTH_USER_MODEL, verbose_name='操作人'),
        ),
        migrations.AddField(
            model_name='membershiplog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_logs', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='memberpointlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='point_logs', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddIndex(
            model_name='wechatloginlog',
            index=models.Index(fields=['user', '-login_time'], name='wechat_logi_user_id_b63200_idx'),
        ),
        migrations.AddIndex(
            model_name='wechatloginlog',
            index=models.Index(fields=['openid'], name='wechat_logi_openid_e8898d_idx'),
        ),
        migrations.AddIndex(
            model_name='membershiplog',
            index=models.Index(fields=['user', '-created_at'], name='membership__user_id_8ec1dd_idx'),
        ),
        migrations.AddIndex(
            model_name='memberpointlog',
            index=models.Index(fields=['user', '-created_at'], name='member_poin_user_id_261a00_idx'),
        ),
    ]