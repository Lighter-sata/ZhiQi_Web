/**
 * 芝栖养生平台 - 表单验证工具
 * 提供常用的表单验证规则和函数
 */

// ==========================================
// 基础验证规则
// ==========================================

/**
 * 验证是否为空
 * @param {string} value - 要验证的值
 * @returns {boolean} 是否为空
 */
export const isEmpty = (value) => {
  return value === null || value === undefined || value === ''
}

/**
 * 验证邮箱格式
 * @param {string} email - 邮箱地址
 * @returns {boolean} 是否为有效邮箱
 */
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * 验证手机号格式 (中国大陆)
 * @param {string} phone - 手机号
 * @returns {boolean} 是否为有效手机号
 */
export const isValidPhone = (phone) => {
  const phoneRegex = /^1[3-9]\d{9}$/
  return phoneRegex.test(phone)
}

/**
 * 验证密码强度
 * @param {string} password - 密码
 * @returns {object} 验证结果 {valid: boolean, message: string}
 */
export const validatePassword = (password) => {
  if (!password || password.length < 6) {
    return { valid: false, message: '密码长度至少6位' }
  }

  if (password.length > 20) {
    return { valid: false, message: '密码长度不能超过20位' }
  }

  // 检查是否包含字母和数字
  const hasLetter = /[a-zA-Z]/.test(password)
  const hasNumber = /\d/.test(password)

  if (!hasLetter || !hasNumber) {
    return { valid: false, message: '密码必须包含字母和数字' }
  }

  return { valid: true, message: '' }
}

/**
 * 验证用户名
 * @param {string} username - 用户名
 * @returns {object} 验证结果 {valid: boolean, message: string}
 */
export const validateUsername = (username) => {
  if (!username) {
    return { valid: false, message: '用户名不能为空' }
  }

  if (username.length < 3) {
    return { valid: false, message: '用户名长度至少3位' }
  }

  if (username.length > 20) {
    return { valid: false, message: '用户名长度不能超过20位' }
  }

  // 检查是否只包含字母、数字、下划线
  const usernameRegex = /^[a-zA-Z0-9_]+$/
  if (!usernameRegex.test(username)) {
    return { valid: false, message: '用户名只能包含字母、数字和下划线' }
  }

  return { valid: true, message: '' }
}

/**
 * 验证真实姓名
 * @param {string} name - 真实姓名
 * @returns {object} 验证结果 {valid: boolean, message: string}
 */
export const validateRealName = (name) => {
  if (!name) {
    return { valid: false, message: '真实姓名不能为空' }
  }

  if (name.length < 2) {
    return { valid: false, message: '真实姓名至少2个字符' }
  }

  if (name.length > 20) {
    return { valid: false, message: '真实姓名不能超过20个字符' }
  }

  // 检查是否包含特殊字符
  const nameRegex = /^[\u4e00-\u9fa5a-zA-Z\s]+$/
  if (!nameRegex.test(name)) {
    return { valid: false, message: '真实姓名只能包含中文、英文和空格' }
  }

  return { valid: true, message: '' }
}

// ==========================================
// 业务验证规则
// ==========================================

/**
 * 验证活动标题
 * @param {string} title - 活动标题
 * @returns {object} 验证结果
 */
export const validateActivityTitle = (title) => {
  if (!title) {
    return { valid: false, message: '活动标题不能为空' }
  }

  if (title.length < 5) {
    return { valid: false, message: '活动标题至少5个字符' }
  }

  if (title.length > 50) {
    return { valid: false, message: '活动标题不能超过50个字符' }
  }

  return { valid: true, message: '' }
}

/**
 * 验证活动描述
 * @param {string} description - 活动描述
 * @returns {object} 验证结果
 */
export const validateActivityDescription = (description) => {
  if (!description) {
    return { valid: false, message: '活动描述不能为空' }
  }

  if (description.length < 20) {
    return { valid: false, message: '活动描述至少20个字符' }
  }

  if (description.length > 1000) {
    return { valid: false, message: '活动描述不能超过1000个字符' }
  }

  return { valid: true, message: '' }
}

/**
 * 验证价格
 * @param {number} price - 价格
 * @returns {object} 验证结果
 */
export const validatePrice = (price) => {
  if (price === null || price === undefined || price === '') {
    return { valid: false, message: '价格不能为空' }
  }

  const numPrice = parseFloat(price)
  if (isNaN(numPrice)) {
    return { valid: false, message: '价格必须是数字' }
  }

  if (numPrice < 0) {
    return { valid: false, message: '价格不能为负数' }
  }

  if (numPrice > 10000) {
    return { valid: false, message: '价格不能超过10000元' }
  }

  return { valid: true, message: '' }
}

