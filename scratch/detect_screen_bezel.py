from PIL import Image

def find_inner_screen(img_path):
    img = Image.open(img_path)
    width, height = img.size
    
    # We know the phone spans x = 32 to 3038 and y = 91 to 2671.
    # Let's inspect a horizontal slice across the middle of the phone, e.g. at y = height // 2
    # The bezel is dark/black, and the screen should start with some non-bezel colors.
    # Let's scan along y = 1359 (height // 2) from x = 32 to 3038, and print color transitions.
    y_mid = height // 2
    row_pixels = [img.getpixel((x, y_mid)) for x in range(width)]
    
    # Let's print the colors around the edges to find where it transitions from bezel to screen.
    # We can also scan the image vertically along x = width // 2 (or a column inside the screen area).
    # Let's find the bounding box of the inner screen.
    # The screen has a notch/Dynamic Island, and rounded corners.
    # Let's look for the first row below the notch/status bar that contains screen background, and the bottom home bar area.
    # Let's print out pixel values at y_mid to locate the left and right inner screen boundaries.
    
    print("Scanning row y_mid =", y_mid)
    # Bezel is black, let's look for where the screen content begins.
    # The screen content is a detail card which has a background of dark grey or a recipe image.
    # Let's scan from left to right:
    left_bezel_end = None
    right_bezel_start = None
    
    for x in range(32, width):
        p = img.getpixel((x, y_mid))
        # Let's print if there's any change
        # A simple heuristic: the bezel is very dark. Let's find where the luminance changes significantly.
        lum = 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]
        if left_bezel_end is None and lum > 20: # transition from bezel to screen
            left_bezel_end = x
        if left_bezel_end is not None and right_bezel_start is None and x > width // 2:
            # Look for transition from screen back to bezel
            # Let's scan backwards from 3038
            break
            
    for x in range(3038, width // 2, -1):
        p = img.getpixel((x, y_mid))
        lum = 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]
        if right_bezel_start is None and lum > 20:
            right_bezel_start = x
            break
            
    print(f"Inner Screen Horizontal boundaries: x = {left_bezel_end} to {right_bezel_start} (width = {right_bezel_start - left_bezel_end + 1})")
    
    # Let's do the same for vertical boundaries along the screen center x_mid = (left_bezel_end + right_bezel_start) // 2
    if left_bezel_end and right_bezel_start:
        x_mid = (left_bezel_end + right_bezel_start) // 2
        top_bezel_end = None
        bottom_bezel_start = None
        
        # Scan from top (91) downwards
        for y in range(91, height):
            p = img.getpixel((x_mid, y))
            lum = 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]
            if top_bezel_end is None and lum > 20:
                top_bezel_end = y
                break
                
        # Scan from bottom (2671) upwards
        for y in range(2671, height // 2, -1):
            p = img.getpixel((x_mid, y))
            lum = 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]
            if bottom_bezel_start is None and lum > 20:
                bottom_bezel_start = y
                break
                
        print(f"Inner Screen Vertical boundaries: y = {top_bezel_end} to {bottom_bezel_start} (height = {bottom_bezel_start - top_bezel_end + 1})")

if __name__ == '__main__':
    find_inner_screen('public/images/device-detail-dark.png')
