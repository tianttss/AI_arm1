# ARM BOX Version 1

机械臂视觉搬运项目开发记录（Version 1）

---

# 项目目标

使用实验箱机械臂与单目摄像头完成：

## 任务1

识别仓库1中的数字积木。

例如：

```text
6 2 4
```

识别后按照：

```text
6 → 4 → 2
```

顺序搬运至仓库2。

---

## 任务2

识别图案积木。

类别包括：

* 动物
* 水果
* 蔬菜
* 字母
* 文字
* 车标

识别后选择指定类别并搬运至仓库2。

---

# 当前完成情况

## 已完成

### 1. SSH远程控制实验箱

通过：

```bash
ssh linux@实验箱IP
```

远程访问实验箱。

---

### 2. 分析官方控制源码

分析目录：

```text
~/Project/FS_AIARM
```

定位机械臂控制协议。

找到关键命令：

```text
30 02 07 01 55 a1 93
```

用于控制单个舵机。

---

### 3. 完成Python控制程序

实现：

* 串口通信
* CRC校验
* 单舵机控制
* 多舵机控制

完全脱离官方GUI。

符合课程要求：

```text
禁止使用官方搬运接口
允许使用底层舵机控制
```

---

### 4. 完成舵机映射

| 编号 | 功能   |
| -- | ---- |
| 1  | 夹爪开合 |
| 2  | 夹爪旋转 |
| 3  | 腕关节  |
| 4  | 小臂关节 |
| 5  | 肩关节  |
| 6  | 底座旋转 |

---

### 5. 完成点位标定工具

可通过命令：

```text
set
add
sub
save
```

实时调整机械臂位置。

自动保存标定结果。

---

### 6. 已完成点位

```python
W1_1_PICK = [110, 140, 210, 60, 140, 43]

W2_1_PLACE = [110, 110, 35, 220, 130, 125]
```

---

# 文件说明

---

## joint_test_one.py

单舵机测试工具。

功能：

```text
测试舵机编号
测试舵机方向
测试舵机范围
```

运行：

```bash
python3 joint_test_one.py
```

示例：

```text
1 20
1 150
```

---

## arm_control_named.py

机械臂控制库。

封装接口：

```python
open_gripper()

close_gripper()

gripper_rotate()

wrist()

elbow()

shoulder()

base()
```

功能：

```text
机械臂底层控制
机械臂姿态控制
机械臂运动测试
```

后续视觉识别结果将直接调用此文件。

---

## calibrate_points.py

机械臂点位标定工具。

运行：

```bash
python3 calibrate_points.py
```

常用命令：

```text
show

set 6 140

add 5 5

sub 4 5

save W1_2_PICK
```

保存结果：

```python
W1_2_PICK = [...]
```

自动写入：

```text
calibration_points.py
```

---

## calibration_points.py

保存所有机械臂点位。

格式：

```python
W1_1_PICK = [...]

W1_2_PICK = [...]

W2_1_PLACE = [...]

W2_2_PLACE = [...]
```

后续搬运程序直接读取。

---

# 下一步计划

## 第一阶段

完成全部点位标定：

```text
W1_1_PICK
W1_2_PICK
W1_3_PICK
W1_4_PICK

W2_1_PLACE
W2_2_PLACE
W2_3_PLACE
W2_4_PLACE
```

---

## 第二阶段

采集数字积木数据集。

训练：

```text
YOLOv8
```

数字识别模型。

---

## 第三阶段

采集图案积木数据集。

训练：

```text
动物
水果
蔬菜
车标
字母
文字
```

分类模型。

---

## 第四阶段

实现完整流程：

```text
摄像头采集

↓

YOLO识别

↓

排序/分类

↓

机械臂抓取

↓

机械臂放置

↓

任务完成
```

---

# Version

Version 1

创建时间：

2026-06-05

作者：

Liangchen

