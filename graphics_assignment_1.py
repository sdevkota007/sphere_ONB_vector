#CODE BY SUDARSHAN DEVKOTA

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math
from math import *

name = 'GRAPHICS_ASSIGNMENT_SPHERE_ONB'

user_x=0
user_z=20
user_radius = math.sqrt(user_x*user_x + user_z*user_z)
user_theta = 0
ORIGIN = (0,0,0)
RED = (1,0,0)
GREEN = (0,1,0)
BLUE = (0,0,1)
RADIUS = 5
lats = 15
longs = 15


def compute_sphere_coordinates():

    list_of_lats = []
    for i in range(0, lats + 1):
        lat0 = pi * (-0.5 + float(float(i - 1) / float(lats)))
        z0 = sin(lat0)
        zr0 = cos(lat0)

        lat1 = pi * (-0.5 + float(float(i) / float(lats)))
        z1 = sin(lat1)
        zr1 = cos(lat1)

        list_vertices = []
        for j in range(0, longs + 1):
            lng = 2 * pi * float(float(j - 1) / float(longs))
            x = cos(lng)
            y = sin(lng)
            vertex_a = (RADIUS*x*zr0, RADIUS*z0, RADIUS*y*zr0)
            vertex_b = (RADIUS*x*zr1, RADIUS*z1, RADIUS*y*zr1)

            list_vertices.append([vertex_a, vertex_b])


        list_of_lats.append(list_vertices)

    return list_of_lats


def draw_ONB_around_sphere(list_of_latitudes):
    for latitude in list_of_latitudes:
        for vertex_a, vertex_b in latitude:
            x,y,z = vertex_a
            w_norm, u_norm, v_norm =  computeONB(vertex_a)
            glTranslatef(x,y,z)
            glBegin(GL_LINES)

            glColor3fv(BLUE)
            glVertex3fv(ORIGIN)
            glVertex3fv(w_norm)

            glColor3fv(RED)
            glVertex3fv(ORIGIN)
            glVertex3fv(u_norm)

            glColor3fv(GREEN)
            glVertex3fv(ORIGIN)
            glVertex3fv(v_norm)

            glEnd()
            glTranslatef(-x,-y,-z)

def draw_sphere(list_of_latitudes):
    for latitude in list_of_latitudes:
        #using quad_strips to draw sphere
        glBegin(GL_QUAD_STRIP)
        for vertex_a, vertex_b in latitude:
            glNormal3fv(vertex_a)
            glColor3fv(calculate_color(normalize(vertex_a)))
            glVertex3fv(vertex_a)

            glNormal3fv(vertex_b)
            glColor3fv(calculate_color(normalize(vertex_b)))
            glVertex3fv(vertex_b)

        glEnd()




def cross_product(a,b):
    c = (a[1] * b[2] - a[2] * b[1],
         a[2] * b[0] - a[0] * b[2],
         a[0] * b[1] - a[1] * b[0])
    return c

def generate_t(w):
    min_value = min(w)
    min_value_pos = w.index(min_value)
    t = w[:min_value_pos] + (1,) + w[min_value_pos + 1:]  # replaces the minimum value by 1
    return t

def computeONB(w):
    w_norm = normalize(w)
    t = generate_t(w_norm)
    u_norm = normalize(cross_product(t,w_norm))
    v_norm = cross_product(w_norm,u_norm)
    return w_norm, u_norm, v_norm



def normalize((x,y,z)):
    magnitude = sqrt(x*x + y*y + z*z)
    return (x/magnitude, y/magnitude, z/magnitude)

def calculate_color(normal):
    color_tup = tuple((x+1)/2 for x in normal)
    return color_tup


def resize(width, height):
    ratio = 1.0 * width/height
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    gluPerspective(45.0, ratio, 0.1, 100.0)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(user_x, 0, user_z, 0, 0, 0, 0, 1, 0)

    sphere_coordinates = compute_sphere_coordinates()

    # glRotate(90,1,0,0)
    draw_sphere(sphere_coordinates)
    draw_ONB_around_sphere(sphere_coordinates)
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

    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutKeyboardFunc(keyPressed)

    glutMainLoop()
    return

if __name__ == '__main__':
    main()