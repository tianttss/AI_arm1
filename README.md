# AI_arm1
人工智能课设
# 机械臂物料识别搬运任务

**项目类型**：低难度（机械臂）  
**团队规模**：2人  
**核心技术**：计算机视觉 + 机器人运动控制

---

## 目录

1. [任务要求](#一任务要求)
2. [关键限制](#二关键限制)
3. [系统架构](#三系统架构)
4. [详细步骤流程](#四详细步骤流程)
   - [第一阶段：环境搭建与硬件熟悉](#第一阶段环境搭建与硬件熟悉建议第12天)
   - [第二阶段：逆运动学实现](#第二阶段逆运动学ik实现建议第35天)
   - [第三阶段：视觉识别模型训练](#第三阶段视觉识别模型训练建议第47天)
   - [第四阶段：坐标计算与抓取规划](#第四阶段坐标计算与抓取规划建议第78天)
   - [第五阶段：完整搬运流程实现](#第五阶段完整搬运流程实现建议第810天)
   - [第六阶段：联调测试与文档](#第六阶段联调测试与文档建议第1014天)
5. [推荐技术栈](#五推荐技术栈)
6. [两人分工建议](#六两人分工建议)
7. [验收要求对应说明](#七验收要求对应说明)

---

## 一、任务要求

### 任务一：数字积木排序搬运
- 对仓库1中 **2-4块带有数字的积木** 进行识别
- 将识别结果从**大到小排序**
- 按照排序顺序依次搬运至仓库2

### 任务二：类别积木识别搬运
- 对4块带有**动物、蔬菜、水果、文字、字母、车标**的积木进行识别
- 识别后**指定一种类别**（例如：熊猫图案和老虎图案归为同一"动物类"）
- 将该类别的**所有积木**夹取到仓库2

---

## 二、关键限制

> ⚠️ **以下限制是验收时的重要检查点，必须严格遵守！**

| 限制项 | 具体要求 | 违规后果 |
|--------|----------|----------|
| 代码运行环境 | 所有代码部署在**自己的PC机**上，不使用实验箱中的电脑 | 直接扣分 |
| 识别算法 | 必须**自己采集数据、自己训练模型**，不得使用现成模型和接口 | 直接扣分 |
| 机械臂控制 | 必须**自己实现逆运动学算法**，不允许使用内置搬运快捷指令 | 直接扣分 |
| 仅允许指令 | 只能使用**读取/控制舵机位置姿态**的基础指令 | — |
| 文档留存 | 保留数据集、训练日志截图、测试截图 | 无法通过检查 |

---

## 三、系统架构

```
┌─────────────────────────────────────────────────────┐
│                    自己的 PC 机                       │
│                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐  │
│  │  摄像头   │───▶│ 目标检测  │───▶│ 坐标转换     │  │
│  │  画面采集 │    │ 自训练模型│    │ 像素→世界坐标│  │
│  └──────────┘    └──────────┘    └──────┬───────┘  │
│                                         │           │
│  ┌──────────────────────────────────────▼───────┐  │
│  │              逆运动学求解（IK）                │  │
│  │    目标坐标 (x,y,z) → 各关节角度 (θ1,θ2...)  │  │
│  └──────────────────────────┬───────────────────┘  │
│                             │                       │
└─────────────────────────────┼───────────────────────┘
                              │ 串口/网络
                    ┌─────────▼─────────┐
                    │     机械臂硬件      │
                    │  舵机控制指令执行   │
                    └───────────────────┘
```

---

## 四、详细步骤流程

### 第一阶段：环境搭建与硬件熟悉（建议第1-2天）

#### 1.1 连接硬件与通信测试

1. 确认机械臂与 PC 的通信方式（通常为 USB 串口或网口）
2. 安装对应驱动，使用以下命令确认串口可用：

```bash
# Linux 查看串口设备
ls /dev/ttyUSB*

# Windows 在设备管理器中查看 COM 口
```

3. 打开摄像头，确认画面正常（分辨率、帧率）

#### 1.2 熟悉舵机控制指令

查阅机械臂说明文档，找到以下两类**允许使用**的指令：

- **读取指令**：读取某个舵机当前角度/位置
- **控制指令**：设置某个舵机到目标角度

编写简单测试脚本，逐一让各关节运动：

```python
import serial
import time

# 建立串口连接（根据实际设备调整端口和波特率）
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

def set_servo_angle(servo_id, angle):
    """发送舵机控制指令（根据实际协议实现）"""
    # 此处替换为机械臂实际通信协议
    pass

def get_servo_angle(servo_id):
    """读取舵机当前角度"""
    pass

# 测试：让1号舵机（底座）转到90度
set_servo_angle(servo_id=1, angle=90)
time.sleep(1)
print(f"当前角度: {get_servo_angle(1)}")
```

#### 1.3 记录各舵机物理极限

| 舵机编号 | 功能 | 最小角度 | 最大角度 | 备注 |
|----------|------|----------|----------|------|
| 1 | 底座旋转 | — | — | 待测量 |
| 2 | 大臂俯仰 | — | — | 待测量 |
| 3 | 小臂俯仰 | — | — | 待测量 |
| 4 | 腕部旋转 | — | — | 待测量 |
| 5 | 夹爪开合 | — | — | 待测量 |

---

### 第二阶段：逆运动学（IK）实现（建议第3-5天）

> 这是整个项目**最核心也最难**的部分，必须在视觉联调之前完成！

#### 2.1 建立机械臂运动学模型

1. 测量或查阅各连杆长度 L1、L2、L3……
2. 确认关节数量（桌面机械臂通常为 4-5 个自由度）
3. 建立 DH 参数表：

| 关节 i | θᵢ（关节角） | dᵢ（连杆偏移） | aᵢ（连杆长度） | αᵢ（扭转角） |
|--------|-------------|--------------|--------------|-------------|
| 1 | 变量 | d1 | 0 | 90° |
| 2 | 变量 | 0 | L2 | 0° |
| 3 | 变量 | 0 | L3 | 0° |
| … | … | … | … | … |

#### 2.2 实现正运动学（FK，用于验证）

```python
import numpy as np

def forward_kinematics(theta1, theta2, theta3, L1, L2, L3):
    """
    正运动学：已知各关节角度，计算末端坐标
    theta: 各关节角度（度）
    L: 各连杆长度（mm）
    """
    t1 = np.radians(theta1)
    t2 = np.radians(theta2)
    t3 = np.radians(theta3)
    
    x = np.cos(t1) * (L2 * np.cos(t2) + L3 * np.cos(t2 + t3))
    y = np.sin(t1) * (L2 * np.cos(t2) + L3 * np.cos(t2 + t3))
    z = L1 + L2 * np.sin(t2) + L3 * np.sin(t2 + t3)
    
    return x, y, z
```

#### 2.3 实现逆运动学（IK，核心算法）

对 4-5 DOF 桌面机械臂使用**解析法**：

```python
import numpy as np

def inverse_kinematics(target_x, target_y, target_z, L1, L2, L3):
    """
    逆运动学解析解：给定目标坐标，求各关节角度
    
    参数:
        target_x, target_y, target_z: 目标末端坐标（mm）
        L1: 底座到大臂关节的高度
        L2: 大臂长度
        L3: 小臂长度
    
    返回:
        theta1, theta2, theta3: 各关节角度（度）
    """
    # 第一步：底座旋转角（绕Z轴）
    theta1 = np.degrees(np.arctan2(target_y, target_x))
    
    # 第二步：将3D问题投影到2D平面
    r = np.sqrt(target_x**2 + target_y**2)  # 水平距离
    h = target_z - L1                        # 相对于大臂关节的高度
    
    # 第三步：用余弦定理求 theta3（小臂关节）
    D = (r**2 + h**2 - L2**2 - L3**2) / (2 * L2 * L3)
    
    # 检查目标是否可达
    if abs(D) > 1:
        raise ValueError(f"目标点不可达！D={D:.3f}，超出工作空间。")
    
    # 选择"肘部向上"解
    theta3 = np.degrees(np.arctan2(-np.sqrt(1 - D**2), D))
    
    # 第四步：求 theta2（大臂关节）
    theta2 = np.degrees(
        np.arctan2(h, r) - np.arctan2(
            L3 * np.sin(np.radians(theta3)),
            L2 + L3 * np.cos(np.radians(theta3))
        )
    )
    
    return theta1, theta2, theta3


# 验证：正逆运动学互相校验
if __name__ == "__main__":
    L1, L2, L3 = 100, 150, 120  # 替换为实际连杆长度（mm）
    target = (200, 100, 150)
    
    t1, t2, t3 = inverse_kinematics(*target, L1, L2, L3)
    print(f"IK 求解角度: θ1={t1:.2f}°, θ2={t2:.2f}°, θ3={t3:.2f}°")
    
    # 用FK反向验证
    x, y, z = forward_kinematics(t1, t2, t3, L1, L2, L3)
    print(f"FK 验证结果: x={x:.2f}, y={y:.2f}, z={z:.2f}")
    print(f"目标坐标:   x={target[0]}, y={target[1]}, z={target[2]}")
    print(f"误差: Δx={abs(x-target[0]):.3f}, Δy={abs(y-target[1]):.3f}, Δz={abs(z-target[2]):.3f}")
```

#### 2.4 手眼标定（Eye-to-Hand Calibration）

建立**摄像头像素坐标 → 机械臂世界坐标**的映射关系：

**标定步骤：**

1. 在工作台上放置标定板（棋盘格）
2. 让机械臂夹爪依次点击 8-12 个已知位置
3. 记录每个点的**像素坐标**和**机械臂世界坐标**
4. 用最小二乘法求变换矩阵

```python
import numpy as np

def calibrate_hand_eye(pixel_points, world_points):
    """
    手眼标定：求像素坐标到世界坐标的仿射变换矩阵
    
    pixel_points: [[u1,v1], [u2,v2], ...] 像素坐标列表
    world_points: [[x1,y1], [x2,y2], ...] 对应世界坐标列表
    """
    n = len(pixel_points)
    A = []
    b_x, b_y = [], []
    
    for (u, v), (x, y) in zip(pixel_points, world_points):
        A.append([u, v, 1, 0, 0, 0])
        A.append([0, 0, 0, u, v, 1])
        b_x.append(x)
        b_y.append(y)
    
    A = np.array(A)
    b = np.array(b_x + b_y)
    
    # 最小二乘求解
    result, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    M = result[:3], result[3:]
    return np.array(M)  # 2×3 变换矩阵

def pixel_to_world(u, v, M):
    """利用标定矩阵将像素坐标转换为世界坐标"""
    uv1 = np.array([u, v, 1])
    world_x = M[0] @ uv1
    world_y = M[1] @ uv1
    return world_x, world_y
```

---

### 第三阶段：视觉识别模型训练（建议第4-7天，可与第二阶段并行）

#### 3.1 任务一：数字识别模型

**数据采集：**
- 将数字积木放在仓库1的实际位置
- 在不同光照、角度下拍摄，每个数字至少 **150-200 张**
- 模拟实际部署场景（相机固定位置）

**数据标注（使用 LabelImg）：**

```bash
pip install labelImg
labelImg
```

- 标注格式：YOLO 格式
- 类别：`1`, `2`, `3`, `4`（根据实际积木数字）

**目录结构：**

```
number_dataset/
├── images/
│   ├── train/     # 80% 训练集
│   └── val/       # 20% 验证集
├── labels/
│   ├── train/
│   └── val/
└── number.yaml    # 数据集配置文件
```

**number.yaml 配置：**

```yaml
path: ./number_dataset
train: images/train
val: images/val

nc: 4  # 类别数量
names: ['1', '2', '3', '4']
```

**训练 YOLOv8 模型：**

```bash
pip install ultralytics

# 开始训练
yolo train \
  data=number.yaml \
  model=yolov8n.pt \
  epochs=100 \
  imgsz=640 \
  batch=16 \
  name=number_model
```

> 📸 **注意保存训练日志截图和 loss 曲线图，验收时需要展示！**

#### 3.2 任务二：类别识别模型

**类别定义（示例）：**

| 大类 | 包含图案示例 |
|------|------------|
| animal（动物） | 熊猫、老虎、狗、猫… |
| vegetable（蔬菜） | 白菜、萝卜、茄子… |
| fruit（水果） | 苹果、香蕉、草莓… |
| text（文字） | 中文汉字积木 |
| letter（字母） | 英文字母 A-Z |
| logo（车标） | 奔驰、宝马、丰田… |

**category.yaml 配置：**

```yaml
path: ./category_dataset
train: images/train
val: images/val

nc: 6
names: ['animal', 'vegetable', 'fruit', 'text', 'letter', 'logo']
```

**训练命令：**

```bash
yolo train \
  data=category.yaml \
  model=yolov8n.pt \
  epochs=150 \
  imgsz=640 \
  name=category_model
```

#### 3.3 模型测试与评估

```python
from ultralytics import YOLO
import cv2

# 加载训练好的模型
model = YOLO('runs/detect/number_model/weights/best.pt')

# 测试单张图片
results = model('test_image.jpg', conf=0.5)
results[0].show()  # 显示检测结果

# 输出各指标
print(f"mAP50: {results[0].boxes.conf.mean():.3f}")
```

> 📸 **保存测试截图！** 包括：检测框正确、数字/类别标签正确的多组截图。

---

### 第四阶段：坐标计算与抓取规划（建议第7-8天）

#### 4.1 从检测结果获取积木坐标

```python
from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO('best.pt')
cap = cv2.VideoCapture(0)

def detect_blocks(frame):
    """检测画面中所有积木，返回位置和类别信息"""
    results = model(frame, conf=0.5)
    blocks = []
    
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cx = (x1 + x2) / 2  # 目标框中心像素x
        cy = (y1 + y2) / 2  # 目标框中心像素y
        label = model.names[int(box.cls)]
        confidence = float(box.conf)
        
        # 转换为世界坐标
        world_x, world_y = pixel_to_world(cx, cy, calibration_matrix)
        
        blocks.append({
            "label": label,
            "pixel": (cx, cy),
            "world": (world_x, world_y),
            "confidence": confidence
        })
    
    return blocks
```

#### 4.2 任务一：排序逻辑

```python
def task1_sort_and_plan(blocks):
    """
    任务一：检测数字积木，按数字从大到小排序，返回搬运顺序
    """
    # 过滤出数字积木（确保标签是数字）
    number_blocks = [b for b in blocks if b["label"].isdigit()]
    
    # 从大到小排序
    sorted_blocks = sorted(number_blocks, key=lambda b: int(b["label"]), reverse=True)
    
    print("搬运顺序（从大到小）：")
    for i, block in enumerate(sorted_blocks):
        print(f"  第{i+1}个：数字 {block['label']} at {block['world']}")
    
    return sorted_blocks
```

#### 4.3 任务二：分类筛选逻辑

```python
def task2_filter_category(blocks, target_category):
    """
    任务二：筛选出指定类别的所有积木
    target_category: 如 'animal', 'fruit' 等
    """
    target_blocks = [b for b in blocks if b["label"] == target_category]
    
    print(f"类别 '{target_category}' 共检测到 {len(target_blocks)} 块积木")
    for block in target_blocks:
        print(f"  位置: {block['world']}, 置信度: {block['confidence']:.2f}")
    
    return target_blocks
```

---

### 第五阶段：完整搬运流程实现（建议第8-10天）

#### 5.1 单次 Pick-and-Place 流程

```python
def pick_and_place(robot, source_pos, target_pos, z_hover=80, z_pick=10):
    """
    单次抓取并放置流程
    
    robot: 机械臂控制对象
    source_pos: 积木位置 (x, y) mm
    target_pos: 目标位置 (x, y) mm
    z_hover: 悬停高度（抓取前/后）mm
    z_pick: 抓取高度（下降到积木）mm
    """
    # 步骤1：移动到积木上方（悬停位）
    angles = inverse_kinematics(source_pos[0], source_pos[1], z_hover, L1, L2, L3)
    robot.move_to_angles(*angles)
    robot.wait_until_done()
    
    # 步骤2：夹爪张开
    robot.open_gripper()
    
    # 步骤3：下降到抓取高度
    angles = inverse_kinematics(source_pos[0], source_pos[1], z_pick, L1, L2, L3)
    robot.move_to_angles(*angles)
    robot.wait_until_done()
    
    # 步骤4：夹爪闭合（抓取）
    robot.close_gripper()
    import time; time.sleep(0.5)  # 等待夹紧
    
    # 步骤5：上升（带物离开）
    angles = inverse_kinematics(source_pos[0], source_pos[1], z_hover, L1, L2, L3)
    robot.move_to_angles(*angles)
    robot.wait_until_done()
    
    # 步骤6：移动到目标位置上方
    angles = inverse_kinematics(target_pos[0], target_pos[1], z_hover, L1, L2, L3)
    robot.move_to_angles(*angles)
    robot.wait_until_done()
    
    # 步骤7：下降到放置高度
    angles = inverse_kinematics(target_pos[0], target_pos[1], z_pick + 20, L1, L2, L3)
    robot.move_to_angles(*angles)
    robot.wait_until_done()
    
    # 步骤8：夹爪张开（放置）
    robot.open_gripper()
    time.sleep(0.3)
    
    # 步骤9：上升回到悬停位
    angles = inverse_kinematics(target_pos[0], target_pos[1], z_hover, L1, L2, L3)
    robot.move_to_angles(*angles)
    robot.wait_until_done()
    
    print(f"完成搬运: {source_pos} → {target_pos}")
```

#### 5.2 任务一完整流程

```python
def run_task1(robot, camera, warehouse2_positions):
    """
    任务一主流程：识别数字积木 → 排序 → 依次搬运
    warehouse2_positions: 仓库2的放置位置列表 [(x1,y1), (x2,y2), ...]
    """
    print("=== 任务一开始 ===")
    
    # 1. 拍照识别
    frame = camera.capture()
    blocks = detect_blocks(frame)
    
    # 2. 排序
    sorted_blocks = task1_sort_and_plan(blocks)
    
    if not sorted_blocks:
        print("未检测到数字积木，任务终止")
        return
    
    # 3. 依次搬运
    for i, block in enumerate(sorted_blocks):
        source = block["world"]
        target = warehouse2_positions[i]
        print(f"\n搬运第{i+1}个：数字{block['label']} {source} → {target}")
        pick_and_place(robot, source, target)
    
    print("\n=== 任务一完成 ===")
```

#### 5.3 任务二完整流程

```python
def run_task2(robot, camera, target_category, warehouse2_positions):
    """
    任务二主流程：识别类别积木 → 筛选 → 搬运指定类别
    """
    print(f"=== 任务二开始，目标类别：{target_category} ===")
    
    # 1. 拍照识别
    frame = camera.capture()
    blocks = detect_blocks(frame)
    
    # 2. 筛选目标类别
    target_blocks = task2_filter_category(blocks, target_category)
    
    if not target_blocks:
        print(f"未检测到类别 '{target_category}' 的积木，任务终止")
        return
    
    # 3. 搬运该类别所有积木
    for i, block in enumerate(target_blocks):
        source = block["world"]
        target = warehouse2_positions[i]
        print(f"\n搬运第{i+1}个：{target_category} {source} → {target}")
        pick_and_place(robot, source, target)
    
    print(f"\n=== 任务二完成，共搬运 {len(target_blocks)} 块 ===")
```

---

### 第六阶段：联调测试与文档（建议第10-14天）

#### 6.1 联调测试清单

- [ ] IK 求解误差 < 5mm（FK 反向验证）
- [ ] 手眼标定误差 < 10px（重投影误差）
- [ ] 数字识别准确率 > 95%
- [ ] 类别识别准确率 > 90%
- [ ] 抓取成功率 > 85%（多次重复测试）
- [ ] 完整任务一流程（2-4个积木）成功运行 ≥ 3 次
- [ ] 完整任务二流程成功运行 ≥ 3 次
- [ ] 不同光照条件下测试稳定性

#### 6.2 常见问题与调试方法

| 问题 | 排查方向 |
|------|----------|
| 积木识别不到 | 检查光照、调低置信度阈值、补充该角度训练数据 |
| 抓取位置偏移 | 重新标定手眼矩阵，检查相机是否松动 |
| 机械臂不到达目标 | 检查 IK 解是否超出关节限位，调整目标Z轴高度 |
| 积木抓起后掉落 | 增大夹爪闭合力度或等待时间，检查积木尺寸与夹爪匹配 |
| 串口通信失败 | 检查波特率、端口号、驱动安装 |

#### 6.3 文档写作要点（占20分）

文档应包含以下内容：

1. **系统总体架构图**（软件模块 + 硬件连接）
2. **数据集说明**：数量统计、类别分布直方图、标注方式截图
3. **训练日志**：loss 曲线、mAP 指标截图
4. **逆运动学推导**：DH 参数、求解步骤公式
5. **手眼标定方法**：标定点分布图、变换矩阵结果
6. **测试结果**：识别截图、搬运过程截图/视频截帧
7. **分工说明**：每位成员负责的模块

---

## 五、推荐技术栈

| 模块 | 推荐工具 | 版本建议 |
|------|----------|----------|
| 视觉检测框架 | YOLOv8 (ultralytics) | ≥ 8.0 |
| 数据标注工具 | LabelImg | 最新版 |
| 串口通信 | pyserial | ≥ 3.5 |
| 图像处理 | OpenCV | ≥ 4.5 |
| 数值计算 | NumPy | ≥ 1.21 |
| 科学计算 | SciPy | ≥ 1.7 |
| 开发语言 | Python | 3.8 – 3.11 |
| 深度学习框架 | PyTorch | ≥ 1.12 |

**安装命令：**

```bash
pip install ultralytics opencv-python pyserial numpy scipy torch torchvision
```

---

## 六、两人分工建议

| 时间段 | 同学 A（视觉方向） | 同学 B（控制方向） |
|--------|------------------|--------------------|
| 第1-2天 | 环境搭建、摄像头测试 | 串口通信、舵机控制测试 |
| 第3-5天 | 数据采集、LabelImg标注 | 逆运动学推导与实现 |
| 第6-7天 | YOLOv8训练与调参 | 手眼标定实现 |
| 第8-9天 | 识别结果坐标转换 | Pick-and-Place 流程 |
| 第10-11天 | 联合调试（视觉+控制） | 联合调试（视觉+控制） |
| 第12-14天 | 撰写文档视觉部分 | 撰写文档控制部分 |

---

## 七、验收要求对应说明

| 验收项 | 分值 | 对应工作 |
|--------|------|----------|
| 任务一识别并排序正确 | 20分 | 数字识别模型 + 排序算法 |
| 任务二识别并分类正确 | 20分 | 类别识别模型 + 筛选逻辑 |
| 任务一、二搬运完成 | 20分 | IK算法 + 手眼标定 + Pick-and-Place |
| 文档 | 20分 | 数据集/训练日志/测试截图/推导过程 |
| **合计** | **80分** | — |

> 💡 **最重要提示**：逆运动学 + 手眼标定是核心难点，务必优先搞定。视觉识别相对独立，可以并行推进。IK 若不能正常工作，后续所有搬运任务都无从谈起。

---

*文档版本：v1.0 | 最后更新：2026年6月*
