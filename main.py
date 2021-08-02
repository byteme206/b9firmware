# B9 Robot Model Firmware v0.1, copyright 2021 Evan C Wade.
# Based on Circuit Python and designed for use with the Adafruit Feather M4
# microcontroller with FeatherWing PropMaker.


### Imports
# Language Core libraries
from time import monotonic as now
import array
import math
try:
    import urandom as random
except ImportError:
    import random
from board import *
import pwmio
import digitalio
from analogio import AnalogIn
import storage

# Firmware-specific libraries
import neopixel
from rainbowio import colorwheel as wheel
from audiomp3 import MP3Decoder
from audioio import AudioOut
import adafruit_lis3dh


### Peripheral configuration
# Set up the Feather for controlling power to the LEDs and audio amp
enable = digitalio.DigitalInOut(board.D10)
enable.direction = digitalio.Direction.OUTPUT
enable.value = True

# Set up a microswitch for rotating color palettes
mcswitch = digitalio.DigitalInOut(board.D9)
mcswitch.switch_to_input(pull=digitalio.Pull.UP)

# Set up audio for mp3 playback
audio = AudioOut(board.A0)

# List of B9 voice clips stored on the Flash chip.
voicemp3 = [
    "affirmitive.mp3",
    "common.mp3",
    "danger3.mp3",
    "doesnotcompute.mp3",
    "icomputeyouwell.mp3",
    "ihaveonlyou.mp3",
    "important.mp3",
    "nofear.mp3",
    "primedirective.mp3",
    "thank_you.mp3",
    "wastingtime.mp3",
    "watch_it.mp3"
]

# List of sound files for low power warnings
pwrmp3 = [
    "alarm.mp3",
    "energy_gone.mp3"
]

# Create a default file object to instantiate the MP3 decoder for later use.
# This is a memory management trick as the MP3Decoder will let us replace the
# filename, causing it to decode whatever is specified.
mp3 = open(voicemp3[0], "rb")
decoder = MP3Decoder(mp3)

# Set the detection threshold for blinking the voice light.
AUD_THRESHOLD = 0.25

# Set up the voice light LED
r_pin = pwmio.PWMOut(board.D11, duty_cycle=0, frequency=20000)
g_pin = pwmio.PWMOut(board.D12, duty_cycle=0, frequency=20000)
b_pin = pwmio.PWMOut(board.D13, duty_cycle=0, frequency=20000)

# Set up the NeoPixel LEDs
NUM_PIXELS = 12
ORDER = neopixel.GRB
BLACK = (0, 0, 0)

pixels = neopixel.NeoPixel(
    board.D5,
    NUM_PIXELS,
    brightness=0.4,
    auto_write=False,
    pixel_order=ORDER
    )

thumpers = neopixel.NeoPixel(
    board.D6,
    2,
    brightness=0.5,
    auto_write=False,
    pixel_order=ORDER
)

pixels.fill(BLACK)
thumpers.fill(BLACK)

pixels.show()
thumpers.show()

# Set up the accelerometer
I2C = busio.I2C(board.SCL, board.SDA)

try:
    ACCEL = adafruit_lis3dh.LIS3DH_I2C(I2C, address=0x18)
except:
    ACCEL = adafruit_lis3dh.LIS3DH_I2C(I2C, address=0x19)

ACCEL.range = adafruit_lis3dh.RANGE_4_G
ACCEL.set_tap(2, 40)

# Set up power management interface
vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)


## Helpers
# non-blocking sleep function
def sleep(delay):
    start = now()
    while start + delay > now():
        yield


# return the voltage value on the reference pin
def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

# LED Helpers
# color definitions
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
PINK = (255,0,213)
WHITE = (255, 255, 255)

# Bottom chest panel color palettes
BLINKY_COLORS = [
    [YELLOW, BLUE, GREEN, WHITE, RED],
    [PURPLE, BLUE, CYAN, GREEN],
    [RED, ORANGE, YELLOW, WHITE],
    [RED, ORANGE, YELLOW, GREEN, BLUE]
]

