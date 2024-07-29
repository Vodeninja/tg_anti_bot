import random
from PIL import Image, ImageDraw, ImageFont

async def generate_captcha():
    captcha_code = ''.join(str(random.randint(0, 9)) for _ in range(7))


    img = Image.new('RGB', (150, 40), color=(73, 109, 137))
    for y in range(40):
        for x in range(150):
            r = int(73 + (x / 150) * 182)
            g = int(109 + (y / 40) * 146)
            b = int(137 + (x / 150) * 118)
            img.putpixel((x, y), (r, g, b))

    for _ in range(200):
        x = random.randrange(0, 150)
        y = random.randrange(0, 40)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        img.putpixel((x, y), (r, g, b))

    fnt = ImageFont.truetype('font/VKSansDisplay-Bold.ttf', 25)
    d = ImageDraw.Draw(img)
    x = 10

    for char in captcha_code:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        angle = random.randint(-10, 10)
        scale = random.uniform(0.8, 1.2)
        d.text((x, 0), char, font=fnt, fill=(r, g, b), rotate=angle, scale=scale)
        x += 20

    d.rectangle([(0, img.height - 11), (img.width, img.height)], fill=(255, 255, 255))
    small_font = ImageFont.truetype('font/VKSansDisplay-Bold.ttf', 10)
    d.text((img.width // 2 - 32, img.height - 12), "vodeninja.ru", font=small_font, fill=(0, 0, 0))
    img.save('captcha.png')

    return captcha_code

# def main():
#     import asyncio
#     loop = asyncio.get_event_loop()
#     captcha_code = loop.run_until_complete(generate_captcha())
#     print("Generated captcha code:", captcha_code)

# if __name__ == "__main__":
#     main()


# import numpy as np
# import cv2
# import tempfile
# import asyncio
# import os
# import matplotlib.pyplot as plt

# CAPTCHA_CODE_LENGTH = 7
# IMAGE_WIDTH = 150
# IMAGE_HEIGHT = 40
# FONT_FILE = 'font/VKSansDisplay-Bold.ttf'
# FONT_SIZE = 25
# SMALL_FONT_SIZE = 8
# DOMAIN_NAME = "vodeninja.ru"

# async def generate_captcha():
#     captcha_code = ''.join(str(np.random.randint(0, 10)) for _ in range(CAPTCHA_CODE_LENGTH))

#     img = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)
#     img[:, :, 0] = 73 + np.arange(IMAGE_WIDTH) * 182 / IMAGE_WIDTH
#     img[:, :, 1] = 109 + np.arange(IMAGE_HEIGHT)[:, None] * 146 / IMAGE_HEIGHT
#     img[:, :, 2] = 137 + np.arange(IMAGE_WIDTH) * 118 / IMAGE_WIDTH

#     for _ in range(200):
#         x, y = np.random.randint(0, IMAGE_WIDTH), np.random.randint(0, IMAGE_HEIGHT)
#         img[y, x] = np.random.randint(0, 256, 3)

#     font = cv2.FONT_HERSHEY_SIMPLEX
#     x = 10
#     for char in captcha_code:
#         angle = np.random.randint(-10, 11)
#         scale = np.random.uniform(0.8, 1.2)
#         r, g, b = tuple(np.random.randint(0, 256, 3))
#         cv2.putText(img, char, (x, 25), font, scale, (int(r), int(g), int(b)), 2, cv2.LINE_AA)
#         x += 20

#     cv2.rectangle(img, (0, IMAGE_HEIGHT - 11), (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255), -1)
#     cv2.putText(img, DOMAIN_NAME, (IMAGE_WIDTH // 2 - 50, IMAGE_HEIGHT - 2), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

#     with tempfile.TemporaryDirectory() as tmp_dir:
#         tmp_file = os.path.join(tmp_dir, 'captcha.png')
#         cv2.imwrite(tmp_file, img)
#         img = plt.imread(tmp_file)
#         plt.imshow(img)
#         plt.show()
#         return captcha_code, tmp_file

# async def main():
#     captcha_code, tmp_file = await generate_captcha()
#     print(captcha_code)

# asyncio.run(main())