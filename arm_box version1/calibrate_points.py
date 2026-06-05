import serial
import time

PORT = "/dev/ttyS4"
BAUD = 115200

OUT_FILE = "calibration_points.py"

# 顺序：[夹爪, 夹爪旋转, 腕部, 小臂, 肩关节, 底座]
pose = [20, 125, 125, 125, 125, 125]

names = [
    "gripper",
    "gripper_rotate",
    "wrist",
    "elbow",
    "shoulder",
    "base"
]


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

    print(label)
    print("TX:", frame.hex())

    ser.write(frame)
    ser.flush()
    time.sleep(0.3)


def move_servo(ser, servo_id, value):
    if value < 0:
        value = 0
    if value > 250:
        value = 250

    cmd = "30 02 07 01 55 a1 93 %02x %02x" % (servo_id, value)
    send_cmd(ser, "servo%d -> %d" % (servo_id, value), cmd)


def apply_pose(ser):
    for i in range(6):
        move_servo(ser, i + 1, pose[i])
        time.sleep(0.15)


def show_pose():
    print("")
    print("当前姿态：")
    print("[夹爪, 夹爪旋转, 腕部, 小臂, 肩关节, 底座]")
    print(pose)
    print("")
    for i in range(6):
        print("%d: %s = %d" % (i + 1, names[i], pose[i]))


def save_point(point_name):
    with open(OUT_FILE, "a") as f:
        f.write("%s = %s\n" % (point_name, str(pose)))
    print("已保存到 %s: %s = %s" % (OUT_FILE, point_name, str(pose)))


def help_text():
    print("")
    print("命令说明：")
    print("  show                 显示当前姿态")
    print("  move                 发送当前姿态到机械臂")
    print("  set 编号 数值         修改某个舵机值，例如：set 6 140")
    print("  add 编号 步长         增加某个舵机值，例如：add 6 5")
    print("  sub 编号 步长         减少某个舵机值，例如：sub 6 5")
    print("  save 名称            保存当前姿态，例如：save W1_1_PICK")
    print("  q                    退出")
    print("")
    print("编号对应：")
    print("  1 夹爪开合：20开，150闭")
    print("  2 夹爪旋转")
    print("  3 腕部上下")
    print("  4 小臂关节")
    print("  5 肩关节/大臂")
    print("  6 底座旋转")
    print("")


def main():
    ser = serial.Serial(PORT, BAUD, timeout=1)

    try:
        help_text()
        show_pose()

        while True:
            cmd = input("calib> ").strip()

            if cmd == "":
                continue

            if cmd == "q":
                break

            if cmd == "help":
                help_text()
                continue

            if cmd == "show":
                show_pose()
                continue

            if cmd == "move":
                apply_pose(ser)
                continue

            parts = cmd.split()

            if parts[0] == "set" and len(parts) == 3:
                idx = int(parts[1]) - 1
                val = int(parts[2])

                if idx < 0 or idx > 5:
                    print("编号必须是1~6")
                    continue

                if val < 0:
                    val = 0
                if val > 250:
                    val = 250

                pose[idx] = val
                move_servo(ser, idx + 1, val)
                show_pose()
                continue

            if parts[0] == "add" and len(parts) == 3:
                idx = int(parts[1]) - 1
                step = int(parts[2])

                if idx < 0 or idx > 5:
                    print("编号必须是1~6")
                    continue

                pose[idx] += step
                if pose[idx] > 250:
                    pose[idx] = 250

                move_servo(ser, idx + 1, pose[idx])
                show_pose()
                continue

            if parts[0] == "sub" and len(parts) == 3:
                idx = int(parts[1]) - 1
                step = int(parts[2])

                if idx < 0 or idx > 5:
                    print("编号必须是1~6")
                    continue

                pose[idx] -= step
                if pose[idx] < 0:
                    pose[idx] = 0

                move_servo(ser, idx + 1, pose[idx])
                show_pose()
                continue

            if parts[0] == "save" and len(parts) == 2:
                save_point(parts[1])
                continue

            print("未知命令，输入 help 查看说明")

    finally:
        ser.close()
        print("serial closed")


if __name__ == "__main__":
    main()
