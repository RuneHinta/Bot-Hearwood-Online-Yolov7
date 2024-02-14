import cv2
import torch
import os
import keyboard
from colorama import Fore, Style
from tqdm import tqdm
from time import time
from WindowCaptureBot import *
from modulos.mod import calculate_distance
from utilidades.Classeclick import *



    

os.environ["CUDA_VISIBLE_DEVICES"] = "0"  
# เลือกอุปกรณ์ GPU หรือ CPU 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
# Load YOLOv7 model
model = torch.hub.load("WongKinYiu/yolov7", "custom", "modelonew.pt",force_reload=True)
model = model.to(device)

coincidencia =0.3


loop_time = time()
windowname = 'Heartwood Online'
windows = WindowCapture(windowname)
#classeclick= Click(windowname)

# Mapeo de colores para cada clase
class_colors = {
    'Coal': (255, 255, 0),  # Color verde
    'TinOre': (255, 255, 0),  # Color rojo
    'Cotton': (114, 167, 153), # Color celeste
    'Bunny': (76, 0, 153), # Morado
    # Añadir más clases y colores según sea necesario
}
while True: 

    screenshot, centerXpj, centerYpj = windows.screenshot()
    results = model(screenshot)
    black_screen = np.zeros_like(screenshot)

    boxes = results.pred[0][:, :4].detach().cpu().numpy()
    labels = results.pred[0][:, -1].detach().cpu().numpy()
    #coincidencia 
    confidences = results.pred[0][:, -2].detach().cpu().numpy()

    centerXpj -= 10
    centerYpj -= 25

    for box, label, confidence in zip(boxes, labels, confidences):

        if confidence >= coincidencia:
            x1, y1, x2, y2 = box.astype(int)
            class_name = model.names[int(label)]

            #calculamos el centro del objeto
            object_center_x = (x1 + x2) // 2
            object_center_y = (y1 + y2) // 2
            
            
            
            #distance = calculate_distance(centerXpj, centerYpj, object_center_x, object_center_y)            
            #dist =str (round(distance, 3))
            # imprimos cordenadas 
            print(f"{Fore.GREEN} x={object_center_x}  y ={object_center_y} = {class_name}{Style.RESET_ALL}")
            
            class_color = class_colors.get(class_name, (0, 255, 0)) 
            
            # Dibujar el rectángulo con el color de la clase
            cv2.rectangle(black_screen, (x1, y1), (x2, y2), class_color, 1)

            cv2.line(black_screen, (centerXpj, centerYpj),  (object_center_x, object_center_y), color=(0, 0, 255), thickness=1)
                       
            #cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.putText(black_screen, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (class_color), 1)
            
            target_x, target_y = object_center_x, object_center_y

    # Calculamos la dirección y la distancia hacia el objetivo
    calculate_distance(centerXpj, centerYpj, target_x, target_y)  
    
     


    cv2.imshow('Game', black_screen)
    #cv2.imshow('Games', screenshot)
    if cv2.waitKey(1) & keyboard.is_pressed('P') :#0xFF == ord('q')
       cv2.destroyAllWindows()
       
       break
       
    

#cv2.destroyAllWindows()
