from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import random

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 禁用ASCII编码，支持UTF-8
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"  # 设置响应编码
# 配置跨域（允许前端8080端口访问）
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

# 模拟数据库数据
TASKS = [
    {"id": 1, "taskName": "东河段日常巡检", "taskTime": "2025-12-27 09:00", "status": "待执行"},
    {"id": 2, "taskName": "西闸口设备检查", "taskTime": "2025-12-26 14:30", "status": "已完成"},
    {"id": 3, "taskName": "北泵站维护巡检", "taskTime": "2025-12-25 10:00", "status": "执行中"}
]

ALERTS = [
    {"id": 1, "alertType": "闸口异常", "alertTime": "2025-12-27 09:15", "confidence": 98.5, "status": "未处理"},
    {"id": 2, "alertType": "水位超标", "alertTime": "2025-12-26 15:20", "confidence": 95.2, "status": "已处理"}
]

REALTIME_ALERTS = [
    {"id": 1, "alert_type": "设备故障", "content": "水位传感器故障", "create_time": "2025-12-27 10:00"},
    {"id": 2, "alert_type": "水位预警", "content": "水位超过警戒值0.5米", "create_time": "2025-12-27 09:30"}
]

PATHS = [
    {"id": 1, "path_name": "东河段全线巡检", "check_points": ["1号闸口", "2号监测点", "3号泵站"], "cycle": "每日"},
    {"id": 2, "path_name": "西闸口专项检查", "check_points": ["西闸口设备", "备用电源"], "cycle": "每周"}
]

HYDROLOGY_DATA = [
    {"record_time": "1月", "water_level": 12.5, "flow": 0.8},
    {"record_time": "2月", "water_level": 13.2, "flow": 0.9},
    {"record_time": "3月", "water_level": 14.1, "flow": 1.2},
    {"record_time": "4月", "water_level": 13.8, "flow": 1.1},
    {"record_time": "5月", "water_level": 15.2, "flow": 0.7},
    {"record_time": "6月", "water_level": 14.8, "flow": 0.9}
]


# ---------------------- 巡检任务接口 ----------------------
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """获取巡检任务列表"""
    return jsonify(TASKS)


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """创建新巡检任务"""
    data = request.json
    new_task = {
        "id": len(TASKS) + 1,
        "taskName": data.get("taskName", "新巡检任务"),
        "taskTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "待执行"
    }
    TASKS.append(new_task)
    return jsonify(new_task), 201


# ---------------------- 视觉识别接口 ----------------------
@app.route('/api/detect', methods=['POST'])
def detect():
    """视觉识别接口（模拟）"""
    # 模拟识别结果
    result = [
        {"type": "正常设备", "confidence": 0.98},
        {"type": "无异常", "confidence": 0.99}
    ]
    return jsonify({"data": result})


# ---------------------- 预警记录接口 ----------------------
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """获取预警记录"""
    return jsonify(ALERTS)


# ---------------------- 实时告警接口 ----------------------
@app.route('/api/realtime/alerts', methods=['GET'])
def get_realtime_alerts():
    """获取实时告警数据"""
    # 模拟数据（实际项目从数据库获取）
    realtime_alerts = [
        {"id": 1, "alert_type": "设备故障", "content": "水位传感器故障", "create_time": "2025-12-27 10:00"},
        {"id": 2, "alert_type": "水位预警", "content": "水位超过警戒值0.5米", "create_time": "2025-12-27 09:30"}
    ]
    return jsonify(realtime_alerts)


@app.route('/api/alerts/simulate', methods=['POST'])
def simulate_alert():
    """模拟生成实时告警"""
    new_alert = {
        "id": len(REALTIME_ALERTS) + 1,
        "alert_type": random.choice(["设备异常", "水位波动", "闸口故障"]),
        "content": f"模拟告警内容{len(REALTIME_ALERTS)+1}",
        "create_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    REALTIME_ALERTS.append(new_alert)
    return jsonify(new_alert), 201


@app.route('/api/alerts/handle/<int:alert_id>', methods=['POST'])
def handle_alert(alert_id):
    """处理告警"""
    # 先查普通预警
    for alert in ALERTS:
        if alert.get("id") == alert_id:
            alert["status"] = "已处理"
            return jsonify({"msg": "处理成功"})
    # 再查实时告警
    for alert in REALTIME_ALERTS:
        if alert.get("id") == alert_id:
            alert["status"] = "已处理"
            return jsonify({"msg": "处理成功"})
    return jsonify({"msg": "告警不存在"}), 404


# ---------------------- 巡检路径接口 ----------------------
@app.route('/api/paths', methods=['GET'])
def get_paths():
    """获取巡检路径"""
    return jsonify(PATHS)


@app.route('/api/paths', methods=['POST'])
def create_path():
    """创建巡检路径"""
    data = request.json
    new_path = {
        "id": len(PATHS) + 1,
        "path_name": data.get("path_name", "新巡检路径"),
        "check_points": data.get("check_points", ["默认点1", "默认点2"]),
        "cycle": data.get("cycle", "每日")
    }
    PATHS.append(new_path)
    return jsonify(new_path), 201


# ---------------------- 水文数据接口 ----------------------
@app.route('/api/hydrology', methods=['GET'])
def get_hydrology():
    """获取水文数据"""
    return jsonify(HYDROLOGY_DATA)

# 新增：用户数据（实际项目用数据库）
USERS = {
    "admin": {
        "password": "123456",  # 实际项目用加密存储
        "role": "admin",
        "username": "管理员"
    }
}

# 新增：登录接口
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username not in USERS:
        return jsonify({"code": 400, "msg": "用户名不存在"}), 400
    if USERS[username]["password"] != password:
        return jsonify({"code": 400, "msg": "密码错误"}), 400
    
    # 生成模拟token（实际项目用JWT）
    token = f"token_{username}_{datetime.datetime.now().timestamp()}"
    return jsonify({
        "code": 200,
        "msg": "登录成功",
        "data": {
            "token": token,
            "userInfo": {
                "username": USERS[username]["username"],
                "role": USERS[username]["role"]
            }
        }
    })

# 新增：退出登录接口
@app.route('/api/logout', methods=['POST'])
def logout():
    # 实际项目需销毁token
    return jsonify({"code": 200, "msg": "退出成功"})

if __name__ == '__main__':
    # 启动服务，端口8881（与前端配置一致）
    app.run(host='0.0.0.0', port=8881, debug=True)