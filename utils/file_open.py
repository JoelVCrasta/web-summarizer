import tkinter as tk
from tkinter import filedialog
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def open_file():
    try:
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title='Choose a text file',
            filetypes=[('Text files', '*.txt')]
        )

        root.destroy()

        if not file_path:
            raise FileNotFoundError("No file selected")
        
        return file_path
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise RuntimeError("An error occurred while opening the file explorer")

def read_text_from_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        raise FileNotFoundError("The file does not exist")
    
    except IOError as e:
        logger.error(f"Error: {e}")
        raise RuntimeError("An error occurred while reading the file")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        raise RuntimeError("Something went wrong while reading the file")


