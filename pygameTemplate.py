from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import pygame as pg
import numpy as np
import pyrr

pg.init()
pg.display.set_mode((640,480),pg.OPENGL|pg.DOUBLEBUF|pg.RESIZABLE)
glClearColor(0.2, 0.3, 0.3, 1.0)

running = True

while running:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running = False
        if event.type==pg.VIDEORESIZE:
            glViewport(0,0,event.w,event.h)

    glClear(GL_COLOR_BUFFER_BIT)
    
    pg.display.flip()

pg.quit()