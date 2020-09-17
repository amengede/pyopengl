import glfw
from OpenGL.GL import *
import numpy as np

"""
    create a rotating triangle
"""

if not glfw.init():
    raise Exception("glfw can not be initialised!")

#glfw.create_window(w,h,title,monitor,share)
#monitor: used for full screen, None if windowed
#share: context with which to share resources, None if not sharing
window = glfw.create_window(1280,720,"My OpenGL Window",None,None)

if not window:
    glfw.terminate()
    raise Exception("glfw window could not be created!")

glfw.set_window_pos(window,400,200)
glfw.make_context_current(window)

#background color, (r,g,b,a)
glClearColor(0,0.1,0.1,1)

#x,y,z
#
#x: -1 = left
#   1 = right
#
#y: -1 = up
#   1 = down
vertices = [-0.5,-0.5,0.0,
            0.5,-0.5,0.0,
            0.0,0.5,0.0]

#r,g,b,a
colors = [1.0,0.0,0.0,
            0.0,1.0,0.0,
            0.0,0.0,1.0]

vertices = np.array(vertices,dtype=np.float32)
colors = np.array(colors,dtype=np.float32)

glEnableClientState(GL_VERTEX_ARRAY)
glVertexPointer(3,GL_FLOAT,0,vertices)
glEnableClientState(GL_COLOR_ARRAY)
glColorPointer(3,GL_FLOAT,0,colors)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)
    glRotatef(2,0,1,0)
    glDrawArrays(GL_TRIANGLES,0,3)
    glfw.swap_buffers(window)

glfw.terminate()