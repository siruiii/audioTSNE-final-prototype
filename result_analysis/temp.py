import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

# Function to create a sphere
def create_sphere(radius, lats, longs):
    vertices = []
    tex_coords = []
    indices = []

    for i in range(lats + 1):
        lat = np.pi * (-0.5 + float(i) / lats)
        y = np.sin(lat) * radius
        cos_lat = np.cos(lat)

        for j in range(longs + 1):
            lon = 2 * np.pi * float(j) / longs
            x = cos_lat * np.cos(lon) * radius
            z = cos_lat * np.sin(lon) * radius
            vertices.append((x, y, z))
            tex_coords.append((j / longs, i / lats))  # Texture coordinates

    for i in range(lats):
        for j in range(longs):
            first = i * (longs + 1) + j
            second = first + longs + 1
            indices.extend([first, second, first + 1, second, second + 1, first + 1])

    vertices = np.array(vertices, dtype=np.float32)
    tex_coords = np.array(tex_coords, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)
    return vertices, tex_coords, indices

# Load texture from equirectangular image
def load_texture(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(img, np.uint8)
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    return texture_id

# Render function to draw the sphere
def render_sphere(vertices, tex_coords, indices, texture_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glTexCoordPointer(2, GL_FLOAT, 0, tex_coords)
    
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, indices)
    
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisable(GL_TEXTURE_2D)

# Main function to set up OpenGL and run the sphere rendering
def main(image_path):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    glEnable(GL_DEPTH_TEST)  # Enable depth testing
    
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    radius = 2
    lats = 30
    longs = 30

    vertices, tex_coords, indices = create_sphere(radius, lats, longs)
    texture_id = load_texture(image_path)

    clock = pygame.time.Clock()
    
    rotate_x = 0
    rotate_y = 0
    last_x, last_y = display[0] // 2, display[1] // 2
    dragging = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    dragging = True
                    last_x, last_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    dragging = False
            elif event.type == MOUSEMOTION:
                if dragging:
                    x, y = event.pos
                    dx = x - last_x
                    dy = y - last_y
                    rotate_x += dy * 0.5
                    rotate_y += dx * 0.5
                    last_x, last_y = x, y
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        glRotatef(rotate_x, 1, 0, 0)
        glRotatef(rotate_y, 0, 1, 0)
        
        render_sphere(vertices, tex_coords, indices, texture_id)
        
        glPopMatrix()
        
        pygame.display.flip()
        clock.tick(60)

# Run the main function with the path to your equirectangular image
main('A1_Skybox.webp')
