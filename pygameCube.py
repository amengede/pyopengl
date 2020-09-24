import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import pygame as pg
import numpy as np
import pyrr

with open("shaders/texturedVertex.txt",'r') as f:
    vertex_src = f.readlines()
with open("shaders/texturedFragment.txt",'r') as f:
    fragment_src = f.readlines()

#(x,y,z,r,g,b,u,v)
vertices = [-0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5,  0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5, -0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

             0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
             0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
            -0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

             0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
            -0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0]

indices = [0,  1,  2,  2,  3,  0,
           4,  5,  6,  6,  7,  4,
           8,  9, 10, 10, 11,  8,
          12, 13, 14, 14, 15, 12,
          16, 17, 18, 18, 19, 16,
          20, 21, 22, 22, 23, 20]

vertices = np.array(vertices,dtype=np.float32)
indices = np.array(indices,dtype=np.uint32)

pg.init()
pg.display.set_mode((1200,720),pg.OPENGL|pg.DOUBLEBUF|pg.RESIZABLE)

shader = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),
                        compileShader(fragment_src,GL_FRAGMENT_SHADER))

#Vertex buffer object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

#Element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER,indices.nbytes,indices,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,vertices.itemsize*8,ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,vertices.itemsize*8,ctypes.c_void_p(12))

glEnableVertexAttribArray(2)
glVertexAttribPointer(2,2,GL_FLOAT,GL_FALSE,vertices.itemsize*8,ctypes.c_void_p(24))

texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D,texture)
#texture wrapping
#s and t: u and v coordinates
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
#texture filtering
#minifying or magnifying filter
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
#load image
image = pg.image.load("textures/cat.png")
image_width,image_height = image.get_rect().size
img_data = pg.image.tostring(image,'RGBA')
glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image_width,image_height,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data)

glUseProgram(shader)
glClearColor(0,0.2,0.2,1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

rotation_loc = glGetUniformLocation(shader,"rotation")

running = True

while running:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running = False
        if event.type==pg.VIDEORESIZE:
            glViewport(0,0,event.w,event.h)

    ct = pg.time.get_ticks()/1000

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    #make rotation matrix
    rot_x = pyrr.Matrix44.from_x_rotation(0.5*ct)
    rot_y = pyrr.Matrix44.from_y_rotation(0.8*ct)
    #(handle to load to, no. of matrices, transposed
    # matrix)
    glUniformMatrix4fv(rotation_loc,1,GL_FALSE,pyrr.matrix44.multiply(rot_x,rot_y))
    #(mode,no of indices,data_type,offset)
    glDrawElements(GL_TRIANGLES,len(indices),GL_UNSIGNED_INT,None)
    
    pg.display.flip()

pg.quit()