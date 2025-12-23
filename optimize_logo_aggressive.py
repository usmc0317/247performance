"""
Aggressive logo optimization - resize and compress
Run: python optimize_logo_aggressive.py
"""

try:
    from PIL import Image
    import os
    
    # Paths
    original_logo = 'static/images/247sign_edited.png'
    optimized_logo = 'static/images/247sign_web.png'
    
    if not os.path.exists(original_logo):
        print(f"❌ Logo not found at: {original_logo}")
        exit(1)
    
    # Get original size
    original_size_mb = os.path.getsize(original_logo) / 1024 / 1024
    print(f"📊 Original: {original_size_mb:.2f} MB")
    
    print("🔧 Optimizing (resize + compress)...")
    
    # Open image
    img = Image.open(original_logo)
    original_width, original_height = img.size
    print(f"   Original: {original_width}x{original_height}px")
    
    # Resize to reasonable web size (max 1200px on longest side)
    max_dimension = 1200
    if max(original_width, original_height) > max_dimension:
        if original_width > original_height:
            new_width = max_dimension
            new_height = int(original_height * (max_dimension / original_width))
        else:
            new_height = max_dimension
            new_width = int(original_width * (max_dimension / original_height))
        
        img = img.resize((new_width, new_height), Image.LANCZOS)
        print(f"   Resized: {new_width}x{new_height}px")
    
    # Convert to RGB if RGBA (smaller file size)
    if img.mode == 'RGBA':
        # Create white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
        img = background
        print(f"   Converted RGBA to RGB")
    
    # Save with optimization
    img.save(optimized_logo, 'PNG', optimize=True, quality=85)
    
    optimized_size_kb = os.path.getsize(optimized_logo) / 1024
    reduction = (1 - (optimized_size_kb / 1024) / original_size_mb) * 100
    
    print(f"\n✅ Optimization complete!")
    print(f"   Output: {optimized_logo}")
    print(f"   Size: {optimized_size_kb:.1f} KB")
    print(f"   Reduction: {reduction:.1f}%")
    
    if optimized_size_kb < 500:
        print(f"\n🎉 Perfect! Under 500KB - ready for production!")
        print(f"\n📝 Next steps:")
        print(f"   1. Review the optimized image: {optimized_logo}")
        print(f"   2. If quality looks good, replace original:")
        print(f"      Move-Item '{optimized_logo}' 'static/images/247sign_edited.png' -Force")
    elif optimized_size_kb < 1000:
        print(f"\n✅ Good! Under 1MB - acceptable for web")
        print(f"\n💡 Optional: Use TinyPNG for even more compression")
    else:
        print(f"\n⚠️  Still over 1MB. Recommended: Use TinyPNG.com")
        print(f"   Visit: https://tinypng.com/")
    
except ImportError:
    print("❌ PIL/Pillow not installed")
    print("   Install with: pip install Pillow")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
