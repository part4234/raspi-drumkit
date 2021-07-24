import smbus  # import SMBus module of I2C

# MPU6050 Registers and their Address
# https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
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
        # sample rate
        bus.write_byte_data(MPU_ADDR, SMPLRT_DIV, 7)
        # power management
        bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 1)
        # configuration 
        bus.write_byte_data(MPU_ADDR, CONFIG, 0)
        # gyroscope configuration +-2000 deg/s
        bus.write_byte_data(MPU_ADDR, GYRO_CONFIG, 24)
        # accelerometer configuration +-16g
        bus.write_byte_data(MPU_ADDR, ACCEL_CONFIG, 24)
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

        # +-2g: 16384
        # +-4g: 8192
        # +-8g: 4096
        # +-16g: 2048
        Ax = acc_x/2048.0
        Ay = acc_y/2048.0
        Az = acc_z/2048.0

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

