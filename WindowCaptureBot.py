import numpy as np
import win32gui,win32ui
from ctypes import windll
from colorama  import Style,Fore
from modulos.mod import resize_window

class WindowCapture:
    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            print(f'{Fore.RED}Ventana no Encontrada: {window_name}{Style.RESET_ALL}')

        resize_window(self.hwnd)

        self.border_pixels = 8
        self.titlebar_pixels = 30
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        self.w = right - left
        self.h = bottom - top

        self.w = self.w - (self.border_pixels * 2)
        self.h = self.h - self.titlebar_pixels - self.border_pixels
        self.cropped_x = self.border_pixels
        self.cropped_y = self.titlebar_pixels

    def screenshot(self):        

        #Calcular el centro de la ventana 
        center_x_vent = self.cropped_x + self.w // 2
        center_y_vent = self.cropped_y + self.h // 2

        hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, self.w, self.h)
        save_dc.SelectObject(bitmap)

        # If Special K is running, this number is 3. If not, 1
        result = windll.user32.PrintWindow(self.hwnd, save_dc.GetSafeHdc(), 3)
        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)
        img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        img = img[..., :3]
        img = np.ascontiguousarray(img)  # make image C_CONTIGUOUS and drop alpha channel

        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwnd_dc)

        return img, center_x_vent, center_y_vent

    def get_window_size(self):
        return (self.w, self.h)



