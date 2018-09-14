from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Last time when sphere was re-displayed
last_time = 0








# The sphere class
class Sphere:

    # Constructor for the sphere class
    def __init__(self, radius):

        # Radius of sphere
        self.radius = radius

        # Number of latitudes in sphere
        self.lats = 50

        # Number of longitudes in sphere
        self.longs = 50

        self.user_theta = 0
        self.user_height = 0

        # Direction of light
        self.direction = [0.0, 2.0, -1.0, 1.0]

        # Intensity of light
        self.intensity = [0.7, 0.7, 0.7, 1.0]

        # Intensity of ambient light
        self.ambient_intensity = [0.3, 0.3, 0.3, 1.0]

        # The surface type(Flat or Smooth)
        self.surface = GL_FLAT

    # Initialize
    def init(self):

        # Set background color to black
        glClearColor(0.0, 0.0, 0.0, 0.0)

        self.compute_location()

        # Set OpenGL parameters
        glEnable(GL_DEPTH_TEST)

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Set light model
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.ambient_intensity)

        # Enable light number 0
        glEnable(GL_LIGHT0)

        # Set position and intensity of light
        glLightfv(GL_LIGHT0, GL_POSITION, self.direction)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.intensity)

        # Setup the material
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    def ONB(self):
        origin = (0, 0, 0)
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


    # Compute location
    def compute_location(self):
        x = 2 * cos(self.user_theta)
        y = 2 * sin(self.user_theta)
        z = self.user_height
        d = sqrt(x * x + y * y + z * z)

        # Set matrix mode
        glMatrixMode(GL_PROJECTION)

        # Reset matrix
        glLoadIdentity()
        glFrustum(-d * 0.5, d * 0.5, -d * 0.5, d * 0.5, d - 1.1, d + 1.1)

        # Set camera
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

    # Display the sphere
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set color to white
        glColor3f(1.0, 1.0, 1.0)

        # Set shade model
        glShadeModel(self.surface)

        self.draw()
        glutSwapBuffers()

    # Draw the sphere
    def draw(self):
        for i in range(0, self.lats + 1):
            lat0 = pi * (-0.5 + float(float(i - 1) / float(self.lats)))
            z0 = sin(lat0)
            zr0 = cos(lat0)

            lat1 = pi * (-0.5 + float(float(i) / float(self.lats)))
            z1 = sin(lat1)
            zr1 = cos(lat1)

            # Use Quad strips to draw the sphere
            glBegin(GL_QUAD_STRIP)

            list_vertices = []
            for j in range(0, self.longs + 1):
                lng = 2 * pi * float(float(j - 1) / float(self.longs))
                x = cos(lng)
                y = sin(lng)
                vertex_a = (x * zr0, y * zr0, z0)
                vertex_b = (x * zr1, y * zr1, z1)
                list_vertices.append(vertex_a)
                glNormal3fv(vertex_a)
                glVertex3fv(vertex_a)
                glNormal3fv(vertex_b)
                glVertex3fv(vertex_b)
            glEnd()

        glTranslate(0,0,1)
        self.ONB()
        glTranslate(0,0,-1)


    # Keyboard controller for sphere
    def special(self, key, x, y):

        # Scale the sphere up or down
        if key == GLUT_KEY_UP:
            self.user_height += 0.1
        if key == GLUT_KEY_DOWN:
            self.user_height -= 0.1

        # Rotate the cube
        if key == GLUT_KEY_LEFT:
            self.user_theta += 0.1
        if key == GLUT_KEY_RIGHT:
            self.user_theta -= 0.1

        # Toggle the surface
        if key == GLUT_KEY_F1:
            if self.surface == GL_FLAT:
                self.surface = GL_SMOOTH
            else:
                self.surface = GL_FLAT

        self.compute_location()
        glutPostRedisplay()

    # The idle callback
    def idle(self):
        global last_time
        time = glutGet(GLUT_ELAPSED_TIME)

        if last_time == 0 or time >= last_time + 40:
            last_time = time
            glutPostRedisplay()

    # The visibility callback
    def visible(self, vis):
        if vis == GLUT_VISIBLE:
            glutIdleFunc(self.idle)
        else:
            glutIdleFunc(None)


# The main function
def main():

    # Initialize the OpenGL pipeline
    glutInit(sys.argv)

    # Set OpenGL display mode
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

    # Set the Window size and position
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(100, 100)

    # Create the window with given title
    glutCreateWindow('Sphere')

    # Instantiate the sphere object
    s = Sphere(5.0)

    s.init()

    # Set the callback function for display
    glutDisplayFunc(s.display)

    # Set the callback function for the visibility
    glutVisibilityFunc(s.visible)

    # Set the callback for special function
    glutSpecialFunc(s.special)

    # Run the OpenGL main loop
    glutMainLoop()


# Call the main function
if __name__ == '__main__':
    main()





# radius = 1
# longs = 100
# lats = 100
# for i in range(0, longs):
#     glBegin(GL_LINE_LOOP)
#     theta = i * (360 / longs) * (math.pi / 180)
#     for j in range(0, lats):
#         phi = j * (180 / lats) * (math.pi / 180)
#         x = radius * math.sin(phi) * math.cos(theta)
#         y = radius * math.sin(phi) * math.sin(theta)
#         z = radius * math.cos(phi)
#         glVertex3f(x, y, z)
#     glEnd()
