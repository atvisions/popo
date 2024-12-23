// src/views/user/MyProfile/constants/moduleConfig.js
export const moduleConfig = [
    {
      id: 'basic',
      name: '基本信息',
      icon: 'UserIcon',
      required: true,
      fields: [
        { key: 'name', label: '姓名', type: 'text', required: true },
        { key: 'phone', label: '手机号', type: 'text', required: true },
        { key: 'email', label: '邮箱', type: 'text', required: true },
        { key: 'location', label: '所在地', type: 'text', required: true },
        { key: 'bio', label: '个人简介', type: 'textarea', required: true }
      ]
    },
    {
      id: 'jobPreference',
      name: '求职意向',
      icon: 'BriefcaseIcon',
      fields: [
        { key: 'jobTitle', label: '期望职位', type: 'text', required: true },
        { key: 'jobCity', label: '期望城市', type: 'text', required: true },
        { key: 'salary', label: '期望薪资', type: 'select', required: true },
        { key: 'jobType', label: '工作类型', type: 'select', required: true },
        { key: 'entryTime', label: '到岗时间', type: 'select', required: true }
      ]
    },
    {
      id: 'education',
      name: '教育经历',
      icon: 'AcademicCapIcon',
      multiple: true,
      fields: [
        { key: 'schoolName', label: '学校名称', type: 'text', required: true },
        { key: 'major', label: '专业', type: 'text', required: true },
        { key: 'degree', label: '学历', type: 'select', required: true },
        { key: 'educationTime', label: '就读时间', type: 'daterange', required: true },
        { key: 'achievements', label: '主要成就', type: 'textarea' }
      ]
    },
    {
      id: 'experience',
      name: '工作经历',
      icon: 'BuildingOfficeIcon',
      multiple: true,
      fields: [
        { key: 'companyName', label: '公司名称', type: 'text', required: true },
        { key: 'position', label: '职位', type: 'text', required: true },
        { key: 'workTime', label: '工作时间', type: 'daterange', required: true },
        { key: 'description', label: '工作内容', type: 'textarea', required: true }
      ]
    },
    {
      id: 'skills',
      name: '技能特长',
      icon: 'StarIcon',
      fields: [
        { key: 'skillList', label: '技能列表', type: 'tags', required: true },
        { key: 'skillDescription', label: '技能描述', type: 'textarea' }
      ]
    },
    {
      id: 'languages',
      name: '语言能力',
      icon: 'LanguageIcon',
      multiple: true,
      fields: [
        { key: 'language', label: '语言', type: 'text', required: true },
        { key: 'proficiency', label: '熟练程度', type: 'select', required: true },
        { key: 'certification', label: '语言证书', type: 'text' }
      ]
    },
    {
      id: 'certificates',
      name: '证书奖项',
      icon: 'TrophyIcon',
      multiple: true,
      fields: [
        { key: 'name', label: '证书名称', type: 'text', required: true },
        { key: 'issuer', label: '发证机构', type: 'text', required: true },
        { key: 'issueDate', label: '获得时间', type: 'date', required: true },
        { key: 'description', label: '证书描述', type: 'textarea' }
      ]
    },
    {
      id: 'links',
      name: '社交主页',
      icon: 'LinkIcon',
      multiple: true,
      fields: [
        { key: 'platform', label: '平台', type: 'text', required: true },
        { key: 'url', label: '链接', type: 'url', required: true },
        { key: 'description', label: '描述', type: 'textarea' }
      ]
    }
  ]