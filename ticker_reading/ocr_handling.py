from PIL import Image, ImageEnhance
import pytesseract
import pyautogui
import time
import yfinance as yf
from multiprocessing import Queue

# x: 1994 - 2106
# y: 94 - 147


def ocr_thread(q: Queue, original_ticker: str, region_q: Queue):
    """
    Continuously monitors the ticker region, performs OCR, and updates the queue
    when a new ticker is detected and confirmed.
    """

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    same_ticker_count = 0
    new_ticker = ""
    region = None

    while True:   
        region = poll_region_queue(region, region_q)

        # Take a partial screenshot and preprocess the image
        image = pyautogui.screenshot(region=region).convert('L')
        image = ImageEnhance.Contrast(image).enhance(2)

        # Perform OCR
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config).strip()

        # Validate the new ticker
        if text != original_ticker and valid_ticker(text):
            if new_ticker == text:
                same_ticker_count += 1
            else:
                new_ticker = text
                same_ticker_count = 1

        # Confirm the new ticker if it appears consistently
        if same_ticker_count >= 3:
            print(f"Confirmed new ticker: {new_ticker}")
            new_ticker = new_ticker.upper()
            q.put(new_ticker)
            original_ticker = new_ticker
            same_ticker_count = 0

        # Reset if the detected text changes
        elif new_ticker != text:
            same_ticker_count = 0

        time.sleep(0.1)


def poll_region_queue(current_region, region_q: Queue) -> tuple[int]:
    if not region_q.empty():
        return region_q.get()
    return current_region



def valid_ticker(text: str):
    if text is None:
        return False

    if text.isalpha():
        #print(f"TICKER {text}")
        #if ticker_exists(text):
        return True    
    return False

def ticker_exists(ticker: str):
    """Checks with yahoo finance to see if a ticker exists"""
    stock = yf.Ticker(ticker)
    info = stock.history(period="7d", interval="1d")

    exists = len(info) > 0

    if exists:
        region = stock.get_info()["region"]
        print(f"region: {region}")
        if region == "US":
            return True
        else:
            return False
    return False



def get_current_ticker(q_ticker_region: Queue):

    screenshot_path = r'ticker_reading\partial_screenshot.png'

    # Define region (x, y, width, height)

    if q_ticker_region.empty():
        print("Error: Found no starting ticker")
        return

    region = q_ticker_region.get()
    q_ticker_region.put(region) # Puts back to the queue so it's not empty for the ocr_thread

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Take a partial screenshot
    screenshot = pyautogui.screenshot(screenshot_path, region=region)

    image = Image.open(screenshot_path).convert('L')  # Convert to grayscale
    image = ImageEnhance.Contrast(image).enhance(2)  # Increase contrast

    # Perform OCR with custom config
    custom_config = r'--oem 3 --psm 6'
    # Perform OCR on the screenshot
    current_ticker: str = pytesseract.image_to_string(image, config=custom_config)
    current_ticker = current_ticker.strip()
    current_ticker = current_ticker.upper()

    return current_ticker  





