from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math

name = 'OpenGL Python Teapot'

user_x=0
user_z=20
user_radius = math.sqrt(user_x*user_x + user_z*user_z)
user_theta = 0

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


def ONB():
    origin= (0,0,0)
    basis_vector = ((1, 0, 0),
                    (0, 1, 0),
                    (0, 0, 1))
    glBegin(GL_LINES)
    for vector in basis_vector:
        glColor3fv(vector)
        glVertex3fv(vector)
        glVertex3fv(origin)

    # glVertex3fv(0, 0, 0)
    # glVertex3fv(5, 5, 5)
    glEnd()

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def sphere():

    # float radius = 1.0f;
    # for (int i = 0; i <= 360; i++) {
    #     gl.glBegin(GL2.GL_LINE_LOOP);
    #     float theta = i * (Math.PI / 180.0f);
    #     for (int j = 0; j <= 180; j++) {
    #         float phi = j * (Math.PI / 180.0f);
    #         float x = radius * Math.sin(phi) * Math.cos(theta);
    #         float y = radius * Math.sin(phi) * Math.sin(theta);
    #         float z = radius * Math.cos(phi);
    #         gl.glVertex3f(x, y, z);
    #     }
    #     gl.glEnd();
    # }

    radius = 5
    longs = 360
    lats = 180

    for i in range(0, longs):
        # if (i % 10) == 0:
            glBegin(GL_LINE_STRIP)
            theta = i* (math.pi/180) * (360/longs)
            for j in range(0, lats):
                # if (j % 100) == 0:
                    phi = j* (math.pi/180) * (180/lats)
                    x = radius * math.sin(phi) * math.cos(theta)
                    y = radius * math.sin(phi) * math.sin(theta)
                    z = radius * math.cos(phi)
                    glNormal3f(x, y, z)
                    glVertex3f(x, y, z)

            glEnd()


# def ONB()
#     glbegin()

def resize(width, height):
    ratio = 1.0 * width/height
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    gluPerspective(45.0, ratio, 0.1, 100.0)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    print user_x, user_z
    gluLookAt(user_x, 5, user_z, 0, 0, 0, 0, 1, 0)

    # Cube()

    sphere()
    glTranslate(0,0,5)
    ONB()
    # glutWireTeapot(5)
    glutSwapBuffers()

    return


def compute_lookat():
    user_theta_rad = user_theta * (math.pi/180)
    global user_x
    user_x = user_radius * math.sin(user_theta_rad)

    global user_z
    user_z = user_radius * math.cos(user_theta_rad)

def keyPressed(*args):
    # Rotate the cube
    if args[0] == 'a':
        global user_theta
        user_theta -= 1
    if args[0] == 'd':
        global user_theta
        user_theta += 1

    compute_lookat()
    glutPostRedisplay()


def main():
    glutInit(sys.argv)

    glutInitWindowPosition(100,100)
    glutInitWindowSize(800, 600)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutCreateWindow(name)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutKeyboardFunc(keyPressed)

    glutMainLoop()
    return

if __name__ == '__main__':
    main()