import smbus  # import SMBus module of I2C

# MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
MPU_ADDR = 0x68   # MPU6050 device address

class AccReader:
    def __init__(self):
        print('[AccReader] init')
        bus = smbus.SMBus(1)
        # write to sample rate register
        bus.write_byte_data(MPU_ADDR, SMPLRT_DIV, 7)
        # write to power management register
        bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 1)
        # write to Configuration register
        bus.write_byte_data(MPU_ADDR, CONFIG, 0)
        # write to Gyro configuration register
        bus.write_byte_data(MPU_ADDR, GYRO_CONFIG, 24)
        # write to interrupt enable register
        bus.write_byte_data(MPU_ADDR, INT_ENABLE, 1)
        self.__bus = bus
        print('[AccReader] done')

    def __read_raw_data(self, addr):
        # accelero and Gyro value are 16-bit
        high = self.__bus.read_byte_data(MPU_ADDR, addr)
        low = self.__bus.read_byte_data(MPU_ADDR, addr+1)

        # concatenate higher and lower value
        value = ((high << 8) | low)

        # to get signed value from mpu6050
        if(value > 32768):
            value = value - 65536
        return value

    @property
    def accleration(self):
        acc_x = self.__read_raw_data(ACCEL_XOUT_H)
        acc_y = self.__read_raw_data(ACCEL_YOUT_H)
        acc_z = self.__read_raw_data(ACCEL_ZOUT_H)

        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0

        return (Ax, Ay, Az)

    @property
    def gyroscope(self):
        gyro_x = self.__read_raw_data(GYRO_XOUT_H)
        gyro_y = self.__read_raw_data(GYRO_YOUT_H)
        gyro_z = self.__read_raw_data(GYRO_ZOUT_H)

        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0

        return (Gx, Gy, Gz)

