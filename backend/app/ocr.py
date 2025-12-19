import pytesseract
from PIL import Image
import io

async def extract_text_from_image(image_data: bytes) -> str:
    """
    Uses Tesseract OCR to extract text from an in-memory image.

    :param image_data: The image file in bytes.
    :return: The extracted text as a string.
    """
    # Open the image from the in-memory bytes
    image = Image.open(io.BytesIO(image_data))
    
    # Use pytesseract to extract text
    # You can specify a language, e.g., lang='eng'
    text = pytesseract.image_to_string(image)
    
    return text

