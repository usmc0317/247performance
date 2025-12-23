"""
Optimize the large logo image for web performance
Run: python optimize_logo.py
"""

try:
    from PIL import Image
    import os
    
    # Paths
    original_logo = 'static/images/247sign_edited.png'
    optimized_logo = 'static/images/247sign_optimized.png'
    backup_original = 'static/images/247sign_edited_ORIGINAL.png'
    
    if not os.path.exists(original_logo):
        print(f"❌ Logo not found at: {original_logo}")
        exit(1)
    
    # Get original size
    original_size = os.path.getsize(original_logo) / 1024 / 1024  # MB
    print(f"📊 Original logo: {original_size:.2f} MB")
    
    # Backup original
    if not os.path.exists(backup_original):
        import shutil
        shutil.copy2(original_logo, backup_original)
        print(f"💾 Backup saved to: {backup_original}")
    
    print("🔧 Optimizing logo...")
    
    # Open and optimize
    img = Image.open(original_logo)
    
    # If it's a huge PNG, we might want to reduce dimensions slightly
    width, height = img.size
    print(f"   Original dimensions: {width}x{height}px")
    
    # Save optimized version with high quality
    img.save(optimized_logo, 'PNG', optimize=True, quality=85)
    
    optimized_size = os.path.getsize(optimized_logo) / 1024  # KB
    reduction = (1 - (optimized_size / 1024) / original_size) * 100
    
    print(f"\n✅ Optimization complete!")
    print(f"   Optimized logo: {optimized_size:.1f} KB")
    print(f"   Reduction: {reduction:.1f}%")
    
    if optimized_size < 500:
        print(f"\n🎉 Perfect! Logo is under 500KB")
        print(f"\n💡 Next step: Replace original with optimized version")
        print(f"   Command: Move-Item '{optimized_logo}' '{original_logo}' -Force")
    else:
        print(f"\n⚠️  Still large. Consider using TinyPNG.com for better compression")
        print(f"   Visit: https://tinypng.com/")
    
except ImportError:
    print("❌ PIL/Pillow not installed")
    print("   Install with: pip install Pillow")
except Exception as e:
    print(f"❌ Error: {e}")
