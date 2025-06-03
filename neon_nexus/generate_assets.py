from PIL import Image, ImageDraw

def create_player_image():
    # Create a 32x32 image with a red circle
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a red circle
    draw.ellipse([4, 4, 28, 28], fill=(255, 0, 0, 255))
    
    # Add some details
    draw.ellipse([12, 12, 20, 20], fill=(255, 255, 255, 255))  # White highlight
    
    img.save('neon_nexus/assets/player.png')

def create_grass_image():
    # Create a 32x32 image with grass texture
    img = Image.new('RGB', (32, 32), (34, 139, 34))  # Forest Green
    draw = ImageDraw.Draw(img)
    
    # Add some grass details
    for _ in range(20):
        x = random.randint(0, 31)
        y = random.randint(0, 31)
        length = random.randint(2, 6)
        draw.line([(x, y), (x, y - length)], fill=(0, 100, 0), width=1)
    
    img.save('neon_nexus/assets/grass.png')

def create_water_image():
    # Create a 32x32 image with water texture
    img = Image.new('RGB', (32, 32), (0, 105, 148))  # Deep Sky Blue
    draw = ImageDraw.Draw(img)
    
    # Add some wave details
    for _ in range(10):
        x = random.randint(0, 31)
        y = random.randint(0, 31)
        length = random.randint(4, 8)
        draw.line([(x, y), (x + length, y)], fill=(0, 80, 120), width=1)
    
    img.save('neon_nexus/assets/water.png')

if __name__ == '__main__':
    import random
    create_player_image()
    create_grass_image()
    create_water_image()
    print("Assets generated successfully!") 