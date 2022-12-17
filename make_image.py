from turtle import back
from PIL import Image
from PIL import ImageFont
import numpy as np
from PIL import Image, ImageDraw, ImageOps
import requests
from io import BytesIO
from textwrap import wrap

def make_image(text,image, mod, membership, name, file_no):
    with Image.open('bgpng.png') as background:
        background.load()
    #download the image
    response = requests.get(image)
    img = Image.open(BytesIO(response.content))
    img = img.resize((32,32))

    location = (0,0)
    #crop the image in a circle
    def circle_crop(im):
        mask = Image.new('L', im.size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + im.size, fill=255)
        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        return output
    img = circle_crop(img)
    # put image on background
    background.paste(img, (0, 0), img)
    location = (40,10)
    color = (255, 255, 255) # white color
    if membership:
        color = (43,166,64)
        membership_logo = "https://yt3.ggpht.com/E05V1WoYUg3qx8SZBdEckIpmvSGUeYF_l9ItwOgK7zttS3f1NWXJhso2y2B9CSQzoCbIkONa4A=s32-c-k"
    if mod:
        color = (94,132,241)
        mod_icon = "https://cdn3.emoji.gg/emojis/9445-blurple-staff.png"
    #draw the name
    font = ImageFont.truetype(r"C:\Users\suraj\Downloads\Roboto-Medium.ttf", 16)
    draw = ImageDraw.Draw(background)
    draw.text(location, name, color, font=font)
    location = (location[0] + len(name)*12, location[1])
    if mod:
        with Image.open('mod_icon.png') as img:
            img.load()
        background.paste(img, location, img)
        location = (location[0]+16,location[1])

    # download the membership logo
    if membership:
        with Image.open('member.png') as img:
            img.load()
        background.paste(img, location, img)
        location = (location[0]+16,location[1])

    location = (location[0]+8,location[1])

    old_y = background.height
    new_y = len(text)-21
    if new_y < 40:
        print('update new y cuz it was less than 0')
        new_y = 40
    #draw the text with word wrap 
    text = wrap(text, width=(background.width-location[0])/9)
    # crop the image to the size of the wrapped text
    print(old_y, new_y)
    background = background.crop((0,0,background.width,new_y))
    # fill the new background with the color

    draw = ImageDraw.Draw(background)
    draw.text(location, text[0], (255,255,255), font=font)
    if len(text) >2:
        text = wrap(" ".join(text[1:]), width=(background.width-location[0])/6)
        location = (location[0]-len(name)*16,location[1]+22)
        for line in text:
            draw.text(location, line, (255,255,255), font=font)
            location = (location[0], location[1]+22)

    #crop the image to the extent its not same color

    background.save('chats_ss/{}.png'.format(file_no))
