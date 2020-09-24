import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
import pyrr
from PIL import Image


with open("shaders/perspectiveVertex.txt",'r') as f:
    vertex_src = f.readlines()
with open("shaders/texturedFragment.txt",'r') as f:
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

#(x,y,z,r,g,b,u,v)
vertices = [-0.5, -0.5,  0.5,  0.0, 0.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 1.0,
            -0.5,  0.5,  0.5,  0.0, 1.0,

            -0.5, -0.5, -0.5,  0.0, 0.0,
             0.5, -0.5, -0.5,  1.0, 0.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5,  0.5, -0.5,  0.0, 1.0,

             0.5, -0.5, -0.5,  0.0, 0.0,
             0.5,  0.5, -0.5,  1.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 1.0,
             0.5, -0.5,  0.5,  0.0, 1.0,

            -0.5,  0.5, -0.5,  0.0, 0.0,
            -0.5, -0.5, -0.5,  1.0, 0.0,
            -0.5, -0.5,  0.5,  1.0, 1.0,
            -0.5,  0.5,  0.5,  0.0, 1.0,

            -0.5, -0.5, -0.5,  0.0, 0.0,
             0.5, -0.5, -0.5,  1.0, 0.0,
             0.5, -0.5,  0.5,  1.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 1.0,

             0.5,  0.5, -0.5,  0.0, 0.0,
            -0.5,  0.5, -0.5,  1.0, 0.0,
            -0.5,  0.5,  0.5,  1.0, 1.0,
             0.5,  0.5,  0.5,  0.0, 1.0]

indices = [0,  1,  2,  2,  3,  0,
           4,  5,  6,  6,  7,  4,
           8,  9, 10, 10, 11,  8,
          12, 13, 14, 14, 15, 12,
          16, 17, 18, 18, 19, 16,
          20, 21, 22, 22, 23, 20]

vertices = np.array(vertices,dtype=np.float32)
indices = np.array(indices,dtype=np.uint32)

shader = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),
                        compileShader(fragment_src,GL_FRAGMENT_SHADER))
#get a handle to the rotation matrix from the shader
model_loc = glGetUniformLocation(shader,"model")
proj_loc = glGetUniformLocation(shader,"projection")
glEnable(GL_DEPTH_TEST)
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

#Element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER,indices.nbytes,indices,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,vertices.itemsize*5,ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,vertices.itemsize*5,ctypes.c_void_p(12))

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
image = Image.open("textures/cat.png")
img_data = np.array(image.getdata(), np.uint8)
glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image.width,image.height,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data)

glUseProgram(shader)
glClearColor(0,0.2,0.2,1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

#(field of view, aspect ratio,near,far)
projection = pyrr.matrix44.create_perspective_projection_matrix(45,1280/720,0.1,100)
glUniformMatrix4fv(proj_loc,1,GL_FALSE,projection)
translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,0,-3]))

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    #make rotation matrix
    rot_x = pyrr.Matrix44.from_x_rotation(0.5*glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(0.8*glfw.get_time())
    rotation = pyrr.matrix44.multiply(rot_x,rot_y)
    model = pyrr.matrix44.multiply(rotation,translation)
    #(handle to load to, no. of matrices, transposed
    # matrix)
    glUniformMatrix4fv(model_loc,1,GL_FALSE,model)
    #(mode,no of indices,data_type,offset)
    glDrawElements(GL_TRIANGLES,len(indices),GL_UNSIGNED_INT,None)
    glfw.swap_buffers(window)

glfw.terminate()