import request from '@/utils/request'
import { publicRequest } from '@/utils/request'

/**
 * 发送短信验证码
 */
export function sendSmsCode(data) {
  return publicRequest({
    url: '/v1/auth/sms/send/',  // 更新
    method: 'post',
    data: {
      phone: data.phone,
      scene: data.scene,
      login_mode: data.login_mode
    }
  })
}

/**
 * 验证码登录
 */
export function loginWithCode(data) {
  return publicRequest({
    url: '/v1/auth/login/code/',  // 更新
    method: 'post',
    data: {
      phone: data.phone,
      code: data.code
    }
  })
}

/**
 * 密码登录
 */
export function loginWithPassword(data) {
  return publicRequest({
    url: '/v1/auth/login/password/',  // 更新
    method: 'post',
    data: {
      phone: data.phone,
      password: data.password
    }
  })
}

/**
 * 用户注册
 */
export function register(data) {
  return publicRequest({
    url: '/v1/auth/register/',  // 更新
    method: 'post',
    data: {
      phone: data.phone,
      code: data.code,
      password: data.password,
      confirm_password: data.password // 添加确认密码字段
    }
  })
}

/**
 * 重置密码
 */
export function resetPassword(data) {
  return publicRequest({
    url: '/v1/auth/password/reset/',  // 更新
    method: 'post',
    data: {
      phone: data.phone,
      code: data.code,
      new_password: data.new_password,
      confirm_password: data.confirm_password
    }
  })
}

/**
 * 上传用户头像
 */
export function uploadAvatar(data) {
  return request({
    url: '/v1/users/profile/avatar/',  // 更新
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 获取用户信息
 */
export function getUserInfo() {
  return request({
    url: '/v1/users/profile/',  // 更新
    method: 'get'
  })
}

/**
 * 更新用户信息
 */
export function updateUserInfo(data) {
  const submitData = { ...data }
  if (submitData.birthday) {
    submitData.birthday = new Date(submitData.birthday).toISOString().split('T')[0]
  }

  return request({
    url: '/v1/users/profile/',  // 更新
    method: 'put',
    data: submitData,
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

/**
 * 更换手机号
 */
export function changePhone(data) {
  return request({
    url: '/v1/users/account/phone/',  // 更新
    method: 'post',
    data: {
      phone: data.phone,
      code: data.code
    }
  })
}

/**
 * 修改密码
 */
export function changePassword(data) {
  return request({
    url: '/v1/users/account/password/',  // 更新
    method: 'post',
    data: {
      old_password: data.old_password,
      new_password: data.new_password,
      confirm_password: data.confirm_password
    }
  })
}

/**
 * 注销账户
 */
export function deleteAccount(data) {
  return request({
    url: '/v1/users/account/delete/',  // 更新
    method: 'post',
    data: {
      password: data.password
    }
  })
}