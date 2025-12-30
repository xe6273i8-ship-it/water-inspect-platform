<template>
  <div class="login-container">
    <el-card class="login-card">
      <div class="login-title">水利巡检平台-管理员登录</div>
      <el-form 
        :model="loginForm" 
        :rules="loginRules" 
        ref="loginFormRef" 
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button 
            type="primary" 
            @click="handleLogin"
            style="width: 100%; --el-button-bg-color: #38bdf8; --el-button-border-color: #38bdf8"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../utils/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const loginFormRef = ref(null)
const loginForm = reactive({
  username: "admin",
  password: "123456"
})
const loginRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  try {
    await loginFormRef.value.validate()
    const res = await api.login(loginForm)
    // 存储token和用户信息到本地
    localStorage.setItem("token", res.data.token)
    localStorage.setItem("userInfo", JSON.stringify(res.data.userInfo))
    ElMessage.success(res.msg)
    // 跳转到首页
    router.push("/")
  } catch (error) {
    ElMessage.error(error.response?.data?.msg || "登录失败")
  }
}
</script>

<style scoped>
.login-container {
  width: 100vw;
  height: 100vh;
  background: #0f172a;
  display: flex;
  justify-content: center;
  align-items: center;
}
.login-card {
  width: 400px;
  background: #1e293b;
  border: 1px solid #334155;
  box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}
.login-title {
  font-size: 20px;
  font-weight: 600;
  color: #e2e8f0;
  text-align: center;
  margin-bottom: 20px;
}
.el-form-item__label {
  color: #e2e8f0 !important;
}
.el-input {
  background: #27374d;
  color: #e2e8f0;
  border-color: #334155;
}
</style>