# solveCaptcha.py
from ocr_utils import solve_captcha_image
import sys

if __name__ == "__main__":
    image_path = sys.argv[1]
    result = solve_captcha_image(image_path)
    print(result)
