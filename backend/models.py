from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 1. 巡检任务模型
class InspectionTask(db.Model):
    __tablename__ = 'inspection_tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    taskName = db.Column(db.String(100), nullable=False)
    taskTime = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="待执行")

# 2. 预警记录模型
class AlertRecord(db.Model):
    __tablename__ = 'alert_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alertType = db.Column(db.String(50), nullable=False)
    alertTime = db.Column(db.String(50), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    confidence = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="未处置")

# 3. 实时告警模型
class RealTimeAlert(db.Model):
    __tablename__ = 'real_time_alerts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alert_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.String(50), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = db.Column(db.String(20), default="未处理")

# 4. 巡检路径模型
class InspectionPath(db.Model):
    __tablename__ = 'inspection_paths'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path_name = db.Column(db.String(100), nullable=False)
    check_points = db.Column(db.String(500), nullable=False)
    cycle = db.Column(db.String(20), default="每日")
    create_time = db.Column(db.String(50), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# 5. 水文校准数据模型
class HydrologyData(db.Model):
    __tablename__ = 'hydrology_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    monitor_point = db.Column(db.String(50), nullable=False)
    water_level = db.Column(db.Float, nullable=False)
    flow = db.Column(db.Float, nullable=False)
    record_time = db.Column(db.String(50), nullable=False)

# 6. 巡检任务详情模型
class TaskDetail(db.Model):
    __tablename__ = 'task_details'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('inspection_tasks.id'), nullable=False)
    check_content = db.Column(db.String(500), nullable=False)
    executor = db.Column(db.String(50), default="系统自动")
    execute_time = db.Column(db.String(50), nullable=True)