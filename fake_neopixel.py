class Adafruit_NeoPixel(object):
    def __init__(self, num, pin, freq_hz=800000, dma=5, invert=False,
                 brightness=255, channel=0, strip_type=0):
        pass

    def _cleanup(self):
        pass

    def begin(self):
        pass

    def show(self):
        pass

    def setPixelColor(self, n, color):
        pass

    def setPixelColorRGB(self, n, red, green, blue, white=0):
        pass

    def setBrightness(self, brightness):
        print("setBri")
        pass

    def getBrightness(self):
        pass

    def getPixels(self):
        pass

    def numPixels(self):
        pass

    def getPixelColor(self, n):
        pass
