import sys
import time, json
# Python Image Library
from PIL import Image

from naoqi import ALProxy


def showNaoImage(IP, PORT):
  """
  First get an image from Nao, then show it on the screen with PIL.
  """

  camProxy = ALProxy("ALVideoDevice", IP, PORT)
  resolution = 2    # VGA
  colorSpace = 11   # RGB

  videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)

  t0 = time.time()

  # Get a camera image.
  # image[6] contains the image data passed as an array of ASCII chars.
  naoImage = camProxy.getImageRemote(videoClient)

  t1 = time.time()

  # Time the image transfer.
  print "acquisition delay ", t1 - t0

  camProxy.unsubscribe(videoClient)

  # Now we work with the image returned and save it as a PNG  using ImageDraw
  # package.
  # Get the image size and pixel array.
  imageWidth = naoImage[0]
  imageHeight = naoImage[1]
  array = naoImage[6]

  # Create a PIL Image from our pixel array.
  im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

  # Save the image.
  im.save("camImage.png", "PNG")
  im.show()

if __name__ == '__main__':
    # IP = "10.0.0.2"  # Replace here with your NaoQi's IP address.
    # PORT = 9559
    # Read IP address from first argument if any.
    with open('config.json') as f:
      data = json.load(f)
    IP = data.get("IP").encode("utf-8")
    print (type(IP))
    PORT = data.get("PORT")
    print (type(PORT))
    if len(sys.argv) > 1:
      IP = sys.argv[1]

    naoImage = showNaoImage(IP, PORT)
