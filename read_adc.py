import adafruit_mcp3xxx.mcp3008 as MCP
import board
import busio
import csv
import digitalio
from adafruit_mcp3xxx.analog_in import AnalogIn

class ReadAdc:
  def __init__(self):
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # create the chip select
    cs = digitalio.DigitalInOut(board.D5)
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    # create an analog input channel on pin 0
    self.chan = AnalogIn(mcp, MCP.P0)