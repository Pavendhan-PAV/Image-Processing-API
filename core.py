# Image manipulation API

from flask import Flask, render_template, send_from_directory, redirect
import os
import cv2
import numpy as np
from PIL import Image

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# default access redirects to API documentation
@app.route("/")
def main():
    return redirect("https://github.com/Pavendhan-PAV/Image-Processing-API/blob/main/README.md", code=302)


# rotate filename the specified degrees
@app.route("/rotate/<angle>/<filename>", methods=["GET"])
def rotate(angle, filename):

    # check for valid angle
    angle = int(angle)
    if not -360 < angle < 360:
        return render_template("error.html", message="Invalid angle parameter (-359 to 359)"), 400

    # open and process image
    target = os.path.join(APP_ROOT, 'static/images')
    destination = "/".join([target, filename])

    img = Image.open(destination)
    img = img.rotate(-1*angle)

    # save and return image
    destination = "/".join([target, 'temp.png'])
    if os.path.isfile(destination):
        os.remove(destination)
    img.save(destination)

    return send_image('temp.png')


# flip filename 'vertical' or 'horizontal'
@app.route("/flip/<mode>/<filename>", methods=["GET"])
def flip(mode, filename):

    # open and process image
    target = os.path.join(APP_ROOT, 'static/images')
    destination = "/".join([target, filename])

    img = Image.open(destination)

    # check mode
    if mode == 'horizontal':
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif mode == 'vertical':
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        return render_template("error.html", message="Invalid mode (vertical or horizontal)"), 400

    # save and return image
    destination = "/".join([target, 'temp.png'])
    if os.path.isfile(destination):
        os.remove(destination)
    img.save(destination)

    return send_image('temp.png')


# crop filename from (x1,y1) to (x2,y2)
@app.route("/crop/<x1>/<y1>/<x2>/<y2>/<filename>", methods=["GET"])
def crop(x1, y1, x2, y2, filename):

    # open image
    target = os.path.join(APP_ROOT, 'static/images')
    destination = "/".join([target, filename])

    img = Image.open(destination)
    width = img.size[0]
    height = img.size[1]

    # check for valid crop parameters
    [x1, y1, x2, y2] = [int(x1), int(y1), int(x2), int(y2)]

    crop_possible = True
    
    while True:
        if not 0 <= x1 < width:
            crop_possible = False
            break
        if not 0 < x2 <= width:
            crop_possible = False
            break
        if not 0 <= y1 < height:
            crop_possible = False
            break
        if not 0 < y2 <= height:
            crop_possible = False
            break
        if not x1 < x2:
            crop_possible = False
            break
        if not y1 < y2:
            crop_possible = False
            break
        break

    # process image
    if crop_possible:
        img = img.crop((x1, y1, x2, y2))
    else:
        return render_template("error.html", message="Crop dimensions not valid"), 400

    # save and return image
    destination = "/".join([target, 'temp.png'])
    if os.path.isfile(destination):
        os.remove(destination)
    img.save(destination)

    return send_image('temp.png')


# blend filename1 and filename2 with alpha parameter
@app.route("/blend/<alpha>/<filename1>/<filename2>", methods=["GET"])
def blend(alpha, filename1, filename2):

    # check for valid alpha
    alpha = float(alpha)
    if not 0 <= alpha <= 100:
        return render_template("error.html", message="Invalid alpha value (0-100)"), 400

    #open images
    target = os.path.join(APP_ROOT, 'static/images')
    destination1 = "/".join([target, filename1])
    destination2 = "/".join([target, filename2])

    img1 = Image.open(destination1)
    img2 = Image.open(destination2)

    # check for dimensions and resize to larger ones
    width = max(img1.size[0], img2.size[0])
    height = max(img1.size[1], img2.size[1])

    img1 = img1.resize((width, height), Image.ANTIALIAS)
    img2 = img2.resize((width, height), Image.ANTIALIAS)

    # if one image in gray scale, convert the other to monochrome
    if len(img1.mode) < 3:
        img2 = img2.convert('L')
    elif len(img2.mode) < 3:
        img1 = img1.convert('L')

    # blend images
    img = Image.blend(img1, img2, float(alpha)/100)

    # save and return
    destination = "/".join([target, 'temp.png'])
    if os.path.isfile(destination):
        os.remove(destination)
    img.save(destination)

    return send_image('temp.png')



# various noise addition
@app.route("/Noise/<type>/<filename>", methods=["GET"])
def Noise(noise_typ, filename):

    # open and process image
    target = os.path.join(APP_ROOT, 'static/images')
    destination = "/".join([target, filename])
    
    image = Image.open(destination)
    
    if noise_typ  == "gauss":
        image = cv2.GaussianBlur(image, (11,11), 0)
        """ row,col,ch= image.shape
        mean = 0
        var = 0.1
        sigma = var**0.5
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        image = image + gauss """

    elif noise_typ  == "s&p":
        row,col,ch = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
        out[coords] = 0
        image = out

    elif noise_typ  == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        image = np.random.poisson(image * vals) / float(vals)

    elif noise_typ  == "speckle":
        row,col,ch = image.shape
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)        
        image = image + image * gauss
    else:
        return render_template("error.html", message="Mode not supported (Gaussian, S&P, Poisson, Speckle)"), 400

    # save and return image
    destination = "/".join([target, 'temp.png'])
    if os.path.isfile(destination):
        os.remove(destination)
    image.save(destination)

    return send_image('temp.png')

# retrieve file from 'static/images' directory
@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)


if __name__ == "__main__":
    app.run()
