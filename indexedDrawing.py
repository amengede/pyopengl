import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np

with open("shaders/basicVertex2.txt",'r') as f:
    vertex_src = f.readlines()
with open("shaders/basicFragment.txt",'r') as f:
    fragment_src = f.readlines()

def window_resize(window,width,height):
    glViewport(0,0,width,height)

if not glfw.init():
    raise Exception("glfw can not be initialised!")

window = glfw.create_window(640,480,"My OpenGL Window",None,None)

if not window:
    glfw.terminate()
    raise Exception("glfw window could not be created!")

glfw.set_window_pos(window,400,200)
glfw.set_window_size_callback(window,window_resize)
glfw.make_context_current(window)

glClearColor(0,0.1,0.1,1)

vertices = [-0.5,-0.5,0.0,1.0,0.0,0.0,
            0.5,-0.5,0.0,0.0,1.0,0.0,
            -0.5,0.5,0.0,0.0,0.0,1.0,
            0.5,0.5,0.0,1.0,1.0,1.0]

indices = [0,1,2,
            1,2,3]

vertices = np.array(vertices,dtype=np.float32)
indices = np.array(indices,dtype=np.uint32)

shader = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),
                        compileShader(fragment_src,GL_FRAGMENT_SHADER))
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

#Element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER,indices.nbytes,indices,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(12))

glUseProgram(shader)
glClearColor(0,0.2,0.2,1)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)
    #(mode,no of indices,data_type,offset)
    glDrawElements(GL_TRIANGLES,len(indices),GL_UNSIGNED_INT,None)
    glfw.swap_buffers(window)

glfw.terminate()