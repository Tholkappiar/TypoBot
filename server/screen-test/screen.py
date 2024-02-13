import time
import cv2
import numpy as np
import pytesseract
import mss
import pyautogui
import keyboard

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to handle mouse events
def mouse_event(event, x, y, flags, param):
    global start_pos, end_pos

    if event == cv2.EVENT_LBUTTONDOWN:
        start_pos = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        end_pos = (x, y)

# Initialize variables to store the coordinates of the selected area
start_pos = None
end_pos = None

# Open a window to display the screen for selection
cv2.namedWindow('Select Area')
cv2.setMouseCallback('Select Area', mouse_event)

# Loop until the user confirms the selection by pressing Enter
while True:
    # Capture the screen
    screen = pyautogui.screenshot()

    # Convert the screen capture to a numpy array
    screen_np = np.array(screen)

    # Display the screen capture
    cv2.imshow('Select Area', cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR))

    # Check if the user has pressed Enter to confirm the selection
    if cv2.waitKey(1) & 0xFF == ord('\r'):
        if start_pos is not None and end_pos is not None:
            break

# Close the window after selection
cv2.destroyAllWindows()

# Calculate the coordinates and dimensions of the selected region
left = min(start_pos[0], end_pos[0])
top = min(start_pos[1], end_pos[1])
width = abs(end_pos[0] - start_pos[0])
height = abs(end_pos[1] - start_pos[1])

# Define the monitor region to capture based on the selected area
mon = {'left': left, 'top': top, 'width': width, 'height': height}

# Initialize a flag to indicate whether the text should be printed
print_text = False

# Function to toggle the print_text flag when the shortcut key is pressed
def toggle_print_text():
    print("yes , printed")
    global print_text
    print_text = not print_text

# Register the shortcut key to toggle the print_text flag
keyboard.add_hotkey('ctrl+shift+p', toggle_print_text)

# Initialize the screen capturing object
with mss.mss() as sct:
    while True:
        try:
            # Capture the screen region defined by 'mon'
            im = np.array(sct.grab(mon))

            # Perform OCR on the captured image
            text = pytesseract.image_to_string(im)

            # Check if the print_text flag is set
            if print_text:
                # Print the recognized text
                print(text)

            # Display the captured image
            cv2.imshow('Image', im)

            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            # Delay to capture one screenshot per second
            time.sleep(1)

        except Exception as e:
            print("An error occurred:", e)
            break
