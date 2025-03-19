import tkinter as tk
from tkinter import ttk
import pyautogui
import time
from PIL import ImageGrab, ImageTk
import win32api
import win32con
import threading
import keyboard

class CursorClicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Auto-Clicker Thingies")
        self.root.attributes('-topmost', True)
        self.root.geometry("400x300")  # Made window larger for coordinate list
        
        # Variables
        self.TARGET_COLOR = (156, 194, 255)
        self.COLOR_THRESHOLD = 50
        self.markers = []  # Will store {position: (x,y), clicked: False}
        self.running = False
        
        self.create_ui()
        self.start_checking()

    def create_ui(self):
        # Control Frame
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill="x")
        
        # Add buttons (unchanged)
        self.add_button = ttk.Button(control_frame, text="Add Point (F8)", command=self.add_marker)
        self.add_button.pack(side="left", padx=5)
        
        self.toggle_button = ttk.Button(control_frame, text="Start (F6)", command=self.toggle_checking)
        self.toggle_button.pack(side="left", padx=5)
        
        self.clear_button = ttk.Button(control_frame, text="Clear Points", command=self.clear_markers)
        self.clear_button.pack(side="left", padx=5)
        
        # Coordinates List Frame
        self.coords_frame = ttk.Frame(self.root, padding="10")
        self.coords_frame.pack(fill="both", expand=True)
        
        # Status Label
        self.status_label = ttk.Label(control_frame, text="Press F8 to add points")
        self.status_label.pack(side="right", padx=5)
        
        # Setup keyboard hooks (unchanged)
        keyboard.on_press_key("F8", lambda _: self.add_marker())
        keyboard.on_press_key("F6", lambda _: self.toggle_checking())
        keyboard.on_press_key("F7", lambda _: self.root.quit())

    def add_marker(self):
        if not self.running:
            x, y = win32api.GetCursorPos()
            marker = {
                'position': (x, y),
                'clicked': False,
                'label': None
            }
            self.markers.append(marker)
            self.update_coordinate_list()
            self.status_label.configure(text=f"Added point at ({x}, {y})")

    def update_coordinate_list(self):
        # Clear existing labels
        for widget in self.coords_frame.winfo_children():
            widget.destroy()
        
        # Add header
        ttk.Label(self.coords_frame, text="Coordinates List:").pack(anchor="w")
        
        # Add each coordinate
        for i, marker in enumerate(self.markers):
            x, y = marker['position']
            frame = ttk.Frame(self.coords_frame)
            frame.pack(fill="x", pady=2)
            
            # Arrow button to locate point
            btn = ttk.Button(frame, text="→", width=3, 
                           command=lambda pos=(x,y): win32api.SetCursorPos(pos))
            btn.pack(side="left", padx=(0,5))
            
            # Coordinate text
            ttk.Label(frame, text=f"Point {i+1}: ({x}, {y})").pack(side="left")

    def clear_markers(self):
        self.markers.clear()
        self.update_coordinate_list()
        self.status_label.configure(text="All points cleared")

    def start_checking(self):
        if self.running:
            for i, marker in enumerate(self.markers):
                if not marker['clicked']:
                    x, y = marker['position']
                    if self.check_color(x, y):
                        print(f"[Marker {i}] Color match found - Clicking...")
                        # Click immediately without any delay or window manipulation
                        self.click(x, y)
                        marker['clicked'] = True
                        print(f"[Marker {i}] Click completed")
        
        self.root.after(1000, self.start_checking)

    # Remove the duplicate start_checking method and delayed_click method as they're no longer needed
    def clear_markers(self):
        for marker in self.markers:
            marker['window'].destroy()
        self.markers.clear()
        self.status_label.configure(text="All points cleared")

    def toggle_checking(self):
        self.running = not self.running
        if self.running:
            self.toggle_button.configure(text="Stop (F6)")
            self.status_label.configure(text="Monitoring points")
            # Reset clicked status
            for marker in self.markers:
                marker['clicked'] = False
        else:
            self.toggle_button.configure(text="Start (F6)")
            self.status_label.configure(text="Monitoring stopped")

    def check_color(self, x, y):
        try:
            area = (x-5, y-5, x+6, y+6)  # Increased area for better detection
            screenshot = ImageGrab.grab(area)
            
            # Check all pixels in the area
            colors_found = []
            for px in range(screenshot.width):
                for py in range(screenshot.height):
                    color = screenshot.getpixel((px, py))
                    colors_found.append(color)
                    
                    # Check if color matches (with threshold)
                    if all(abs(c1 - c2) <= self.COLOR_THRESHOLD for c1, c2 in zip(color, self.TARGET_COLOR)):
                        print(f"✓ Color match at ({x}, {y}): Found RGB{color} vs Target RGB{self.TARGET_COLOR}")
                        return True
            
            # If no match found, print some sample colors
            print(f"× No match at ({x}, {y}). Sample colors found: {colors_found[:5]}")
            print(f"  Target color is RGB{self.TARGET_COLOR}")
            return False
            
        except Exception as e:
            print(f"Error checking color: {e}")
            return False

    def start_checking(self):
        if self.running:
            for i, marker in enumerate(self.markers):
                if not marker['clicked']:
                    x, y = marker['position']
                    if self.check_color(x, y):
                        print(f"[Marker {i}] Color match found - Processing...")
                        window = marker['window']
                        
                        # Hide marker completely and ensure it's not blocking
                        window.attributes('-alpha', 0)  # Make fully transparent
                        window.lower()  # Put behind all windows
                        window.update()  # Force update window state
                        
                        # Schedule click immediately
                        self.root.after(100, lambda m=marker, idx=i, pos=(x,y): self.delayed_click(m, idx, pos))
                        
                        # Schedule marker return after click
                        def return_marker(w, m):
                            w.attributes('-alpha', 0.6)  # Restore transparency
                            w.lift()  # Bring back to front
                            m['clicked'] = False  # Reset clicked status
                        
                        self.root.after(5000, lambda: return_marker(window, marker))
        
        self.root.after(1000, self.start_checking)

    def delayed_click(self, marker, index, position):
        if not marker['clicked'] and self.running:
            x, y = position  # Use original position for clicking
            print(f"[Marker {index}] Clicking at original position ({x}, {y})")
            self.click(x, y)
            marker['clicked'] = True
            print(f"[Marker {index}] ✓ Click completed")

    def click(self, x, y):
        try:
            print(f"Clicking at ({x}, {y})")
            # Move cursor and perform click
            win32api.SetCursorPos((x, y))
            time.sleep(0.1)  # Wait for cursor to move
            
            # Send direct click events
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.1)
            
            print(f"Click completed at ({x}, {y})")
        except Exception as e:
            print(f"Error clicking: {e}")

    def start_checking(self):
        if self.running:
            for i, marker in enumerate(self.markers):
                if not marker['clicked']:
                    x, y = marker['position']
                    if self.check_color(x, y):
                        print(f"[Marker {i}] Color match found - Clicking...")
                        self.click(x, y)
                        marker['clicked'] = True
                        # Reset after 5 seconds using dictionary syntax
                        self.root.after(5000, lambda m=marker: m.update({'clicked': False}))
        
        self.root.after(100, self.start_checking)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CursorClicker()
    app.run()