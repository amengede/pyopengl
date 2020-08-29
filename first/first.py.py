import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
import numpy as np
import os

def CompileShaders(vertexPath,fragmentPath):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    #
    #Load files
    #
    vertexFile = open(os.path.join(dir_path,vertexPath),'r')
    vertexCode = vertexFile.read()
    vertexFile.close()
    fragmentFile = open(os.path.join(dir_path,fragmentPath),'r')
    fragmentCode = fragmentFile.read()
    fragmentFile.close()
    #
    #Compile shaders
    #
    vertexShader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertexShader,vertexCode)
    glCompileShader(vertexShader)
    fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragmentShader,fragmentCode)
    glCompileShader(fragmentShader)
    #
    #link shaders
    #
    program = glCreateProgram()
    glAttachShader(program,vertexShader)
    glAttachShader(program,fragmentShader)
    glLinkProgram(program)
    #
    #delete shaders
    #
    glDeleteShader(vertexShader)
    glDeleteShader(fragmentShader)
    return program

def Render(color,program):
    glClearBufferfv(GL_COLOR,0,color)
    glBegin(GL_POINTS)
    glUseProgram(program)
    glDrawArrays(GL_POINTS,0,1)
    glEnd()

def Startup():
    renderingProgram = CompileShaders("vertex.txt","fragment.txt")
    glBindVertexArray(glGenVertexArrays(1))
    return renderingProgram

def main():
    red = np.array([1.0,0.0,0.0,1.0])
    display = (800,600)
    
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    renderingProgram = Startup()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Render(red,renderingProgram)
        pygame.display.flip()
        pygame.time.wait(10)

main()