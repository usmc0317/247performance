"""
Remove whitespace/padding from logo image
"""
from PIL import Image

# Load the logo
img = Image.open('static/images/247sign_edited.png')

# Convert to RGBA to handle transparency
img = img.convert('RGBA')

# Get the bounding box of non-white pixels
# Create an alpha mask where white pixels are transparent
datas = img.getdata()
newData = []
for item in datas:
    # If pixel is white or very light (close to white), make it transparent
    if item[0] > 240 and item[1] > 240 and item[2] > 240:
        newData.append((255, 255, 255, 0))  # Transparent
    else:
        newData.append(item)

img.putdata(newData)

# Get bounding box of non-transparent content
bbox = img.getbbox()

if bbox:
    # Crop to content
    img_cropped = img.crop(bbox)
    
    # Save with transparency
    img_cropped.save('static/images/247sign_edited.png', 'PNG', optimize=True, quality=95)
    
    print(f"✅ Logo whitespace removed!")
    print(f"   Original size: {img.size}")
    print(f"   Cropped size: {img_cropped.size}")
    print(f"   Removed {img.size[0] - img_cropped.size[0]}px width, {img.size[1] - img_cropped.size[1]}px height")
else:
    print("No whitespace found to remove")
