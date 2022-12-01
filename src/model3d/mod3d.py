from ursina import *

app = Ursina()
# entity
worldcube = Entity(model='cube', color=color.red, texture='white_cube', scale=(3,3,3))
minicube = Entity(parent=worldcube, model='cube', color=color.blue, texture='white_cube', position=(0,0.75,0), scale=(0.5,0.5,0.5))
