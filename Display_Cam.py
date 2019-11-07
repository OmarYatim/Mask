import pyglet
from pyglet.gl import *
from pyglet.window import key
import pywavefront
from pywavefront import visualization
import cv2
import numpy
import sys
from PIL import Image

window = pyglet.window.Window()
obj = pywavefront.Wavefront('mask/Mask.obj')
Face_Cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
camera = cv2.VideoCapture(0)
pos = [(5.0, 5.0)]
X = 0
Y = 0
Scale = 0


def cv2glet():
    ret, img = camera.read()
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = Face_Cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            global X
            X=x
            global Y
            Y = y
            global Scale
            Scale = w
            print(str(w))
            print(str(h))
            pos.clear()
            pos.append((0.0, -1.0))

    except:
        print("error")
    rows, cols, channels = img.shape
    raw_img = Image.fromarray(img).tobytes()

    top_to_bottom_flag = -1
    bytes_per_row = channels*cols
    pyimg = pyglet.image.ImageData(width=cols,
                                   height=rows,
                                   format='BGR',
                                   data=raw_img,
                                   pitch=top_to_bottom_flag*bytes_per_row)

    return pyimg


@window.event
def on_resize(width, height):
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45., float(width)/height, 1., 1000.)
    glMatrixMode(GL_MODELVIEW)
    return True


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        print('Application Exited with Key Press')
        window.close()


@window.event
def on_draw():
    window.clear()
    glLoadIdentity()
    cv2glet().blit(-300,-250,-500)
    draw_face()
    #visualization.draw(obj)


@window.event
def update(dt):#zedtlek el update
    cv2glet().blit(-300, -250, -500)


def draw_face():
    glLoadIdentity()
#    glPushMatrix()
    if(Scale > 90) and (Scale < 120):
        glTranslated(-2 + X / 120, 1 - Y / 120 , -4.5)
    if (Scale > 120) and (Scale < 150):
        glTranslated(-2 + X / 120, 0.6 - Y / 120, -4.5)
    if(Scale > 150) and (Scale < 180):
        glTranslated(-1.8 + X / 120, 0.2 - Y / 120 , -4.5)
    if(Scale > 180) and (Scale < 210):
        glTranslated(-1.7 + X / 120, - Y / 120 , -4.5)
    if(Scale >210) and (Scale < 240):
        glTranslated(-1.5 + X / 120,  - Y / 120 , -4.5)
    glScalef(Scale/190,Scale/190,Scale/190)
    visualization.draw(obj)
 #   glPopMatrix()


pyglet.clock.schedule(update)  # zedet ligne hedhy
pyglet.app.run()
