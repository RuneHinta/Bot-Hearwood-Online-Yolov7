import math
import win32gui
import pyautogui
from time import sleep
import numpy as np



def calculate_distance(Xcenter_pj, Ycenter_pj, Xobject_center, Yobject_center):    
    

    # Calculamos la distancia entre Centro del persoje y el centro del objeto
    center_pj = Xcenter_pj , Ycenter_pj
    center_object = Xobject_center, Yobject_center
    # Calculamos la distancia 
    # distance = math.sqrt((center_pj[0] - center_object[0]) ** 2 + (center_pj[1] - center_object[1]) ** 2)
    distance  = math.sqrt(math.pow(center_pj[0] - center_object[0], 2) + math.pow(center_pj[1] - center_object[1], 2))
    calculate_direction(Xobject_center, Yobject_center, Xcenter_pj, Ycenter_pj ,distance)
    

def calculate_direction(target_x, target_y, centerXpj, centerYpj, distance):
    # Calculamos la dirección y la distancia hacia el objetivo
    direction_x = target_x - centerXpj
    direction_y = target_y - centerYpj

def move_to_nearest_match(self, coordinates_list, center_x, center_y):

    #Cálculo de Distancias:
    distances = [np.sqrt((x - center_x)**2 + (y - center_y)**2) for x, y in coordinates_list]

    # Inicializa direction_x y direction_y
    direction_x, direction_y = 0, 0

    if distances:
        nearest_index = np.argmin(distances)
        nearest_distance = distances[nearest_index]

    if nearest_distance < 300:
            nearest_x, nearest_y = coordinates_list[nearest_index]

            direction_x = nearest_x - center_x
            direction_y = nearest_y - center_y

            print(f"Moviendo hacia la coincidencia más cercana: ({nearest_x}, {nearest_y})")
            print(f"Dirección X: {direction_x}, Dirección Y: {direction_y}")

            velocidad = 800
            tiempo_estimado_x = abs(direction_x) / velocidad
            tiempo_estimado_y = abs(direction_y) / velocidad
            tiempo_estimado = max(tiempo_estimado_x, tiempo_estimado_y)

            pyautogui.keyDown('d') if direction_x > 0 else pyautogui.keyDown('a')
            pyautogui.keyDown('s') if direction_y > 0 else pyautogui.keyDown('w')
            sleep(tiempo_estimado)
            pyautogui.keyUp('d') if direction_x > 0 else pyautogui.keyUp('a')
            pyautogui.keyUp('s') if direction_y > 0 else pyautogui.keyUp('w')
            print(f'{tiempo_estimado}')
            
            margen_de_error = 60  # Ajusta según sea necesario
            if abs(direction_x) <= margen_de_error and abs(direction_y) <= margen_de_error:
                print("El personaje está cerca del objetivo. Realizar acciones adicionales.")


def resize_window(hwnd):

    if hwnd != 0:
        # Cambia el tamaño de la ventana
        new_width = 540
        new_height = 440
        win32gui.MoveWindow(hwnd, 0, 0, new_width, new_height, True)
    else:
        print(f"No se encontró la ventana '.")
