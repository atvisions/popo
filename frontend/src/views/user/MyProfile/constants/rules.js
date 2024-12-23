// src/views/user/MyProfile/constants/rules.js
export const validationRules = {
    basic: {
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' },
        { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      location: [
        { required: true, message: '请输入所在地', trigger: 'blur' }
      ],
      bio: [
        { required: true, message: '请输入个人简介', trigger: 'blur' },
        { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
      ]
    },
    jobPreference: {
      jobTitle: [
        { required: true, message: '请输入期望职位', trigger: 'blur' }
      ],
      jobCity: [
        { required: true, message: '请输入期望城市', trigger: 'blur' }
      ],
      salary: [
        { required: true, message: '请选择期望薪资', trigger: 'change' }
      ],
      jobType: [
        { required: true, message: '请选择工作类型', trigger: 'change' }
      ]
    },
    education: {
      schoolName: [
        { required: true, message: '请输入学校名称', trigger: 'blur' }
      ],
      major: [
        { required: true, message: '请输入专业', trigger: 'blur' }
      ],
      degree: [
        { required: true, message: '请选择学历', trigger: 'change' }
      ],
      educationTime: [
        { required: true, message: '请选择就读时间', trigger: 'change' }
      ]
    },
    experience: {
      companyName: [
        { required: true, message: '请输入公司名称', trigger: 'blur' }
      ],
      position: [
        { required: true, message: '请输入职位', trigger: 'blur' }
      ],
      workTime: [
        { required: true, message: '请选择工作时间', trigger: 'change' }
      ],
      description: [
        { required: true, message: '请输入工作内容', trigger: 'blur' },
        { min: 10, max: 1000, message: '长度在 10 到 1000 个字符', trigger: 'blur' }
      ]
    }
  }