import serial
import time

PORT = "/dev/ttyS4"
BAUD = 115200


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
    time.sleep(1.5)


def move_joint(ser, servo_id, value):
    cmd = "30 02 07 01 55 a1 93 %02x %02x" % (servo_id, value)
    send_cmd(ser, "servo%d -> %d" % (servo_id, value), cmd)


def main():
    ser = serial.Serial(PORT, BAUD, timeout=1)

    try:
        while True:
            print("")
            print("输入格式：舵机编号 目标值")
            print("例如：1 159")
            print("退出：q")

            s = input("cmd> ").strip()

            if s == "q":
                break

            parts = s.split()

            if len(parts) != 2:
                print("格式错误，例如输入：1 159")
                continue

            servo_id = int(parts[0])
            value = int(parts[1])

            if servo_id < 1 or servo_id > 6:
                print("舵机编号必须是1~6")
                continue

            if value < 0 or value > 250:
                print("目标值建议在0~250")
                continue

            move_joint(ser, servo_id, value)

    finally:
        ser.close()
        print("serial closed")


if __name__ == "__main__":
    main()
