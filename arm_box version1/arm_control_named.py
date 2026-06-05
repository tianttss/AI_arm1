import serial
import time

PORT = "/dev/ttyS4"
BAUD = 115200

# ====== 你实测得到的安全值 ======
GRIPPER_OPEN = 20
GRIPPER_CLOSE = 150

# 初始安全姿态，先取比较保守的竖直姿态
# 顺序是：[夹爪, 夹爪旋转, 腕部, 小臂, 肩关节, 底座]
HOME = [20, 125, 125, 125, 125, 125]


def crc8(data):
    crc = 0
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ 0x07) & 0xff
            else:
                crc = (crc << 1) & 0xff
    return crc


def to_bytes(hex_str):
    return bytes([int(x, 16) for x in hex_str.split()])


def send_cmd(ser, label, hex_str):
    payload = to_bytes(hex_str)
    frame = payload + bytes([crc8(payload)])

    print("")
    print(label)
    print("TX:", frame.hex())

    ser.write(frame)
    ser.flush()
    time.sleep(0.45)


def move_servo(ser, servo_id, value):
    if value < 0:
        value = 0
    if value > 250:
        value = 250

    cmd = "30 02 07 01 55 a1 93 %02x %02x" % (servo_id, value)
    send_cmd(ser, "servo%d -> %d" % (servo_id, value), cmd)


# ====== 真实关节封装 ======

def gripper(ser, value):
    # servo1：夹爪开合，20张开，150闭合
    move_servo(ser, 1, value)


def gripper_rotate(ser, value):
    # servo2：夹爪旋转，小=逆时针，大=顺时针
    move_servo(ser, 2, value)


def wrist(ser, value):
    # servo3：腕部上下，20最上，250最下
    move_servo(ser, 3, value)


def elbow(ser, value):
    # servo4：小臂关节，125左右竖直向上
    move_servo(ser, 4, value)


def shoulder(ser, value):
    # servo5：肩关节/大臂，10~230，125左右竖直向上
    move_servo(ser, 5, value)


def base(ser, value):
    # servo6：底座旋转，小=顺时针，大=逆时针
    move_servo(ser, 6, value)


def open_gripper(ser):
    gripper(ser, GRIPPER_OPEN)


def close_gripper(ser):
    gripper(ser, GRIPPER_CLOSE)


def move_pose(ser, pose, delay=0.45):
    """
    pose顺序：
    [夹爪, 夹爪旋转, 腕部, 小臂, 肩关节, 底座]
    """
    gripper(ser, pose[0])
    time.sleep(delay)

    gripper_rotate(ser, pose[1])
    time.sleep(delay)

    wrist(ser, pose[2])
    time.sleep(delay)

    elbow(ser, pose[3])
    time.sleep(delay)

    shoulder(ser, pose[4])
    time.sleep(delay)

    base(ser, pose[5])
    time.sleep(delay)


def move_pose_safe(ser, pose):
    """
    更安全的移动顺序：
    先抬起肩/小臂/腕部，再转底座，再调整到目标。
    """
    print("\n=== move safe ===")

    # 先抬起来，避免扫到桌面
    shoulder(ser, 125)
    elbow(ser, 125)
    wrist(ser, 80)
    time.sleep(1)

    # 再转底座
    base(ser, pose[5])
    time.sleep(1)

    # 再调整姿态
    shoulder(ser, pose[4])
    elbow(ser, pose[3])
    wrist(ser, pose[2])
    gripper_rotate(ser, pose[1])
    gripper(ser, pose[0])


def home(ser):
    print("\n=== HOME ===")
    move_pose_safe(ser, HOME)


def test_basic(ser):
    print("\n=== basic test ===")

    print("open gripper")
    open_gripper(ser)
    time.sleep(1)

    print("close gripper")
    close_gripper(ser)
    time.sleep(1)

    print("open gripper")
    open_gripper(ser)
    time.sleep(1)

    print("base test")
    base(ser, 110)
    time.sleep(1)
    base(ser, 140)
    time.sleep(1)
    base(ser, 125)
    time.sleep(1)


def main():
    ser = serial.Serial(PORT, BAUD, timeout=1)

    try:
        print("Connected:", PORT)

        # 先回安全姿态
        home(ser)

        # 基础测试：夹爪开合 + 底座小范围转动
        test_basic(ser)

        print("\nDone")

    finally:
        ser.close()
        print("serial closed")


if __name__ == "__main__":
    main()