# Voice light color palettes
VOICE_COLORS = [RED, CYAN, YELLOW, PINK]

# Heartbeat light color palettes
THUMPER_COLORS = [ WHITE, BLUE, ORANGE, PURPLE ]

# Set the default color palette on startup
palette_index = 0


# Utility function to cycle the LED color palettes used by animation functions.
def change_palette():
    palette_index += 1

    if palette_index > 3:
        palette_index = 0


# Function that randomly blinks LEDs on the 12-light panel at the bottom of the
# robot's chest panel.
def blinky_random(wait, qty, palette_index):
    for _ in range(qty):
        c = random.randint(0, len(BLINKY_COLORS[palette_index]) - 1)
        j = random.randint(0, NUM_PIXELS - 1)
        pixels[j] = blinky_colors[c]

        for i in range(1,5):
            pixels.brightness = i / 5.0
            pixels.show()
            sleep(wait)

        for i in range(5, 0, -1):
            pixels.brightness = i / 5.0
            pixels[j] = [0, 0, 0]
            pixels.show()
            sleep(wait)
    pass

# Function that randomly flashes one of two "heartbeat" lights at the top of
# the robot's chest panel.
def heartbeat(wait, palette_index):
    for _ in range(2):
        j = random.randint(0, 1)
        thumpers[j] = THUMPER_COLORS[palette_index]

        for i in range(1,5):
            thumpers.brightness = i / 5.0
            thumpers.show()
            sleep(wait)

        for i in range(5, 0, -1):
            thumpers.brightness = i / 5.0
            thumpers[j] = [0, 0, 0]
            thumpers.show()
            sleep(wait)
    pass


# Function that automatically flashes the LED voice light when the audio levels
# exceed the defined threshold. This causes the LED to flash in sync with the
# clip being played automatically.
def voice_flash(palette_index):
    r, g, b = wheel(VOICE_COLORS[palette_index])
    if audio.rms > AUD_THRESHOLD:
        red.duty_cycle = int(r * 65536 / 256)
        green.duty_cycle = int(g * 65536 / 256)
        blue.duty_cycle = int(b * 65536 / 256)
    pass


### Main loop
while True:
# Run the chest lights on a random pattern
    blinky_random(0.3, 2, palette_index)
    heartbeat(0.1, palette_index)
    blinky_random(0.3, 2, palette_index)
    heartbeat(0.1, palette_index)
    blinky_random(0.3, 2, palette_index)
    heartbeat(0.1, palette_index)

# Detect a double-tap event and respond by playing a random voice clip of B9
    while ACCEL.tapped:
        enable.value = True
        sleep(.01)
        filename = voicemp3[random.randint(0, len(voicemp3) - 1]
        decoder.file = open(filename, "rb")
        initial = now()
        audio.play(decoder)
        pass

# While the audio is playing, trigger a function that flashes the voice light
# in sync with the audio clip automatically
    while audio.playing:
        voice_flash(palette_index)
        pass

# Sense if the palette cycle button has been pressed
    if not mcswitch.value:
        change_palette()
        pass

# Power saving and monitoring function. First, checks to see if there is active
# audio playback. If not, it sets a two minute timeout, after which it will
# power down the LEDs and the audio amplifier circuit, extending battery life.
# It will also check for battery charge level and enter "crisis" mode. In this
# mode, the B9 will play a classic Lost In Space sound effect, then announce
# that its energy is depleted. Then it will sleep for ten minutes before
# waking up and repeating its warning until the battery falls below usable
# levels.
    if audio.playing == False:
        sleep(120.0)
        enable.value = False

        if get_voltage(vbat_voltage) < 3.31:
            enable.value = True
            pixels.fill(BLACK)
            thumpers.fill(BLACK)
            pixels.show()
            thumpers.show()
            palette_index = 0

            for filename in pwrmp3:
                decoder.file = open(filename, "rb")
                audio.play(decoder)

            enable.value = False
            sleep(600)
