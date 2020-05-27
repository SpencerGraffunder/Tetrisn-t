from PIL import Image

# a nice green color
BASE_COLOR_0 = 80
BASE_COLOR_1 = 240
BASE_COLOR_2 = 60

# darken edges by
EDGE_DARKEN_0 = 0.95
EDGE_DARKEN_1 = 0.85
EDGE_DARKEN_2 = 0.75

# brighten middle by
MIDDLE_BRIGHTEN_0 = 0.40
MIDDLE_BRIGHTEN_1 = 0.25
MIDDLE_BRIGHTEN_2 = 0.10

# do stuff
img = Image.new('RGB', (8,8), (BASE_COLOR_0, BASE_COLOR_1, BASE_COLOR_2)) # Create a new 8x8 image with the base color
pixels = img.load() # Create the pixel map

# darken corners
for i in [0,7]: # For every corner pixel:
    for j in [0,7]:
        pixels[i,j] = ((int)(BASE_COLOR_0 * (1 - EDGE_DARKEN_0)), (int)(BASE_COLOR_1 * (1 - EDGE_DARKEN_0)), (int)(BASE_COLOR_2 * (1 - EDGE_DARKEN_0)))

# darken around corners on the edges
for i in [1,2,5,6]:
    for j in [0,7]:
        pixels[i,j] = ((int)(BASE_COLOR_0 * (1 - EDGE_DARKEN_1)), (int)(BASE_COLOR_1 * (1 - EDGE_DARKEN_1)), (int)(BASE_COLOR_2 * (1 - EDGE_DARKEN_1)))
for i in [0,7]:
    for j in [1,2,5,6]:
        pixels[i,j] = ((int)(BASE_COLOR_0 * (1 - EDGE_DARKEN_1)), (int)(BASE_COLOR_1 * (1 - EDGE_DARKEN_1)), (int)(BASE_COLOR_2 * (1 - EDGE_DARKEN_1)))

# darken the middle of the edges
for i in [3,4]:
    for j in [0,7]:
        pixels[i,j] = ((int)(BASE_COLOR_0 * (1 - EDGE_DARKEN_2)), (int)(BASE_COLOR_1 * (1 - EDGE_DARKEN_2)), (int)(BASE_COLOR_2 * (1 - EDGE_DARKEN_2)))
for i in [0,7]:
    for j in [3,4]:
        pixels[i,j] = ((int)(BASE_COLOR_0 * (1 - EDGE_DARKEN_2)), (int)(BASE_COLOR_1 * (1 - EDGE_DARKEN_2)), (int)(BASE_COLOR_2 * (1 - EDGE_DARKEN_2)))

# brigthen the center 2x2
for i in [3,4]:
    for j in [3,4]:
        pixels[i,j] = ((int)(BASE_COLOR_0 * (1 - MIDDLE_BRIGHTEN_0) + 255 * MIDDLE_BRIGHTEN_0), (int)(BASE_COLOR_1 * (1 - MIDDLE_BRIGHTEN_0) + 255 * MIDDLE_BRIGHTEN_0), (int)(BASE_COLOR_2 * (1 - MIDDLE_BRIGHTEN_0) + 255 * MIDDLE_BRIGHTEN_0))

# brigthen around the center 2x2
for i in [2,5]:
    for j in [3,4]:
        pixels[i,j] = ((int)(BASE_COLOR_0 * (1 - MIDDLE_BRIGHTEN_1) + 255 * MIDDLE_BRIGHTEN_1), (int)(BASE_COLOR_1 * (1 - MIDDLE_BRIGHTEN_1) + 255 * MIDDLE_BRIGHTEN_1), (int)(BASE_COLOR_2 * (1 - MIDDLE_BRIGHTEN_1) + 255 * MIDDLE_BRIGHTEN_1))
for i in [3,4]:
    for j in [2,5]:
        pixels[i,j] = ((int)(BASE_COLOR_0 * (1 - MIDDLE_BRIGHTEN_1) + 255 * MIDDLE_BRIGHTEN_1), (int)(BASE_COLOR_1 * (1 - MIDDLE_BRIGHTEN_1) + 255 * MIDDLE_BRIGHTEN_1), (int)(BASE_COLOR_2 * (1 - MIDDLE_BRIGHTEN_1) + 255 * MIDDLE_BRIGHTEN_1))

# brigthen near the middle of the edge
for i in [2,5]:
    for j in [2,5]:
        pixels[i,j] = ((int)(BASE_COLOR_0 * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2), (int)(BASE_COLOR_1 * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2), (int)(BASE_COLOR_2 * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2))
for i in [1,6]:
    for j in [3,4]:
        pixels[i,j] = ((int)(BASE_COLOR_0 * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2), (int)(BASE_COLOR_1 * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2), (int)(BASE_COLOR_2 * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2))
for i in [3,4]:
    for j in [1,6]:
        pixels[i,j] = ((int)(BASE_COLOR_0 * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2), (int)(BASE_COLOR_1 * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2), (int)(BASE_COLOR_2 * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2))

img.save('test.bmp')