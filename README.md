# Image Processing API
Image Processing API written in Python, using the Pillow library for image manipulation and exposing the functions with the Flask framework. The API has been tested with jpg, png and bmp formats and is able to flip, rotate and crop an image, as well as blending two images, either RGB or gray scale.

For a live demo, please visit this [HOSTED WEBISTE](https://dig-img-processing-api.herokuapp.com/). The App has been deployed to Heroku.

## Getting started
The API includes three Python files:
* `core.py`: includes the basic calls of the API. Run the file and use `GET` requests on `localhost:5000`. For more details please refer to the documentation section in this file.
* `app.py`: a web application to test the functionality that serves as a proof of concept. Run it, navigate to `localhost:5000` and follow the instructions. For more details please refer to the documentation section in this file.

Other files have been included for Heroku deployment: `Procfile` & `requirements.txt`.

## Dependencies
Python installation needs the `PIL` library (image processing)<br> `flask` with its dependencies (`werkzeug`, `jinja2`, `markupsafe`, `itsdangerous`)<br> testing libraries (`unittest` and `requests`)<br> `gunicorn` to provide an entrypoint for the live deployment. 

## Documentation
The different calls can be interfaced with `GET` methods. All images must be located in the `static/images` folder, or otherwise specify the relative path, from that folder, in `filename` parameter. If the request is correct, the modified image will be returned. The syntaxes and an example for each function are described herein.

### Flip
``` http
GET /flip/<mode>/<filename>
```
where `mode` can either be `vertical` or `horizontal` and `filename` is the image file name, including extension and relative to the images folder. 

### Rotate
``` http
GET /rotate/<angle>/<filename>
```
where `angle` can take any value between 0 and 359 degrees. A positive value indicates clockwise rotation, whereas a negative one indicates counter-clockwise rotation. `filename` is the image file name, including extension and relative to the images folder. 

### Crop
``` http
GET /crop/<x1>/<y1>/<x2>/<y2>/<filename>
```
with the start and stop point coordinates, (`x1, y1`) and (`x2, y2`), respectively. `filename` is the image file name, including extension and relative to the images folder. 

### Blend
``` http
GET /blend/<alpha>/<filename1>/<filename2>
```
where `alpha`, in % (between 0 and 100), is the weight of the first image in the blend. `filename1` and `filename2` specify the images to blend. If one of them is in gray scale, the other one will be converted automatically. Antialias resizing is also done behind the curtains.

### Noise & Blur
``` http
GET /Noise/<typ>/<filename>
```
where `typ` can be `Gaussian` or `Salt & Pepper` or `Poisson` or `Speckle` and `filename` is the image file name, including extension and relative to the images folder. 

## Web application
To test the app localy, run `app.py` and navigate to `localhost:5000`. Otherwise, navigate to the live demo.

Use the `SELECT FILE` button to upload the desired file. 

If successful, the browser will redirect to the processing page.

Input the desired parameters to apply the corresponding transformation. The modified image will be opened with your default image viewing program. The parameters are now sent through the form data with a post method, instead of being passed as arguments in the GET request. So, this app showcases a different approach to API functionality. The different transformations are:

* Flip: simply click either the `Vertical` or the `Horizontal` buttons.
* Rotate: input the degrees between 0 and 359 (html field validation). Use a positive number for clockwise rotation or a negative one for a counter-clockwise one. Click `GO` to proceed.
* Crop: input the start and stop point coordinates, (`x1, y1`) and (`x2, y2`), respectively. Click `GO` to proceed. Will be validated by the API.
* Blend: input alpha (%) between 0 and 100, html validated. The image will be blend with the stock photo `blend.jpg`. The higher the alpha parameter, the more weight will be assigned to the stock photo (i.e. for alpha equals 0 the image will remain unchanged). Click `GO` to proceed.
