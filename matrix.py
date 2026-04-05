import time
import random
import sys
import shutil
import os

# Initialize ANSI escape sequences for Windows
if sys.platform == 'win32':
    os.system('')


class message(str):
    def __new__(cls, text, speed, width):
        self = super(message, cls).__new__(cls, text)
        self.speed = speed
        self.y = -1 * len(text)
        self.x = random.randint(0, width - 1)
        self.skip = 0
        return self

    def move(self):
        if self.speed > self.skip:
            self.skip += 1
        else:
            self.skip = 0
            self.y += 1


class display(list):

    def __init__(self):
        size = shutil.get_terminal_size()
        self.width, self.height = size.columns, size.lines
        self[:] = [' ' for _ in range(self.height * self.width)]

    def set_vertical(self, x, y, string):
        string = string[::-1]
        if x < 0:
            x = 80 + x
        if x >= self.width:
            x = self.width - 1
        if y < 0:
            string = string[abs(y):]
            y = 0
        if y + len(string) > self.height:
            string = string[0:self.height - y]
        if y >= self.height:
            return
        start = y * self.width + x
        length = self.width * (y + len(string))
        step = self.width
        self[start:length:step] = string

    def __str__(self):
        return ''.join(self)


def matrix(iterations, sleep_time=.08):
    messages = []
    try:
        d = display()
    except Exception:
        return # Fallback for non-TTY environments

    for _ in range(iterations):
        # Clear buffer for new frame
        d[:] = [' ' for _ in range(d.height * d.width)]
        
        messages.append(message('10' * 16, random.randint(1, 5), d.width))
        for text in messages:
            d.set_vertical(text.x, text.y, text)
            text.move()
        # Remove messages that are off-screen to save memory/CPU
        messages = [m for m in messages if m.y < d.height]
        
        sys.stdout.write('\033[H\033[1m\033[31m%s\033[0m' % d)
        sys.stdout.flush()
        time.sleep(sleep_time)


if __name__ == '__main__':
    while True:
        try:
            matrix(150)
        except KeyboardInterrupt:
            sys.stdout.write('\n\033[1m\033[32m=== Matrix Stopped ====\033[0m\n')
            sys.exit()