/**
 * 验证参与人数
 * @param {number} count - 参与人数
 * @returns {object} 验证结果
 */
export const validateParticipantCount = (count) => {
  if (count === null || count === undefined || count === '') {
    return { valid: false, message: '参与人数不能为空' }
  }

  const numCount = parseInt(count)
  if (isNaN(numCount)) {
    return { valid: false, message: '参与人数必须是整数' }
  }

  if (numCount < 1) {
    return { valid: false, message: '参与人数至少1人' }
  }

  if (numCount > 1000) {
    return { valid: false, message: '参与人数不能超过1000人' }
  }

  return { valid: true, message: '' }
}

// ==========================================
// 表单验证组合
// ==========================================

/**
 * 用户注册表单验证
 * @param {object} form - 注册表单数据
 * @returns {object} 验证结果 {valid: boolean, errors: object}
 */
export const validateRegisterForm = (form) => {
  const errors = {}

  // 用户名验证
  const usernameResult = validateUsername(form.username)
  if (!usernameResult.valid) {
    errors.username = usernameResult.message
  }

  // 邮箱验证
  if (!form.email) {
    errors.email = '邮箱不能为空'
  } else if (!isValidEmail(form.email)) {
    errors.email = '邮箱格式不正确'
  }

  // 密码验证
  const passwordResult = validatePassword(form.password)
  if (!passwordResult.valid) {
    errors.password = passwordResult.message
  }

  // 确认密码验证
  if (form.password !== form.confirmPassword) {
    errors.confirmPassword = '两次输入的密码不一致'
  }

  // 手机号验证 (可选)
  if (form.phone && !isValidPhone(form.phone)) {
    errors.phone = '手机号格式不正确'
  }

  // 真实姓名验证 (可选)
  if (form.real_name) {
    const nameResult = validateRealName(form.real_name)
    if (!nameResult.valid) {
      errors.real_name = nameResult.message
    }
  }

  return {
    valid: Object.keys(errors).length === 0,
    errors
  }
}

/**
 * 用户登录表单验证
 * @param {object} form - 登录表单数据
 * @returns {object} 验证结果
 */
export const validateLoginForm = (form) => {
  const errors = {}

  if (!form.username) {
    errors.username = '用户名不能为空'
  }

  if (!form.password) {
    errors.password = '密码不能为空'
  }

  return {
    valid: Object.keys(errors).length === 0,
    errors
  }
}

/**
 * 活动创建表单验证
 * @param {object} form - 活动表单数据
 * @returns {object} 验证结果
 */
export const validateActivityForm = (form) => {
  const errors = {}

  // 标题验证
  const titleResult = validateActivityTitle(form.title)
  if (!titleResult.valid) {
    errors.title = titleResult.message
  }

  // 描述验证
  const descResult = validateActivityDescription(form.description)
  if (!descResult.valid) {
    errors.description = descResult.message
  }

  // 价格验证
  const priceResult = validatePrice(form.price)
  if (!priceResult.valid) {
    errors.price = priceResult.message
  }

  // 参与人数验证
  const countResult = validateParticipantCount(form.max_participants)
  if (!countResult.valid) {
    errors.max_participants = countResult.message
  }

  // 时间验证
  if (!form.start_time) {
    errors.start_time = '开始时间不能为空'
  }

  if (!form.end_time) {
    errors.end_time = '结束时间不能为空'
  }

  if (form.start_time && form.end_time) {
    const startTime = new Date(form.start_time)
    const endTime = new Date(form.end_time)

    if (startTime >= endTime) {
      errors.end_time = '结束时间必须晚于开始时间'
    }

    if (startTime < new Date()) {
      errors.start_time = '开始时间不能早于当前时间'
    }
  }

  // 地点验证
  if (!form.location) {
    errors.location = '活动地点不能为空'
  }

  return {
    valid: Object.keys(errors).length === 0,
    errors
  }
}

// ==========================================
// 工具函数
// ==========================================

/**
 * 获取字段错误信息
 * @param {object} errors - 错误对象
 * @param {string} field - 字段名
 * @returns {string} 错误信息
 */
export const getFieldError = (errors, field) => {
  return errors[field] || ''
}

/**
 * 检查字段是否有错误
 * @param {object} errors - 错误对象
 * @param {string} field - 字段名
 * @returns {boolean} 是否有错误
 */
export const hasFieldError = (errors, field) => {
  return !!errors[field]
}

/**
 * 清空表单验证错误
 * @param {object} errors - 错误对象
 * @param {string} field - 字段名 (可选，不传则清空所有)
 */
export const clearFieldError = (errors, field) => {
  if (field) {
    delete errors[field]
  } else {
    Object.keys(errors).forEach(key => {
      delete errors[key]
    })
  }
}
