from PIL import Image

def make_transparent(input_path, output_path):
    # Open the image with black background
    img = Image.open(input_path)
    img = img.convert("RGBA")
    
    datas = img.getdata()
    
    new_data = []
    for item in datas:
        # Check if the pixel is black or very close to black
        # (r, g, b, a)
        # Tweak threshold to cleanly remove background without affecting the translucent sheet
        r, g, b, a = item
        if r < 12 and g < 12 and b < 12:
            # Make it fully transparent
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Saved transparent PNG to {output_path}")

if __name__ == "__main__":
    input_file = "/Users/MummyDaddy/.gemini/antigravity/brain/32000fcd-04bf-4dbe-8064-d5ff18b58d02/bento_share_sheet_black_border_1780770107775.png"
    output_file = "/Users/MummyDaddy/My Projects/Code Projects/Pouch3 Website/public/images/bento-share-sheet.png"
    make_transparent(input_file, output_file)
