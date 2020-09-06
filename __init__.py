import time

PIN_NODEMCU_D0=16
PIN_NODEMCU_D1=5
PIN_NODEMCU_D2=4
PIN_NODEMCU_D3=0
PIN_NODEMCU_D4=2
PIN_NODEMCU_D5=14
PIN_NODEMCU_D6=12
PIN_NODEMCU_D7=13
PIN_NODEMCU_D8=15

PIN_NODEMCU_RX=3
PIN_NODEMCU_TX=1

PIN_NODEMCU_A0=0

class shell:
    def __init__(self):
        pass

    @property
    def ls(self):
        print("qwert")

class led_strip:

    def __init__(self, pin, count):
        import machine, neopixel
        self.np = neopixel.NeoPixel(machine.Pin(pin), count)

        self._rainbow_color = (255, 0, 0)
        self._rainbow_index = 0
        self._count = count
        self._ms = 10
        self._inteval = 1

    def set_ms(self, ms):
        self._ms = ms;

    def set_interval(self, inteval):
        self._inteval = inteval

    def red_update(self, index, up_down):
        for i in range(255):
            self.np[index] = (self.np[index][0] + up_down, self.np[index][1], self.np[index][2])
            self.np.write()
            time.sleep_ms(self._ms)

    def green_update(self, index, up_down):
        for i in range(255):
            self.np[index] = (self.np[index][0], self.np[index][1] + up_down, self.np[index][2])
            self.np.write()
            time.sleep_ms(self._ms)

    def blue_update(self, index, up_down):
        for i in range(255):
            self.np[index] = (self.np[index][0], self.np[index][1], self.np[index][2]+ up_down)
            self.np.write()
            time.sleep_ms(self._ms)

    def clear(self):
        for i in range(self._count):
            self.np[i] = (0, 0, 0)
            self.np.write()

    def rainbow(self, pin):
        self.red_update(pin, 1)
        self.green_update(pin, 1)
        self.red_update(pin, -1)
        self.blue_update(pin, 1)
        self.green_update(pin, -1)
        self.red_update(pin, 1)
        self.blue_update(pin, -1)
        self.red_update(pin, -1)

    def rainbow_next_color(self):
        self._rainbow_index = self._rainbow_index + self._inteval
        if (self._rainbow_index >= 6*256):
            self._rainbow_index = 0;

        if (self._rainbow_index < 256):
            self._rainbow_color = (255, self._rainbow_index, 0)

        elif (self._rainbow_index < 2*256):
            self._rainbow_color = (255-(self._rainbow_index-256), 255, 0)

        elif (self._rainbow_index < 3*256):
            self._rainbow_color = (0, 255, self._rainbow_index-2*256)

        elif (self._rainbow_index < 4*256):
            self._rainbow_color = (0, 255-(self._rainbow_index-3*256), 255)

        elif (self._rainbow_index < 5*256):
            self._rainbow_color = (self._rainbow_index-4*256, 0, 255)

        elif (self._rainbow_index < 6*256):
            self._rainbow_color = (255, 0, 255-(self._rainbow_index-5*256))

    def rainbow_bounce(self, start=0, end=-1):
        forward = True
        i = 0

        if (start < 0):
            start = 0
        if (start > (self._count-1)):
            start = (self._count-1)

        if (end  < 0 or end > (self._count-1)):
            end = (self._count-1)

        while True:
            self.np[i] = (0,0,0)

            if (forward):
                i = i + 1
                if (i > end):
                    i = end
                    forward = False
            else:
                i = i - 1
                if (i < start):
                    i = start
                    forward = True

            self.np[i] = self._rainbow_color
            self.rainbow_next_color()
            self.np.write()
            time.sleep_ms(self._ms)

