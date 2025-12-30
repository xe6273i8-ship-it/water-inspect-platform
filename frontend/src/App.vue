<template>
  <!-- 最外层容器 -->
  <el-container style="height: 100vh !important; width: 100vw !important; display: flex !important; flex-direction: row !important; margin: 0 !important; padding: 0 !important; background: #0f172a;">
    <!-- 侧边栏 -->
    <el-aside width="220px" style="height: 100vh !important; background: #1e293b; border-right: 2px solid #38bdf8; padding: 0 !important; flex: 0 0 220px !important;">
      <div style="padding: 20px; text-align: center; border-bottom: 2px solid #38bdf8;">
        <h2 style="color: #38bdf8; margin: 0; font-weight: 600; font-size: 18px;">水利巡检平台</h2>
      </div>
      <el-menu 
        default-active="1" 
        class="el-menu-vertical-demo" 
        @select="handleMenuSelect"
        background-color="#1e293b"
        text-color="#94a3b8"
        active-text-color="#38bdf8"
        style="border-right: none; height: calc(100vh - 80px);"
      >
        <el-menu-item index="1">
          <template #title>
            <el-icon style="color: #38bdf8"><Menu /></el-icon>
            <span style="margin-left: 10px">巡检任务管理</span>
          </template>
        </el-menu-item>
        <el-menu-item index="2">
          <template #title>
            <el-icon style="color: #38bdf8"><Picture /></el-icon>
            <span style="margin-left: 10px">视觉识别预警</span>
          </template>
        </el-menu-item>
        <el-menu-item index="3">
          <template #title>
            <el-icon style="color: #38bdf8"><Search /></el-icon>
            <span style="margin-left: 10px">预警记录查询</span>
          </template>
        </el-menu-item>
        <el-menu-item index="4">
          <template #title>
            <el-icon style="color: #38bdf8"><Bell /></el-icon>
            <span style="margin-left: 10px">实时告警管理</span>
          </template>
        </el-menu-item>
        <el-menu-item index="5">
          <template #title>
            <el-icon style="color: #38bdf8"><Location /></el-icon>
            <span style="margin-left: 10px">巡检路径管理</span>
          </template>
        </el-menu-item>
        <el-menu-item index="6">
          <template #title>
            <el-icon style="color: #38bdf8"><DataAnalysis /></el-icon>
            <span style="margin-left: 10px">水校准数据分析</span>
          </template>
        </el-menu-item>
        <el-menu-item index="7">
          <template #title>
            <el-icon style="color: #38bdf8"><Grid /></el-icon>
            <span style="margin-left: 10px">3D 可视化分析</span>
          </template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主容器 -->
    <el-container style="flex: 1 !important; width: calc(100vw - 220px) !important; height: 100vh !important; display: flex !important; flex-direction: column !important; margin: 0 !important; padding: 0 !important;">
      <!-- 顶部导航 -->
      <el-header style="height: 60px !important; width: 100% !important; background: #1e293b; color: #fff; padding: 0 20px !important; border-bottom: 2px solid #38bdf8; margin: 0 !important; flex: 0 0 60px !important;">
        <div style="display: flex; justify-content: space-between; align-items: center; height: 100%;">
          <div style="font-size: 18px; font-weight: 600; color: #38bdf8;">水利设施智能视觉巡检与预警平台</div>
          <el-dropdown @command="handleDropdown">
            <div style="display: flex; align-items: center; cursor: pointer;">
              <el-icon style="color: #38bdf8; margin-right: 5px;"><User /></el-icon>
              <span style="color: #e2e8f0">{{ userInfo.username || '管理员' }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu style="background: #1e293b; border: 1px solid #38bdf8;">
                <el-dropdown-item command="profile" style="color: #94a3b8">个人中心</el-dropdown-item>
                <el-dropdown-item command="logout" style="color: #94a3b8">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 主内容区 -->
      <el-main style="flex: 1 !important; width: 100% !important; height: calc(100vh - 60px) !important; background: #0f172a; color: #e2e8f0; padding: 20px !important; margin: 0 !important; overflow-y: auto !important;">
        <!-- 1. 巡检任务管理 -->
        <div v-if="activeMenu === '1'" class="content-card" style="width: 100%; margin-bottom: 20px;">
          <div style="font-size: 20px; font-weight: 600; margin-bottom: 20px; display: flex; align-items: center; color: #38bdf8;">
            <el-icon style="color: #38bdf8; margin-right: 10px;"><Menu /></el-icon>
            巡检任务列表
          </div>
          <el-card style="width: 100%; background: #1e293b; border: 1px solid #38bdf8; box-shadow: 0 2px 12px rgba(56, 189, 248, 0.1);">
            <el-table 
              :data="taskList" 
              border 
              style="width: 100%" 
              :loading="loading"
              :header-cell-style="{ background: '#27374d', color: '#38bdf8', padding: '12px 16px', borderBottom: '2px solid #38bdf8' }"
              :row-style="{ background: '#1e293b', color: '#e2e8f0' }"
              :cell-style="{ padding: '12px 16px', verticalAlign: 'middle', borderRight: '1px solid #334155' }"
            >
              <el-table-column prop="id" label="任务ID" width="80" align="center" />
              <el-table-column prop="taskName" label="任务名称" align="center" />
              <el-table-column prop="taskTime" label="创建时间" width="180" align="center" />
              <el-table-column prop="status" label="任务状态" width="120" align="center">
                <template v-slot="scope">
                  <el-tag 
                    :type="scope.row.status === '执行中' ? 'primary' : scope.row.status === '已完成' ? 'success' : 'warning'"
                    style="--el-tag-bg-color: var(--el-color-primary-light-9); --el-tag-border-color: var(--el-color-primary-light-7); padding: 4px 12px; font-weight: 500;"
                  >
                    {{ scope.row.status }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120" align="center">
                <template v-slot="scope">
                  <el-button 
                    size="small" 
                    type="primary"
                    @click="handleTaskOperate(scope.row)"
                    style="--el-button-bg-color: #38bdf8; --el-button-border-color: #38bdf8; padding: 4px 12px; font-weight: 500; vertical-align: middle; line-height: 1;"
                  >
                    {{ scope.row.status === '执行中' ? '跟踪进度' : scope.row.status === '待执行' ? '开始执行' : '详情' }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px; width: 100%;">
              <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="currentPage"
                :page-sizes="[10, 20, 50, 100]"
                :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="total"
                style="color: #e2e8f0"
              />
              <el-button 
                type="primary" 
                @click="createTask"
                style="--el-button-bg-color: #38bdf8; --el-button-border-color: #38bdf8; font-weight: 500;"
              >
                创建巡检任务
              </el-button>
            </div>
          </el-card>
        </div>

        <!-- 2. 视觉识别预警 -->
        <div v-if="activeMenu === '2'" class="content-card" style="width: 100%; margin-bottom: 20px;">
          <div style="font-size: 20px; font-weight: 600; margin-bottom: 20px; display: flex; align-items: center; color: #38bdf8;">
            <el-icon style="color: #38bdf8; margin-right: 10px;"><Picture /></el-icon>
            视觉识别预警
          </div>
          <el-card style="width: 100%; background: #1e293b; border: 1px solid #38bdf8; box-shadow: 0 2px 12px rgba(56, 189, 248, 0.1);">
            <el-upload
              class="upload-demo"
              drag
              action="#"
              :auto-upload="false"
              :on-change="handleFileChange"
              :file-list="fileList"
              style="width: 100%; border: 2px dashed #38bdf8; background: #27374d; margin-bottom: 20px; padding: 20px !important;"
            >
              <template #default>
                <el-icon style="color: #38bdf8; font-size: 40px; margin-bottom: 10px;"><Upload /></el-icon>
                <div class="el-upload__text" style="color: #e2e8f0; font-size: 16px;">将文件拖到此处，或点击上传</div>
              </template>
            </el-upload>
            <el-button 
              type="primary" 
              @click="uploadAndRecognize" 
              :disabled="!fileList.length"
              style="--el-button-bg-color: #38bdf8; --el-button-border-color: #38bdf8; margin-bottom: 20px; font-weight: 500;"
            >
              选择图片上传识别
            </el-button>
            
            <div v-if="previewImage" style="width: 100%; margin-bottom: 20px; border: 1px solid #334155; padding: 10px; border-radius: 4px;">
              <div style="font-size: 16px; font-weight: 500; margin-bottom: 10px; color: #38bdf8">图片预览</div>
              <img :src="previewImage" alt="预览图片" style="width: 100%; border: 1px solid #38bdf8; border-radius: 4px; max-height: 500px; object-fit: contain;" />
            </div>
            <div v-if="recognizeResult" style="width: 100%; padding: 20px; border: 1px solid #38bdf8; border-radius: 4px; background: #27374d;">
              <div style="font-size: 16px; font-weight: 500; margin-bottom: 10px; color: #38bdf8">识别结果</div>
              <pre style="color: #e2e8f0; white-space: pre-wrap; margin: 0; width: 100%; font-size: 14px; font-weight: 500;">{{ recognizeResult }}</pre>
            </div>
          </el-card>
        </div>

        <!-- 3. 预警记录查询 -->
        <div v-if="activeMenu === '3'" class="content-card" style="width: 100%; margin-bottom: 20px;">
          <div style="font-size: 20px; font-weight: 600; margin-bottom: 20px; display: flex; align-items: center; color: #38bdf8;">
            <el-icon style="color: #38bdf8; margin-right: 10px;"><Search /></el-icon>
            预警记录查询
          </div>
          <el-card style="width: 100%; background: #1e293b; border: 1px solid #38bdf8; box-shadow: 0 2px 12px rgba(56, 189, 248, 0.1);">
            <!-- 表单：强制标签与输入框分离 -->
            <el-form 
              :model="alertQueryForm" 
              style="width: 100%; margin-bottom: 20px; background: #27374d; padding: 20px; border-radius: 4px; border: 1px solid #334155;"
              label-width="100px"
              label-position="left"
            >
              <el-row :gutter="24">
                <el-col :span="6">
                  <el-form-item label="预警类型" style="color: #38bdf8; width: 100%; font-weight: 500;">
                    <el-select v-model="alertQueryForm.type" placeholder="请选择" style="width: 100%; background: #1e293b; color: #e2e8f0; border-color: #38bdf8; font-weight: 500;">
                      <el-option label="闸口异常" value="闸口异常" style="background: #1e293b; color: #e2e8f0;"></el-option>
                      <el-option label="水位超标" value="水位超标" style="background: #1e293b; color: #e2e8f0;"></el-option>
                      <el-option label="设备故障" value="设备故障" style="background: #1e293b; color: #e2e8f0;"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="处置状态" style="color: #38bdf8; width: 100%; font-weight: 500;">
                    <el-select v-model="alertQueryForm.status" placeholder="请选择" style="width: 100%; background: #1e293b; color: #e2e8f0; border-color: #38bdf8; font-weight: 500;">
                      <el-option label="未处置" value="未处理" style="background: #1e293b; color: #e2e8f0;"></el-option>
                      <el-option label="已处置" value="已处理" style="background: #1e293b; color: #e2e8f0;"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="开始日期" style="color: #38bdf8; width: 100%; font-weight: 500;">
                    <el-date-picker v-model="alertQueryForm.startDate" type="date" placeholder="选择日期" style="width: 100%; background: #1e293b; color: #e2e8f0; border-color: #38bdf8; font-weight: 500;"></el-date-picker>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="至" style="color: #38bdf8; width: 100%; font-weight: 500;">
                    <el-date-picker v-model="alertQueryForm.endDate" type="date" placeholder="选择日期" style="width: 100%; background: #1e293b; color: #e2e8f0; border-color: #38bdf8; font-weight: 500;"></el-date-picker>
                  </el-form-item>
                </el-col>
                <el-col :span="24" style="text-align: right; padding-top: 10px;">
                  <el-button 
                    type="primary" 
                    @click="queryAlertRecords"
                    style="--el-button-bg-color: #38bdf8; --el-button-border-color: #38bdf8; margin-right: 10px; font-weight: 500;"
                  >
                    查询
                  </el-button>
                  <el-button @click="resetAlertQuery" style="background: #27374d; color: #e2e8f0; border-color: #38bdf8; font-weight: 500;">
                    重置
                  </el-button>
                </el-col>
              </el-row>
            </el-form>

            <el-table 
              :data="alertRecordList" 
              border 
              style="width: 100%" 
              :loading="loading"
              :header-cell-style="{ background: '#27374d', color: '#38bdf8', padding: '12px 16px', borderBottom: '2px solid #38bdf8', fontWeight: 500 }"
              :row-style="{ background: '#1e293b', color: '#e2e8f0' }"
              :cell-style="{ padding: '12px 16px', verticalAlign: 'middle', borderRight: '1px solid #334155', fontWeight: 500 }"
            >
              <el-table-column prop="id" label="记录ID" width="80" align="center" />
              <el-table-column prop="alertType" label="预警类型" align="center" />
              <el-table-column prop="alertTime" label="预警时间" width="180" align="center" />
              <el-table-column prop="confidence" label="置信度(%)" width="180" align="center">
                <template v-slot="scope">
                  <div style="display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%;">
                    <el-progress 
                      :percentage="Math.min(Number(scope.row.confidence), 100)" 
                      :show-text="false" 
                      style="width: 120px; height: 8px;"
                      color="#38bdf8"
                    />
                    <span style="color: #38bdf8; font-size: 14px; font-weight: 600;">
                      {{ Math.min(Number(scope.row.confidence), 100).toFixed(1) }}%
                    </span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="处置状态" width="120" align="center">
                <template v-slot="scope">
                  <el-tag 
                    :type="scope.row.status === '已处理' ? 'success' : 'danger'"
                    style="--el-tag-bg-color: var(--el-color-primary-light-9); --el-tag-border-color: var(--el-color-primary-light-7); padding: 4px 12px; font-weight: 600;"
                  >
                    {{ scope.row.status === '已处理' ? '已处置' : '未处置' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120" align="center">
                <template v-slot="scope">
                  <el-button 
                    size="small" 
                    type="primary"
                    @click="handleDisposeAlert(scope.row)"
                    v-if="scope.row.status === '未处理'"
                    style="--el-button-bg-color: #38bdf8; --el-button-border-color: #38bdf8; padding: 4px 12px; font-weight: 500; vertical-align: middle; line-height: 1;"
                  >
                    标记已处置
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-pagination
              @size-change="handleAlertSizeChange"
              @current-change="handleAlertCurrentChange"
              :current-page="alertCurrentPage"
              :page-sizes="[10, 20, 50, 100]"
              :page-size="alertPageSize"
              layout="total, sizes, prev, pager, next, jumper"
              :total="alertTotal"
              style="width: 100%; margin-top: 20px; text-align: right; color: #e2e8f0; font-weight: 500;"
            />
          </el-card>
        </div>

        <!-- 4. 实时告警管理（核心修复区） -->
        <div v-if="activeMenu === '4'" class="content-card" style="width: 100%; margin-bottom: 20px;">
          <div style="font-size: 20px; font-weight: 600; margin-bottom: 20px; display: flex; align-items: center; color: #38bdf8;">
            <el-icon style="color: #38bdf8; margin-right: 10px;"><Bell /></el-icon>
            实时告警管理
          </div>
          <el-card style="width: 100%; background: #1e293b; border: 1px solid #38bdf8; box-shadow: 0 2px 12px rgba(56, 189, 248, 0.1);">
            <div style="width: 100%; margin-bottom: 20px;">
              <el-button 
                type="danger" 
                @click="generateMockAlert"
                style="--el-button-bg-color: #ef4444; --el-button-border-color: #ef4444; font-weight: 500;"
              >
                生成模拟实时告警
              </el-button>
            </div>
            <!-- 修复：统一单元格对齐 -->
            <el-table 
              :data="realTimeAlertList" 
              border 
              style="width: 100%" 
              :loading="loading"
              :header-cell-style="{ background: '#27374d', color: '#38bdf8', padding: '12px 16px', borderBottom: '2px solid #38bdf8', fontWeight: 500 }"
              :row-style="{ background: '#1e293b', color: '#e2e8f0' }"
              :cell-style="{ padding: '12px 16px', verticalAlign: 'middle', borderRight: '1px solid #334155', textAlign: 'center' }"
            >
              <el-table-column prop="id" label="告警ID" width="80" align="center" />
              <el-table-column prop="alert_type" label="告警类型" align="center" />
              <el-table-column prop="content" label="告警内容" align="center" />
              <el-table-column prop="create_time" label="告警时间" width="180" align="center" />
              <el-table-column label="操作" width="120" align="center">
                <template v-slot="scope">
                  <!-- 终极修复：原生按钮 + 强制居中 -->
                  <button 
                    @click="handleProcessAlert(scope.row)"
                    style="
                      background-color: #10b981;
                      color: white;
                      border: none;
                      border-radius: 4px;
                      padding: 6px 16px;
                      font-size: 14px;
                      font-weight: 500;
                      cursor: pointer;
                      display: inline-flex;
                      align-items: center;
                      justify-content: center;
                      height: 32px;
                      width: 90px;
                      margin: 0 auto;
                      box-sizing: border-box;
                    "
                    onmouseover="this.style.backgroundColor='#059669'"
                    onmouseout="this.style.backgroundColor='#10b981'"
                  >
                    标记已处理
                  </button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>

        <!-- 5. 巡检路径管理 -->
        <div v-if="activeMenu === '5'" class="content-card" style="width: 100%; margin-bottom: 20px;">
          <div style="font-size: 20px; font-weight: 600; margin-bottom: 20px; display: flex; align-items: center; color: #38bdf8;">
            <el-icon style="color: #38bdf8; margin-right: 10px;"><Location /></el-icon>
            巡检路径管理
          </div>
          <el-card style="width: 100%; background: #1e293b; border: 1px solid #38bdf8; box-shadow: 0 2px 12px rgba(56, 189, 248, 0.1);">
            <!-- 表单：强制标签宽度 + 输入框内边距 -->
            <el-form 
              :model="pathForm" 
              :rules="pathRules" 
              ref="pathFormRef" 
              style="width: 100%; margin-bottom: 20px; background: #27374d; padding: 20px; border-radius: 4px; border: 1px solid #334155;"
              label-width="100px"
              label-position="left"
            >
              <el-row :gutter="24">
                <el-col :span="8">
                  <el-form-item label="路径名称" prop="pathName" style="color: #38bdf8; width: 100%; font-weight: 500;">
                    <el-input 
                      v-model="pathForm.pathName" 
                      placeholder="输入路径名称（如：东河段）" 
                      style="width: 100%; background: #1e293b; color: #e2e8f0; border-color: #38bdf8; padding: 8px 12px !important; font-weight: 500;"
                    ></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="10">
                  <el-form-item label="巡检点" prop="checkPoints" style="color: #38bdf8; width: 100%; font-weight: 500;">
                    <el-input 
                      v-model="pathForm.checkPoints" 
                      placeholder="多个巡检点用逗号分隔" 
                      style="width: 100%; background: #1e293b; color: #e2e8f0; border-color: #38bdf8; padding: 8px 12px !important; font-weight: 500;"
                    ></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="巡检周期" style="color: #38bdf8; width: 100%; font-weight: 500;">
                    <el-select 
                      v-model="pathForm.cycle" 
                      placeholder="请选择" 
                      style="width: 100%; background: #1e293b; color: #e2e8f0; border-color: #38bdf8; padding: 8px 12px !important; font-weight: 500;"
                    >
                      <el-option label="每日" value="每日" style="background: #1e293b; color: #e2e8f0;"></el-option>
                      <el-option label="每周" value="每周" style="background: #1e293b; color: #e2e8f0;"></el-option>
                      <el-option label="每月" value="每月" style="background: #1e293b; color: #e2e8f0;"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="24" style="text-align: right; padding-top: 10px;">
                  <el-button 
                    type="primary" 
                    @click="createPath"
                    style="--el-button-bg-color: #38bdf8; --el-button-border-color: #38bdf8; margin-right: 10px; font-weight: 500;"
                  >
                    创建路径
                  </el-button>
                  <el-button @click="resetPathForm" style="background: #27374d; color: #e2e8f0; border-color: #38bdf8; font-weight: 500;">
                    重置
                  </el-button>
                </el-col>
              </el-row>
            </el-form>

            <el-table 
              :data="pathList" 
              border 
              style="width: 100%" 
              :loading="loading"
              :header-cell-style="{ background: '#27374d', color: '#38bdf8', padding: '12px 16px', borderBottom: '2px solid #38bdf8', fontWeight: 500 }"
              :row-style="{ background: '#1e293b', color: '#e2e8f0' }"
              :cell-style="{ padding: '12px 16px', verticalAlign: 'middle', borderRight: '1px solid #334155', fontWeight: 500 }"
            >
              <el-table-column prop="id" label="路径ID" width="80" align="center" />
              <el-table-column prop="path_name" label="路径名称" align="center" />
              <el-table-column prop="check_points" label="巡检点" align="center">
                <template v-slot="scope">
                  <el-tag 
                    v-for="point in scope.row.check_points" 
                    :key="point" 
                    size="small" 
                    style="margin-right: 5px; background: #27374d; color: #38bdf8; border-color: #38bdf8; padding: 4px 8px; font-weight: 500;"
                  >
                    {{ point }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="cycle" label="巡检周期" width="120" align="center" />
              <el-table-column label="操作" width="160" align="center">
                <template v-slot="scope">
                  <el-button 
                    size="small" 
                    type="primary"
                    @click="editPath(scope.row)"
                    style="--el-button-bg-color: #38bdf8; --el-button-border-color: #38bdf8; margin-right: 5px; padding: 4px 8px; font-weight: 500; vertical-align: middle; line-height: 1;"
                  >
                    编辑
                  </el-button>
                  <el-button 
                    size="small" 
                    type="danger"
                    @click="deletePath(scope.row.id)"
                    style="--el-button-bg-color: #ef4444; --el-button-border-color: #ef4444; padding: 4px 8px; font-weight: 500; vertical-align: middle; line-height: 1;"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>

        <!-- 6. 水校准数据分析 -->
        <div v-if="activeMenu === '6'" class="content-card" style="width: 100%; margin-bottom: 20px;">
          <div style="font-size: 20px; font-weight: 600; margin-bottom: 20px; display: flex; align-items: center; color: #38bdf8;">
            <el-icon style="color: #38bdf8; margin-right: 10px;"><DataAnalysis /></el-icon>
            水校准数据分析
          </div>
          <el-card style="width: 100%; background: #1e293b; border: 1px solid #38bdf8; box-shadow: 0 2px 12px rgba(56, 189, 248, 0.1);">
            <!-- 刷新按钮 -->
            <div style="width: 100%; margin-bottom: 20px; display: flex; justify-content: flex-end;">
              <el-button 
                type="primary" 
                @click="refreshHydroData"
                style="--el-button-bg-color: #38bdf8; --el-button-border-color: #38bdf8; font-weight: 500;"
              >
                刷新数据
              </el-button>
            </div>
            
            <!-- 加载状态 -->
            <div v-if="loading" style="width: 100%; height: 400px; min-width: 600px; min-height: 400px; display: flex; align-items: center; justify-content: center; border: 1px solid #38bdf8; border-radius: 4px; background: #27374d;">
              <el-icon size="40" color="#38bdf8"><Loading /></el-icon>
              <span style="margin-left: 10px; color: #38bdf8; font-weight: 500;">数据加载中...</span>
            </div>
            
            <!-- 错误提示 -->
            <div v-else-if="hydroDataError" style="color: #ef4444; margin: 20px 0; width: 100%; font-weight: 500; text-align: center; padding: 20px; border: 1px solid #ef4444; border-radius: 4px; background: #27374d;">
              {{ hydroDataError }}
            </div>
            
            <!-- 图表容器 -->
            <div v-else style="width: 100%; height: 400px; min-width: 600px; min-height: 400px; border: 1px solid #38bdf8; border-radius: 4px; padding: 10px; background: #27374d;" ref="chartRef">
              <div id="hydro-chart" style="width: 100%; height: 100%;"></div>
            </div>
          </el-card>
        </div>
        <!-- 7. 3D可视化 -->
        <div v-if="activeMenu === '7'" class="content-card" style="width: 100%; margin-bottom: 20px;">
          <div style="font-size: 20px; font-weight: 600; margin-bottom: 20px; display: flex; align-items: center; color: #38bdf8;">
            <el-icon style="color: #38bdf8; margin-right: 10px;"><Grid /></el-icon>
            3D可视化
          </div>
          <el-card style="width: 100%; background: #1e293b; border: 1px solid #38bdf8; box-shadow: 0 2px 12px rgba(56, 189, 248, 0.1);">
            <ThreeDView />
          </el-card>
        </div>

      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, reactive, onMounted, onUpdated, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElNotification } from 'element-plus'
import {
  Menu, Picture, Search, Bell, Location, DataAnalysis, User, Upload, Loading
} from '@element-plus/icons-vue'
import ThreeDView from "@/components/ThreeDView.vue"
import * as echarts from 'echarts'

const router = useRouter()
// 核心引用
const chartRef = ref(null)
const pathFormRef = ref(null)
let hydroChartInstance = null

// 登录相关
const userInfo = ref(JSON.parse(localStorage.getItem("userInfo") || JSON.stringify({ username: '管理员' })))

const handleLogout = async () => {
  try {
    localStorage.removeItem("token")
    localStorage.removeItem("userInfo")
    ElMessage.success("退出登录成功")
  } catch (error) {
    ElMessage.error("退出登录失败，请重试")
  }
}

const handleDropdown = (command) => {
  if (command === "logout") {
    handleLogout()
  } else if (command === "profile") {
    ElMessage.info("个人中心功能正在开发中...")
  }
}

// 基础变量
const activeMenu = ref('1')
const loading = ref(false)

// 菜单切换逻辑
const handleMenuSelect = (index) => {
  activeMenu.value = index
  if (index === '1') getTaskList()
  if (index === '3') getAlertRecords()
  if (index === '4') getRealTimeAlerts()
  if (index === '5') getPathList()
  if (index === '6') {
    setTimeout(() => {
      getHydroData()
      initHydroChart()
    }, 200)
  }
  //if (index === '7') {
    //router.push('/3d')
  //}
}

// 巡检任务管理
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const taskList = ref([])

const getTaskList = async () => {
  loading.value = true
  try {
    taskList.value = [
      {"id": 1, "taskName": "东河段日常巡检", "taskTime": "2025-12-27 09:00", "status": "待执行"},
      {"id": 2, "taskName": "西闸口设备检查", "taskTime": "2025-12-26 14:30", "status": "已完成"},
      {"id": 3, "taskName": "北泵站维护巡检", "taskTime": "2025-12-25 10:00", "status": "执行中"},
      {"id": 4, "taskName": "新巡检任务", "taskTime": "2025-12-27 16:55", "status": "待执行"},
      {"id": 5, "taskName": "新巡检任务", "taskTime": "2025-12-27 17:06", "status": "待执行"}
    ]
    total.value = 5
  } catch (error) {
    ElMessage.error('获取任务列表失败')
    taskList.value = [
      {"id": 1, "taskName": "东河段日常巡检", "taskTime": "2025-12-27 09:00", "status": "待执行"},
      {"id": 2, "taskName": "西闸口设备检查", "taskTime": "2025-12-26 14:30", "status": "已完成"},
      {"id": 3, "taskName": "北泵站维护巡检", "taskTime": "2025-12-25 10:00", "status": "执行中"},
      {"id": 4, "taskName": "新巡检任务", "taskTime": "2025-12-27 16:55", "status": "待执行"},
      {"id": 5, "taskName": "新巡检任务", "taskTime": "2025-12-27 17:06", "status": "待执行"}
    ]
    total.value = 5
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (val) => {
  pageSize.value = val
  getTaskList()
}
const handleCurrentChange = (val) => {
  currentPage.value = val
  getTaskList()
}

const createTask = async () => {
  try {
    taskList.value.push({
      id: taskList.value.length + 1,
      taskName: "新巡检任务",
      taskTime: new Date().toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }).replace(/\//g, '-'),
      status: "待执行"
    })
    total.value = taskList.value.length
    ElNotification({
      title: '成功',
      message: '巡检任务创建成功',
      type: 'success',
      customClass: 'notification'
    })
  } catch (error) {
    ElMessage.error('创建任务失败')
  }
}

const handleTaskOperate = (row) => {
  if (row.status === '待执行') {
    ElMessage.success(`任务${row.taskName}已开始执行`)
  } else if (row.status === '执行中') {
    ElMessage.success(`跟踪任务${row.taskName}进度`)
  } else {
    ElMessage.success(`查看任务${row.taskName}详情`)
  }
}

// 视觉识别预警
const fileList = ref([])
const previewImage = ref('')
const recognizeResult = ref('')
const recognizeSuccess = ref(false)

const handleFileChange = (file) => {
  if (file.raw) previewImage.value = URL.createObjectURL(file.raw)
}

const uploadAndRecognize = async () => {
  loading.value = true
  try {
    recognizeSuccess.value = true
    recognizeResult.value = "闸口异常（置信度：98.5%）\n水位正常（置信度：99.2%）"
    ElMessage.success('图片识别完成')
  } catch (error) {
    recognizeSuccess.value = false
    recognizeResult.value = '识别失败：网络或服务异常'
    ElMessage.error('识别失败')
  } finally {
    loading.value = false
  }
}

// 预警记录查询
const alertQueryForm = reactive({
  type: '',
  status: '',
  startDate: '',
  endDate: ''
})
const alertRecordList = ref([])
const alertCurrentPage = ref(1)
const alertPageSize = ref(10)
const alertTotal = ref(0)

const getAlertRecords = async () => {
  loading.value = true
  try {
    alertRecordList.value = [
      {"id": 1, "alertType": "闸口异常", "alertTime": "2025-12-27 09:15", "confidence": 98.5, "status": "未处理"},
      {"id": 2, "alertType": "水位超标", "alertTime": "2025-12-26 15:20", "confidence": 95.2, "status": "已处理"}
    ]
    alertTotal.value = 2
  } catch (error) {
    ElMessage.error('获取预警记录失败')
    alertRecordList.value = [
      {"id": 1, "alertType": "闸口异常", "alertTime": "2025-12-27 09:15", "confidence": 98.5, "status": "未处理"},
      {"id": 2, "alertType": "水位超标", "alertTime": "2025-12-26 15:20", "confidence": 95.2, "status": "已处理"}
    ]
    alertTotal.value = 2
  } finally {
    loading.value = false
  }
}

const queryAlertRecords = () => {
  getAlertRecords()
  ElMessage.info('已根据筛选条件查询')
}

const resetAlertQuery = () => {
  alertQueryForm.type = ''
  alertQueryForm.status = ''
  alertQueryForm.startDate = ''
  alertQueryForm.endDate = ''
}

const handleDisposeAlert = async (row) => {
  try {
    row.status = '已处理'
    ElMessage.success(`预警${row.id}已标记为已处置`)
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleAlertSizeChange = (val) => {
  alertPageSize.value = val
  getAlertRecords()
}
const handleAlertCurrentChange = (val) => {
  alertCurrentPage.value = val
  getAlertRecords()
}

// 实时告警管理
const realTimeAlertList = ref([])

const getRealTimeAlerts = async () => {
  loading.value = true
  try {
    realTimeAlertList.value = [
      {"id": 1, "alert_type": "设备故障", "content": "水位传感器故障", "create_time": "2025-12-27 10:00"},
      {"id": 2, "alert_type": "水位预警", "content": "水位超过警戒值0.5米", "create_time": "2025-12-27 09:30"}
    ]
  } catch (error) {
    ElMessage.error('获取实时告警失败')
    realTimeAlertList.value = [
      {"id": 1, "alert_type": "设备故障", "content": "水位传感器故障", "create_time": "2025-12-27 10:00"},
      {"id": 2, "alert_type": "水位预警", "content": "水位超过警戒值0.5米", "create_time": "2025-12-27 09:30"}
    ]
  } finally {
    loading.value = false
  }
}

const generateMockAlert = async () => {
  try {
    realTimeAlertList.value.push({
      id: realTimeAlertList.value.length + 1,
      alert_type: "设备故障",
      content: "流量传感器异常",
      create_time: new Date().toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }).replace(/\//g, '-')
    })
    ElNotification({
      title: '新告警',
      message: '已生成实时告警',
      type: 'warning',
      customClass: 'notification'
    })
  } catch (error) {
    ElMessage.error('生成告警失败')
  }
}

const handleProcessAlert = async (row) => {
  try {
    row.status = '已处理'
    ElMessage.success(`告警${row.id}已标记为已处理`)
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 巡检路径管理
const pathForm = reactive({
  pathName: '',
  checkPoints: '',
  cycle: '每日'
})
const pathRules = {
  pathName: [{ required: true, message: '请输入路径名称', trigger: 'blur' }],
  checkPoints: [{ required: true, message: '请输入巡检点', trigger: 'blur' }]
}
const pathList = ref([])

const getPathList = async () => {
  loading.value = true
  try {
    pathList.value = [
      {"id": 1, "path_name": "东河段全线巡检", "check_points": ["1号闸口", "2号监测点", "3号泵站"], "cycle": "每日"},
      {"id": 2, "path_name": "西闸口专项检查", "check_points": ["西闸口设备", "备用电源"], "cycle": "每周"},
      {"id": 3, "path_name": "东西段全线巡检", "check_points": ["1号闸口", "2号监测点", "3号泵站"], "cycle": "每日"},
      {"id": 4, "path_name": "门口小河段", "check_points": ["名门口"], "cycle": "每周"}
    ]
    total.value = 4
  } catch (error) {
    ElMessage.error('获取巡检路径失败')
    pathList.value = [
      {"id": 1, "path_name": "东河段全线巡检", "check_points": ["1号闸口", "2号监测点", "3号泵站"], "cycle": "每日"},
      {"id": 2, "path_name": "西闸口专项检查", "check_points": ["西闸口设备", "备用电源"], "cycle": "每周"},
      {"id": 3, "path_name": "东西段全线巡检", "check_points": ["1号闸口", "2号监测点", "3号泵站"], "cycle": "每日"},
      {"id": 4, "path_name": "门口小河段", "check_points": ["名门口"], "cycle": "每周"}
    ]
    total.value = 4
  } finally {
    loading.value = false
  }
}

const createPath = async () => {
  pathFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        pathList.value.push({
          id: pathList.value.length + 1,
          path_name: pathForm.pathName,
          check_points: pathForm.checkPoints.split(','),
          cycle: pathForm.cycle
        })
        ElMessage.success('巡检路径创建成功')
        resetPathForm()
      } catch (error) {
        ElMessage.error('创建路径失败')
      }
    }
  })
}

const resetPathForm = () => {
  pathFormRef.value?.resetFields()
  pathForm.cycle = '每日'
}

const editPath = (row) => {
  pathForm.pathName = row.path_name
  pathForm.checkPoints = row.check_points.join(',')
  pathForm.cycle = row.cycle
  ElMessage.info('已加载路径数据至编辑表单')
}

const deletePath = (pathId) => {
  pathList.value = pathList.value.filter(item => item.id !== pathId)
  ElMessage.success('巡检路径已删除')
}

// 水校准数据分析
const hydroDataError = ref('')
const hydroChartOptions = ref(null)

const initHydroChart = () => {
  try {
    if (hydroChartInstance) {
      hydroChartInstance.dispose()
    }
    const chartDom = document.getElementById('hydro-chart')
    if (!chartDom) {
      hydroDataError.value = '图表容器未找到'
      return
    }
    hydroChartInstance = echarts.init(chartDom)
    hydroChartInstance.setOption(hydroChartOptions.value)
    window.addEventListener('resize', handleChartResize)
  } catch (error) {
    hydroDataError.value = '图表初始化失败：' + error.message
    console.error('图表初始化失败', error)
  }
}

const handleChartResize = () => {
  if (hydroChartInstance) {
    hydroChartInstance.resize()
  }
}

const getHydroData = async () => {
  loading.value = true
  hydroDataError.value = ''
  try {
    hydroChartOptions.value = {
      backgroundColor: '#27374d',
      textStyle: { color: '#38bdf8', fontWeight: 500 },
      title: { 
        text: '水文数据趋势分析', 
        left: 'center',
        textStyle: { color: '#38bdf8', fontSize: 18, fontWeight: 600 } 
      },
      tooltip: {
        trigger: 'axis',
        textStyle: { color: '#fff' },
        backgroundColor: 'rgba(15, 23, 42, 0.8)'
      },
      legend: {
        data: ['水位(m)', '流速(m/s)'],
        textStyle: { color: '#38bdf8' },
        top: 30
      },
      grid: {
        left: '5%',
        right: '5%',
        bottom: '8%',
        top: '15%',
        containLabel: true
      },
      xAxis: { 
        type: 'category', 
        data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月'], 
        axisLine: { lineStyle: { color: '#38bdf8' } }, 
        axisLabel: { color: '#e2e8f0', fontSize: 12 },
        splitLine: { lineStyle: { color: '#334155' } }
      },
      yAxis: [
        { 
          type: 'value', 
          name: '水位(m)', 
          axisLine: { lineStyle: { color: '#38bdf8' } }, 
          splitLine: { lineStyle: { color: '#334155' } }, 
          axisLabel: { color: '#e2e8f0', fontSize: 12 },
          nameTextStyle: { color: '#38bdf8' }
        },
        { 
          type: 'value', 
          name: '流速(m/s)', 
          position: 'right', 
          axisLine: { lineStyle: { color: '#10b981' } }, 
          splitLine: { lineStyle: { color: '#334155' } }, 
          axisLabel: { color: '#e2e8f0', fontSize: 12 },
          nameTextStyle: { color: '#10b981' }
        }
      ],
      series: [
        { 
          name: '水位(m)', 
          type: 'line', 
          data: [12.5, 13.2, 14.1, 13.8, 15.2, 14.8, 15.5, 14.9], 
          itemStyle: { color: '#38bdf8' }, 
          lineStyle: { color: '#38bdf8', width: 2 },
          symbol: 'circle',
          symbolSize: 6
        },
        { 
          name: '流速(m/s)', 
          type: 'line', 
          data: [0.8, 0.9, 1.2, 1.1, 0.7, 0.9, 0.8, 1.0], 
          itemStyle: { color: '#10b981' }, 
          lineStyle: { color: '#10b981', width: 2 },
          symbol: 'circle',
          symbolSize: 6,
          yAxisIndex: 1
        }
      ]
    }
    if (hydroChartInstance) {
      hydroChartInstance.setOption(hydroChartOptions.value)
    }
  } catch (error) {
    hydroDataError.value = '获取水文数据失败：' + error.message
    hydroChartOptions.value = {
      backgroundColor: '#27374d',
      textStyle: { color: '#38bdf8', fontWeight: 500 },
      title: { text: '水文数据趋势分析', textStyle: { color: '#38bdf8', fontSize: 16, fontWeight: 600 } },
      xAxis: { type: 'category', data: ['1月', '2月', '3月'], axisLine: { lineStyle: { color: '#38bdf8' } }, axisLabel: { color: '#e2e8f0' } },
      yAxis: { type: 'value', axisLine: { lineStyle: { color: '#38bdf8' } }, splitLine: { lineStyle: { color: '#334155' } }, axisLabel: { color: '#e2e8f0' } },
      series: [
        { name: '水位(m)', type: 'line', data: [12.5, 13.2, 14.1], itemStyle: { color: '#38bdf8' }, lineStyle: { color: '#38bdf8', width: 2 } },
        { name: '流速(m/s)', type: 'line', data: [0.8, 0.9, 1.2], itemStyle: { color: '#10b981' }, lineStyle: { color: '#10b981', width: 2 } }
      ]
    }
  } finally {
    loading.value = false
  }
}

const refreshHydroData = () => {
  getHydroData()
  if (hydroChartInstance) {
    hydroChartInstance.setOption(hydroChartOptions.value)
  }
}

// 生命周期钩子
onMounted(() => {
  getTaskList()
  if (activeMenu.value === '6') {
    setTimeout(() => {
      getHydroData()
      initHydroChart()
    }, 300)
  }
})

onUpdated(() => {
  if (activeMenu.value === '6') {
    setTimeout(() => {
      initHydroChart()
    }, 100)
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleChartResize)
  if (hydroChartInstance) {
    hydroChartInstance.dispose()
    hydroChartInstance = null
  }
})
</script>

<style scoped>
/* 全局重置 */
:global(*) {
  margin: 0 !important;
  padding: 0 !important;
  box-sizing: border-box !important;
}

:global(body), :global(html) {
  width: 100vw !important;
  height: 100vh !important;
  overflow: hidden !important;
  background: #0f172a !important;
  font-size: 14px !important;
}

/* 容器布局 */
:deep(.el-container) {
  width: 100% !important;
  height: 100% !important;
  display: flex !important;
}

:deep(.el-aside) {
  flex: 0 0 220px !important;
  max-width: 220px !important;
  min-width: 220px !important;
  height: 100vh !important;
}

:deep(.el-header) {
  flex: 0 0 60px !important;
  max-height: 60px !important;
  min-height: 60px !important;
}

:deep(.el-main) {
  flex: 1 !important;
  height: calc(100vh - 60px) !important;
  min-height: calc(100vh - 60px) !important;
  padding: 20px !important;
  overflow-y: auto !important;
}

/* 表单样式 */
:deep(.el-form) {
  width: 100% !important;
}

:deep(.el-form-item) {
  width: 100% !important;
  margin-bottom: 16px !important;
  display: flex !important;
  align-items: center !important;
}

:deep(.el-form-item__label) {
  color: #38bdf8 !important;
  font-size: 14px !important;
  width: 100px !important;
  text-align: left !important;
  margin-right: 8px !important;
  font-weight: 500 !important;
}

:deep(.el-form-item__content) {
  margin-left: 0 !important;
  flex: 1 !important;
}

/* 输入框/下拉框样式 */
:deep(.el-input__inner), :deep(.el-select__inner), :deep(.el-date-picker__input) {
  background: #1e293b !important;
  color: #e2e8f0 !important;
  border-color: #38bdf8 !important;
  font-size: 14px !important;
  height: 40px !important;
  line-height: 40px !important;
  padding: 0 16px !important;
  font-weight: 500 !important;
}

:deep(.el-select-dropdown), :deep(.el-date-picker__panel) {
  background: #1e293b !important;
  border-color: #38bdf8 !important;
  color: #e2e8f0 !important;
}

:deep(.el-select-dropdown__item), :deep(.el-date-table-cell) {
  color: #e2e8f0 !important;
  font-weight: 500 !important;
}

:deep(.el-select-dropdown__item:hover), :deep(.el-date-table-cell:hover) {
  background: #27374d !important;
  color: #38bdf8 !important;
}

/* 表格样式 */
:deep(.el-table) {
  --el-table-header-text-color: #38bdf8 !important;
  --el-table-row-hover-bg-color: #27374d !important;
  --el-table-border-color: #334155 !important;
  width: 100% !important;
}

:deep(.el-table__header-wrapper) {
  color: #38bdf8 !important;
  font-weight: 500 !important;
}

:deep(.el-table__row) {
  color: #e2e8f0 !important;
  font-weight: 500 !important;
}

:deep(.el-table__cell) {
  border-color: #334155 !important;
  padding: 14px 18px !important;
  vertical-align: middle !important;
  border-right: 1px solid #334155 !important;
  text-align: center !important;
}

/* 卡片样式 */
:deep(.el-card) {
  --el-card-bg-color: #1e293b !important;
  --el-card-border-color: #38bdf8 !important;
  width: 100% !important;
  padding: 20px !important;
  box-shadow: 0 2px 12px rgba(56, 189, 248, 0.1) !important;
}

/* 按钮样式（保留其他按钮样式） */
:deep(.el-button) {
  font-size: 14px !important;
  padding: 4px 12px !important;
  font-weight: 500 !important;
  vertical-align: middle !important;
  line-height: 1 !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  height: 28px !important;
}

:deep(.el-button--primary) {
  --el-button-bg-color: #38bdf8 !important;
  --el-button-border-color: #38bdf8 !important;
}

:deep(.el-button--danger) {
  --el-button-bg-color: #ef4444 !important;
  --el-button-border-color: #ef4444 !important;
}

:deep(.el-button--success) {
  --el-button-bg-color: #10b981 !important;
  --el-button-border-color: #10b981 !important;
}

/* 进度条样式 */
:deep(.el-progress-bar__outer) {
  background-color: #27374d !important;
  height: 8px !important;
}

:deep(.el-progress-bar__inner) {
  background-color: #38bdf8 !important;
}

/* 标签样式 */
:deep(.el-tag) {
  --el-tag-bg-color: #27374d !important;
  --el-tag-border-color: #38bdf8 !important;
  --el-tag-text-color: #38bdf8 !important;
  padding: 6px 10px !important;
  margin: 0 4px !important;
  font-weight: 500 !important;
}

/* 上传组件样式 */
:deep(.el-upload-dragger) {
  background-color: #27374d !important;
  border: 2px dashed #38bdf8 !important;
  padding: 30px !important;
}

:deep(.el-upload__text) {
  color: #e2e8f0 !important;
  font-weight: 500 !important;
}

/* 分页样式 */
:deep(.el-pagination) {
  width: 100% !important;
  text-align: right !important;
  color: #e2e8f0 !important;
  margin-top: 20px !important;
}

:deep(.el-pagination__sizes), :deep(.el-pagination__total) {
  color: #e2e8f0 !important;
  font-weight: 500 !important;
}

:deep(.el-pagination__prev), :deep(.el-pagination__next), :deep(.el-pagination__item) {
  background: #27374d !important;
  border-color: #38bdf8 !important;
  color: #e2e8f0 !important;
  font-weight: 500 !important;
}

:deep(.el-pagination__item.is-active) {
  background: #38bdf8 !important;
  border-color: #38bdf8 !important;
  color: #0f172a !important;
  font-weight: 600 !important;
}

/* 下拉菜单样式 */
:deep(.el-dropdown-menu) {
  --el-dropdown-menu-bg-color: #1e293b !important;
  --el-dropdown-menu-border-color: #38bdf8 !important;
}

:deep(.el-dropdown-item) {
  --el-dropdown-item-text-color: #94a3b8 !important;
  --el-dropdown-item-hover-bg-color: #27374d !important;
  --el-dropdown-item-hover-text-color: #38bdf8 !important;
  font-weight: 500 !important;
}

/* 加载动画 */
:deep(.el-icon-loading) {
  animation: el-icon-loading-rotate 2s linear infinite;
}

@keyframes el-icon-loading-rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>