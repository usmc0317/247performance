"""
Quick script to create favicon from existing logo
Run: python create_favicon.py
"""

try:
    from PIL import Image
    import os
    
    # Paths
    logo_path = 'static/images/247sign_edited.png'
    favicon_path = 'static/images/favicon.png'
    
    if not os.path.exists(logo_path):
        print(f"❌ Logo not found at: {logo_path}")
        print("   Please ensure the logo file exists.")
        exit(1)
    
    print("🎨 Creating favicon from logo...")
    
    # Open and process logo
    img = Image.open(logo_path)
    
    # Convert to RGBA if needed
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Create square crop from center
    width, height = img.size
    size = min(width, height)
    left = (width - size) / 2
    top = (height - size) / 2
    right = (width + size) / 2
    bottom = (height + size) / 2
    
    img_cropped = img.crop((left, top, right, bottom))
    
    # Resize to 512x512 (good quality for all uses)
    img_favicon = img_cropped.resize((512, 512), Image.LANCZOS)
    
    # Save as favicon
    img_favicon.save(favicon_path, 'PNG', optimize=True)
    
    file_size = os.path.getsize(favicon_path) / 1024  # KB
    
    print(f"✅ Favicon created successfully!")
    print(f"   Location: {favicon_path}")
    print(f"   Size: {file_size:.1f} KB")
    print(f"   Dimensions: 512x512px")
    print("\n💡 Tip: Test by refreshing http://127.0.0.1:8000/ and checking browser tab")
    
except ImportError:
    print("❌ PIL/Pillow not installed")
    print("   Install with: pip install Pillow")
    print("\n   Or use online tool: https://realfavicongenerator.net/")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n   Alternative: Use online tool at https://realfavicongenerator.net/")
