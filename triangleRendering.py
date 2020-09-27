from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import pygame as pg
import numpy as np

pg.init()
#display
pg.display.set_mode((640,480),pg.OPENGL|pg.DOUBLEBUF|pg.RESIZABLE)
glClearColor(0.2, 0.3, 0.3, 1.0)

#timer
clock = pg.time.Clock()

#define data
vertices = [0.5,  0.5, 0.0,
            0.5, -0.5, 0.0,
            -0.5, -0.5, 0.0,
            -0.5,  0.5, 0.0] 
indices = [0, 1, 3,
            1, 2, 3]

vertices = np.array(vertices,dtype=np.float32)
indices = np.array(indices,dtype=np.uint32)
VBO = glGenBuffers(1)
EBO = glGenBuffers(1)
VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,vertices.itemsize*3,ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

#shaders
with open("shaders/basicVertex3.txt",'r') as f:
    vertex_src = f.readlines()
with open("shaders/flatFragment.txt",'r') as f:
    fragment_src = f.readlines()
shader = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),
                        compileShader(fragment_src,GL_FRAGMENT_SHADER))
glUseProgram(shader)
running = True

while running:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running = False
        if event.type==pg.VIDEORESIZE:
            glViewport(0,0,event.w,event.h)

    glClear(GL_COLOR_BUFFER_BIT)
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
    
    pg.display.flip()
    clock.tick()
    fps = clock.get_fps()
    pg.display.set_caption("Running at "+str(int(fps))+" fps")

pg.quit()