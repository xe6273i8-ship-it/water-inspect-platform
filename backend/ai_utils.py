from ultralytics import YOLO
import cv2
import os

# 加载YOLO模型（先用官方轻量版测试，后续可替换为自定义水利模型）
model = YOLO('yolov8n.pt')

def detect_water_defect(image_path):
    """
    水利设施缺陷识别
    :param image_path: 图片本地路径
    :return: 识别结果列表（包含类型、置信度）
    """
    # 校验图片是否存在
    if not os.path.exists(image_path):
        return []
    
    # 读取图片并推理
    img = cv2.imread(image_path)
    results = model(img)
    
    # 解析结果（临时用通用类别，后续替换为水利专属标签：水位异常、裂缝、油污等）
    defect_list = []
    for r in results:
        for box in r.boxes:
            cls_name = model.names[int(box.cls[0])]
            # 筛选需要预警的类别（示例：可自定义）
            if cls_name in ['person', 'bottle', 'chair']:
                defect_list.append({
                    "type": cls_name,
                    "confidence": float(box.conf[0])
                })
    return defect_list