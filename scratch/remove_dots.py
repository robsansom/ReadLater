from PIL import Image, ImageDraw

def remove_dots(img_path, output_path):
    img = Image.open(img_path)
    width, height = img.size
    print(f"Loaded image: {width}x{height}")
    
    # We want to create a mask for the phone bezel.
    # The inner screen is x = 1020 to 2052.
    # The outer bezel of the phone is slightly wider, let's say it starts around x = 950 and ends around x = 2122.
    # Vertically, the inner screen is y = 263 to 2454.
    # The outer bezel starts around y = 190 and ends around y = 2520.
    # Let's create a solid black image of the same size.
    black_img = Image.new("RGB", (width, height), (0, 0, 0))
    
    # We will copy a slice of the original image (the phone bezel) onto the black image.
    # Specifically, the region x = 940 to 2132, and y = 180 to 2530.
    # To keep it looking natural and avoid a harsh vertical cut, we can use a rounded rectangle mask for the phone.
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    # Draw a rounded rectangle for the phone bezel + shadow
    # Let's make it slightly larger than the bezel: x from 920 to 2152, y from 160 to 2550
    # Corner radius ~120px (standard for iPhone mockups at @3x)
    draw.rounded_rectangle(
        [(920, 160), (2152, 2550)],
        radius=140,
        fill=255
    )
    
    # Composite the original image over the black image using the mask
    final_img = Image.composite(img, black_img, mask)
    
    # Save the output
    final_img.save(output_path, "PNG")
    print(f"Saved optimized image without dots to {output_path}")

if __name__ == '__main__':
    # First, let's back up the original image
    import shutil
    import os
    if not os.path.exists('public/images/device-detail-dark-backup.png'):
        shutil.copyfile('public/images/device-detail-dark.png', 'public/images/device-detail-dark-backup.png')
        print("Created backup of device-detail-dark.png")
        
    remove_dots('public/images/device-detail-dark-backup.png', 'public/images/device-detail-dark.png')
    
    # Also regenerate the webp version of the device mockup
    from PIL import Image
    img = Image.open('public/images/device-detail-dark.png')
    img.save('public/images/device-detail-dark.webp', "WEBP", quality=92, method=6)
    print("Regenerated device-detail-dark.webp")
