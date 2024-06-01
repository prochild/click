import pyautogui
import time
import tkinter as tk
from threading import Thread

running = False

def find_and_click_button(image_path, delay_after_click=2):
    global running
    try:
        # 버튼 이미지 위치 찾기
        button_location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        
        if button_location:
            # 버튼 이미지의 중앙 좌표 계산
            button_center = pyautogui.center(button_location)
            
            # 중앙 좌표로 마우스 이동 후 클릭
            pyautogui.moveTo(button_center.x, button_center.y)
            pyautogui.click()
            
            log(f"Clicked on the button at {button_center}")
            
            # 클릭 후 일정 시간 대기
            time.sleep(delay_after_click)
            
            return True
    except pyautogui.ImageNotFoundException:
        log(f"{image_path} not found. Retrying...")
        
    return False

def main():
    global running
    search_interval = 15  # 검색 주기를 15초로 고정
    
    button1_image_path = "next_chapter.png"
    button2_image_path = "OK.png"

    log("Press Ctrl+C to stop the program.")
    
    while running:
        # 첫 번째 버튼 클릭 시도
        if find_and_click_button(button1_image_path):
            log("First button clicked.")
        
        # 15초 대기
        time.sleep(search_interval)
        
        if not running:
            break
        
        # 두 번째 버튼 클릭 시도
        if find_and_click_button(button2_image_path):
            log("Second button clicked.")
        
        # 15초 대기
        time.sleep(search_interval)

def log(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, f"{message}\n")
    log_text.config(state=tk.DISABLED)
    log_text.see(tk.END)

def start_thread():
    global running
    if not running:
        running = True
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        thread = Thread(target=main)
        thread.daemon = True
        thread.start()

def stop_thread():
    global running
    if running:
        running = False
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        log("Program stopped.")

def on_closing():
    global running
    running = False
    root.quit()

# GUI 설정
root = tk.Tk()
root.title("Button Clicker")

frame = tk.Frame(root)
frame.pack(pady=10, padx=10)

log_text = tk.Text(frame, height=20, width=50, state=tk.DISABLED)
log_text.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

start_button = tk.Button(button_frame, text="Start", command=start_thread)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="Stop", command=stop_thread, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, padx=5)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
