import glfw

if not glfw.init():
    raise Exception("glfw can not be initialised!")

window = glfw.create_window(1280,720,"My OpenGL Window",None,None)

if not window:
    glfw.terminate()
    raise Exception("glfw window could not be created!")

glfw.set_window_pos(window,400,200)
glfw.make_context_current(window)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glfw.swap_buffers(window)

glfw.terminate()