import sys
from PIL import Image

def detect_screen(img_path):
    img = Image.open(img_path)
    width, height = img.size
    print(f"Image dimensions: {width}x{height}")
    
    # We want to find the screen area in device-detail-dark.png
    # The image is a phone mockup. The screen has dynamic content (a recipe detail screen)
    # let's analyze column by column and row by row to find where the screen starts.
    # Usually, the screen will be centered or aligned to some side. Let's dump some row/column profiles.
    # Specifically, the screen is dark-ish, and the page background is pure black (0,0,0) in device-detail-dark.png.
    # The phone bezel is a dark grey or silver. The notch/Dynamic Island is pure black too.
    # Let's find columns where there are non-black pixels, which will tell us the phone's horizontal span.
    
    non_black_cols = []
    for x in range(width):
        col_has_color = False
        for y in range(height):
            p = img.getpixel((x, y))
            # Check if pixel is not black (allow small threshold for compression noise)
            if sum(p[:3]) > 15:
                col_has_color = True
                break
        if col_has_color:
            non_black_cols.append(x)
            
    if not non_black_cols:
        print("No non-black columns found!")
        return
        
    x_min, x_max = min(non_black_cols), max(non_black_cols)
    print(f"Phone horizontal span: x = {x_min} to {x_max} (width = {x_max - x_min + 1})")
    
    # Now let's find the vertical span of the phone
    non_black_rows = []
    for y in range(height):
        row_has_color = False
        for x in range(width):
            p = img.getpixel((x, y))
            if sum(p[:3]) > 15:
                row_has_color = True
                break
        if row_has_color:
            non_black_rows.append(y)
            
    y_min, y_max = min(non_black_rows), max(non_black_rows)
    print(f"Phone vertical span: y = {y_min} to {y_max} (height = {y_max - y_min + 1})")

if __name__ == '__main__':
    detect_screen('public/images/device-detail-dark.png')
