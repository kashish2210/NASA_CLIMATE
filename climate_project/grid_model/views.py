# grid_model/views.py
from django.shortcuts import render
# grid_model/views.py
import os
import subprocess
from django.http import HttpResponse


import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import os
import math
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from .test import  MainWindow

def run_testpy(request):
    try:
        # Update with the correct path to your test.py script
        script_path = os.path.join(os.path.dirname(__file__), 'test.py')
        subprocess.Popen(['python', script_path])

        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
        print("eone")

        return HttpResponse(status=200)  # Success response
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)  # Error response


# View for the grid model page
def grid_page(request):
    return render(request, 'grid_page.html')

def index(request):
    return render(request, 'index.html')

