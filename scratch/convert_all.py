import os
from pathlib import Path
from PIL import Image

SOURCE_DIR = Path("/Users/MummyDaddy/My Projects/Code Projects/Pouch3/Read Later Card Detail Examples for Web")
DEST_DIR = Path("/Users/MummyDaddy/My Projects/Code Projects/Pouch3 Website/public/images/card-screens")

# Ensure destination directory exists
DEST_DIR.mkdir(parents=True, exist_ok=True)

# Standardized width for @3x retina display in the mockup
TARGET_WIDTH = 1033

# Let's map the specific screenshots we identified to descriptive names
NAME_MAPPING = {
    "13.30.57": "living-room",
    "13.31.22": "eames-archive",
    "13.31.32": "hampstead-heath",
    "13.31.39": "lisbon-travel",
    "13.31.45": "sourdough-recipe",
    "13.31.56": "tate-modern",
    "13.32.40": "v-and-a-exhibition",
    "13.33.18": "athens-tavernas",
    "13.34.08": "manteca-pasta",
    "13.34.14": "bao-london",
    "13.35.49": "paris-hotels",
}

def convert_screenshots():
    files = list(SOURCE_DIR.glob("*.png"))
    print(f"Found {len(files)} PNG screenshots in source folder.")
    
    for f in files:
        # Extract timestamp from filename, e.g. "Simulator Screenshot - iPhone 17 Pro - 2026-06-06 at 13.31.22.png"
        name = f.name
        timestamp = None
        for key in NAME_MAPPING.keys():
            if key in name:
                timestamp = key
                break
                
        if timestamp:
            descriptive_name = f"card-detail-{NAME_MAPPING[timestamp]}"
        else:
            # Fallback to a timestamp-based name if not in our predefined list
            import re
            match = re.search(r"at (\d{2}\.\d{2}\.\d{2})", name)
            if match:
                descriptive_name = f"card-detail-{match.group(1).replace('.', '-')}"
            else:
                descriptive_name = f"card-detail-unknown-{f.stem[:10]}"
                
        webp_dest = DEST_DIR / f"{descriptive_name}.webp"
        png_dest = DEST_DIR / f"{descriptive_name}.png"
        
        with Image.open(f) as img:
            # Resize
            w, h = img.size
            scale = TARGET_WIDTH / w
            new_h = int(h * scale)
            resized_img = img.resize((TARGET_WIDTH, new_h), Image.LANCZOS)
            
            # Save as WebP
            resized_img.save(webp_dest, "WEBP", quality=90)
            
            # Also save as PNG in case needed as fallback, but keep it optimized
            resized_img.save(png_dest, "PNG", optimize=True)
            
            print(f"Processed: {f.name} -> {descriptive_name}.webp / .png ({TARGET_WIDTH}x{new_h})")

if __name__ == '__main__':
    convert_screenshots()
