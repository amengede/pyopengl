import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np

with open("shaders/basicVertex.txt",'r') as f:
    vertex_src = f.readlines()
with open("shaders/basicFragment.txt",'r') as f:
    fragment_src = f.readlines()

if not glfw.init():
    raise Exception("glfw can not be initialised!")

window = glfw.create_window(1280,720,"My OpenGL Window",None,None)

if not window:
    glfw.terminate()
    raise Exception("glfw window could not be created!")

glfw.set_window_pos(window,400,200)
glfw.make_context_current(window)

glClearColor(0,0.1,0.1,1)

#(x,y,z,r,g,b,a)
vertices = [-0.5,-0.5,0.0,1.0,0.0,0.0,
            0.5,-0.5,0.0,0.0,1.0,0.0,
            0.0,0.5,0.0,0.0,0.0,1.0]

vertices = np.array(vertices,dtype=np.float32)

shader = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),
                        compileShader(fragment_src,GL_FRAGMENT_SHADER))
#Vertex Buffer Object
#glGenBuffers(no. of buffers)
VBO = glGenBuffers(1)
#bind VBO to GL's array buffer
glBindBuffer(GL_ARRAY_BUFFER,VBO)
#send data to array buffer
#(target,size in bytes,array,draw_mode)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

#get a pointer to the position array
position = glGetAttribLocation(shader,"a_position")
glEnableVertexAttribArray(position)
#index, points per vertex, data type, 
#normalised, stride, pointer to first
glVertexAttribPointer(position,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))

color = glGetAttribLocation(shader,"a_color")
glEnableVertexAttribArray(color)
glVertexAttribPointer(color,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(12))

glUseProgram(shader)
glClearColor(0,0.2,0.2,1)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLES,0,3)
    glfw.swap_buffers(window)

glfw.terminate()