from PIL import Image

def remove_background(input_path, output_path):
    try:
        img = Image.open(input_path).convert("RGBA")
        datas = img.getdata()
        newData = []
        
        # We assume background is white or light checkerboard (very common for fake PNGs)
        for item in datas:
            # If the pixel is very light (R>220, G>220, B>220), make it transparent
            if item[0] > 220 and item[1] > 220 and item[2] > 220:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
                
        img.putdata(newData)
        img.save(output_path, "PNG")
        print("Background removed successfully.")
    except Exception as e:
        print(f"Error: {e}")

remove_background("public/ambient/reaper.png", "public/ambient/reaper_transparent.png")