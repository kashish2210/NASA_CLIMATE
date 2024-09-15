import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import os
import math
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

# Initialize Pygame
pygame.init()

# List of textures
texture_list = [f"texture_file/{i}.jpg" for i in range(1, 11)]  # Update texture paths
current_texture_index = 0
current_texture_id = None

# Load textures
def load_texture(texture_file):
    global current_texture_id
    try:
        img = Image.open(texture_file)
        img = img.convert("RGB")
        img_data = img.tobytes("raw", "RGB", 0, -1)

        # Generate and bind texture
        current_texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, current_texture_id)

        # Set texture parameters
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        print(f"Loaded texture: {texture_file}")

    except Exception as e:
        print(f"Failed to load texture {texture_file}: {e}")

# Function to switch to the next texture
def change_texture():
    global current_texture_index
    current_texture_index = (current_texture_index + 1) % len(texture_list)
    load_texture(texture_list[current_texture_index])

# Function to switch to the previous texture
def previous_texture():
    global current_texture_index
    current_texture_index = (current_texture_index - 1) % len(texture_list)
    load_texture(texture_list[current_texture_index])

# Draw the sphere with the texture
def draw_sphere():
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    glBindTexture(GL_TEXTURE_2D, current_texture_id)
    gluSphere(quad, 1, 50, 50)

# Draw the grid over the sphere
def draw_grid(radius, slices, stacks):
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(1.0)
    # Draw latitude lines
    for i in range(1, stacks):
        lat = math.pi * (-0.5 + float(i) / stacks)
        z = radius * math.sin(lat)
        r = radius * math.cos(lat)

        glBegin(GL_LINE_LOOP)
        for j in range(slices):
            lng = 2 * math.pi * float(j) / slices
            x = r * math.cos(lng)
            y = r * math.sin(lng)
            glVertex3f(x, y, z)
        glEnd()

    # Draw longitude lines
    for j in range(slices):
        lng = 2 * math.pi * float(j) / slices
        glBegin(GL_LINE_STRIP)
        for i in range(stacks + 1):
            lat = math.pi * (-0.5 + float(i) / stacks)
            x = radius * math.cos(lat) * math.cos(lng)
            y = radius * math.cos(lat) * math.sin(lng)
            z = radius * math.sin(lat)
            glVertex3f(x, y, z)
        glEnd()

# PyQt5 interface for buttons and fullscreen
class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(OpenGLWidget, self).__init__(parent)
        self.zoom = -5
        self.rotate_x = 0
        self.rotate_y = 0
        self.mouse_dragging = False
        self.last_mouse_pos = None

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, 800 / 600, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        load_texture(texture_list[current_texture_index])

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, self.zoom)
        glRotatef(self.rotate_x, 1, 0, 0)
        glRotatef(self.rotate_y, 0, 1, 0)
        glBindTexture(GL_TEXTURE_2D, current_texture_id)
        
        # Draw the textured sphere
        draw_sphere()
        
        # Draw the grid
        draw_grid(1, 36, 18)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_dragging = True
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mouse_dragging:
            delta = event.pos() - self.last_mouse_pos
            self.rotate_x += delta.y() * 0.5
            self.rotate_y += delta.x() * 0.5
            self.last_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_dragging = False

    def wheelEvent(self, event):
        self.zoom += event.angleDelta().y() * 0.01
        self.update()

    # Handle key press events for texture changes
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            change_texture()  # Go to the next texture
            self.update()
        elif event.key() == Qt.Key_PageDown:
            previous_texture()  # Go to the previous texture
            self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("3D Earth Model with Grid, Texture Switching, and Zoom")
        self.setGeometry(100, 100, 800, 600)

        self.opengl_widget = OpenGLWidget(self)
        self.setCentralWidget(self.opengl_widget)

        # Add buttons for texture switching
        self.initUI()

    def initUI(self):
        container = QWidget(self)
        layout = QVBoxLayout(container)

        # Next Texture button
        next_texture_btn = QPushButton('Next Texture', self)
        next_texture_btn.clicked.connect(change_texture)
        layout.addWidget(next_texture_btn)

        # Previous Texture button
        prev_texture_btn = QPushButton('Previous Texture', self)
        prev_texture_btn.clicked.connect(previous_texture)
        layout.addWidget(prev_texture_btn)

        # Set the layout
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
