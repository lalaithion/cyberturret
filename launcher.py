import platform
import time
import usb.core
import usb.util
import fire

class Armageddon:
    """
    Based on https://github.com/codedance/Retaliation
    """
    DOWN = 0x01
    UP = 0x02
    LEFT = 0x04
    RIGHT = 0x08
    FIRE = 0x10
    STOP = 0x20

    DEVICE_ORIGINAL = 'Original'
    DEVICE_THUNDER = 'Thunder'

    def __init__(self):
        self._get_device()
        self._detach_hid()
        self.DEVICE.set_configuration()

    def _get_device(self):
        self.DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)
        if self.DEVICE is None:
            self.DEVICE = usb.core.find(idVendor=0x0a81, idProduct=0x0701)
            if self.DEVICE is None:
                raise ValueError('Missile device not found')
            else:
                self.DEVICE_TYPE = self.DEVICE_ORIGINAL
        else:
            self.DEVICE_TYPE = self.DEVICE_THUNDER

    def _detach_hid(self):
        if "Linux" == platform.system():
            try:
                self.DEVICE.detach_kernel_driver(0)
            except Exception:
                pass

    def send_cmd(self, cmd):
        print(cmd)
        if self.DEVICE_THUNDER == self.DEVICE_TYPE:
            self.DEVICE.ctrl_transfer(0x21, 0x09, 0, 0,
                                      [0x02, cmd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        elif self.DEVICE_ORIGINAL == self.DEVICE_TYPE:
            self.DEVICE.ctrl_transfer(0x21, 0x09, 0x0200, 0,
                                      [cmd])

    def send_move(self, cmd, duration_ms):
        self.send_cmd(cmd)
        time.sleep(duration_ms / 1000.0)
        self.send_cmd(self.STOP)

class ArmageddonController:
    HALF = 3900
    
    def __init__(self):
        self.turret = Armageddon()
    
    def fire(self, angle):
        angle /= 180
        duration = abs(angle) * self.HALF
        if angle > 0:
            self.turret.send_move(self.turret.LEFT, duration)
            self.turret.send_cmd(self.turret.FIRE)
            time.sleep(3.0)
            self.turret.send_move(self.turret.RIGHT, duration)
        else:
            self.turret.send_move(self.turret.RIGHT, duration)
            self.turret.send_cmd(self.turret.FIRE)
            time.sleep(3.0)
            self.turret.send_move(self.turret.LEFT, duration)
    
    def shake(self, angle):
        angle /= 180
        time = abs(angle) * self.HALF
        if angle > 0:
            self.turret.send_move(self.turret.LEFT, duration)
            self.turret.send_move(self.turret.RIGHT, duration)
        else:
            self.turret.send_move(self.turret.RIGHT, duration)
            self.turret.send_move(self.turret.LEFT, duration)

if __name__ == '__main__':
    fire.Fire(ArmageddonController)
