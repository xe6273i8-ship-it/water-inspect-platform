import axios from 'axios'

// 创建axios实例：统一配置后端基础路径和请求规则
const api = axios.create({
  baseURL: 'http://127.0.0.1:8881/api', // 后端接口根路径（必须与后端app.py的路由前缀一致）
  timeout: 5000, // 普通接口超时时间
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
})

// 请求拦截器：自动携带登录token，实现权限验证
api.interceptors.request.use(
  (config) => {
    // 从本地缓存获取登录token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}` // 规范的token携带格式
    }
    return config
  },
  (error) => {
    console.error('请求拦截器错误：', error)
    return Promise.reject(error)
  }
)

// 响应拦截器：统一处理错误和状态码
api.interceptors.response.use(
  (response) => {
    // 只返回后端的业务数据，简化前端调用
    return response.data
  },
  (error) => {
    // 统一错误处理
    const errMsg = error.response?.data?.msg || error.message || '接口请求失败'
    
    // 401未授权：自动退出登录并跳转登录页
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      ElMessage.error('登录状态已过期，请重新登录')
      window.location.href = '/login'
    }
    
    // 404接口不存在：提示接口路径错误
    if (error.response?.status === 404) {
      ElMessage.error(`接口不存在：${error.config.url} → ${errMsg}`)
    } else {
      ElMessage.error(errMsg)
    }
    
    return Promise.reject(error)
  }
)

// 封装所有业务接口：路径与后端app.py严格对齐
const apiService = {
  // ===================== 登录认证相关 =====================
  // 管理员登录 (POST /api/login)
  login: (data) => api.post('/login', data),
  // 退出登录 (POST /api/logout)
  logout: () => api.post('/logout'),

  // ===================== 巡检任务管理 =====================
  // 获取巡检任务列表 (GET /api/tasks)
  getTasks: () => api.get('/tasks'),
  // 创建巡检任务 (POST /api/tasks)
  createTask: (data) => api.post('/tasks', data),
  // 获取单个任务详情 (GET /api/tasks/:id)
  getTaskDetail: (id) => api.get(`/tasks/${id}`),
  // 更新任务状态 (PUT /api/tasks/:id/status)
  updateTaskStatus: (id, data) => api.put(`/tasks/${id}/status`, data),

  // ===================== 视觉识别预警 =====================
  // 图片识别（文件上传）(POST /api/detect)
  detect: (data) => {
    return axios({
      method: 'post',
      url: 'http://127.0.0.1:8881/api/detect',
      data: data,
      headers: {
        'Content-Type': 'multipart/form-data', // 文件上传必须的Content-Type
        'Authorization': `Bearer ${localStorage.getItem('token')}` // 携带token
      },
      timeout: 10000 // 文件上传超时时间延长至10秒
    })
  },

  // ===================== 预警记录查询 =====================
  // 获取预警记录列表 (GET /api/alerts)
  getAlerts: () => api.get('/alerts'),
  // 标记预警为已处理 (POST /api/alerts/handle/:id)
  handleAlert: (id) => api.post(`/alerts/handle/${id}`),
  // 筛选预警记录 (POST /api/alerts/filter)
  filterAlerts: (data) => api.post('/alerts/filter', data),

  // ===================== 实时告警管理 =====================
  // 获取实时告警列表 (GET /api/realtime/alerts)
  getRealtimeAlerts: () => api.get('/realtime/alerts'),
  // 生成模拟实时告警 (POST /api/realtime/alerts/simulate)
  simulateAlert: () => api.post('/realtime/alerts/simulate'),
  // 标记实时告警为已处理 (POST /api/realtime/alerts/handle/:id)
  handleRealtimeAlert: (id) => api.post(`/realtime/alerts/handle/${id}`),

  // ===================== 巡检路径管理 =====================
  // 获取巡检路径列表 (GET /api/paths)
  getPaths: () => api.get('/paths'),
  // 创建巡检路径 (POST /api/paths)
  createPath: (data) => api.post('/paths', data),
  // 编辑巡检路径 (PUT /api/paths/:id)
  editPath: (id, data) => api.put(`/paths/${id}`, data),
  // 删除巡检路径 (DELETE /api/paths/:id)
  deletePath: (id) => api.delete(`/paths/${id}`),

  // ===================== 水文数据分析 =====================
  // 获取水文数据 (GET /api/hydrology)
  getHydrology: () => api.get('/hydrology'),
  // 获取水文数据趋势 (GET /api/hydrology/trend)
  getHydrologyTrend: (params) => api.get('/hydrology/trend', { params })
}

// 导出接口服务，供前端组件调用
export default apiService