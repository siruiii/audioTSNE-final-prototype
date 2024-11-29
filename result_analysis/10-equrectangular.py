import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.image as mpimg

def cylindrical_to_equirectangular(theta, z, z_min, z_max, coord_width, coord_height, image_width, image_height):

    # Ensure theta is within 0 to 2π
    theta = theta % (2 * np.pi)

    # Map theta to x-coordinate in cylindrical coordinate space
    x = (theta / (2 * np.pi)) * coord_width

    # Map z to pitch angle phi, which ranges from -π/2 to π/2
    phi = ((z - z_min) / (z_max - z_min)) * np.pi - (np.pi / 2)

    # Map phi to y-coordinate in cylindrical coordinate space
    y = (1 - (phi + (np.pi / 2)) / np.pi) * coord_height

    # Center coordinates in the larger image
    x = (x - coord_width / 2) + (image_width / 2)
    y = (y - coord_height / 2) + (image_height / 2)

    return int(x), int(y)

def main():
    # Configuration
    coord_width = 4096*0.99  
    coord_height = 2048*0.5  
    image_width = 4096  
    image_height = 2048 
    background_image_path = 'A1_Skybox.webp'  

    # Load and process the background image
    img = mpimg.imread(background_image_path)

    # Load Cartesian coordinates from JSON file
    try:
        with open('../console_log/4-A1-merge.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("The JSON file was not found.")
        return
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        return

    if not data:
        print("No data loaded from JSON file.")
        return

    z_values = []
    cylindrical_coords = []

    for entry in data:
        if 'point3d' not in entry:
            print(f"Missing 'point3d' in entry: {entry}")
            continue

        x, z, y = entry['point3d']
        # Convert Cartesian (x, z, y) to cylindrical (r, theta, z)
        theta = np.arctan2(y, x)
        r = np.sqrt(x**2 + y**2)
        
        cylindrical_coords.append((theta, z))
        z_values.append(z)

    if not z_values:
        print("No valid z values found in the data.")
        return

    z_min = min(z_values)
    z_max = max(z_values)

    # Extract x and y coordinates for plotting
    x_coords = []
    y_coords = []

    for theta, z in cylindrical_coords:
        pixel_x, pixel_y = cylindrical_to_equirectangular(theta, z, z_min, z_max, coord_width, coord_height, image_width, image_height)
        
        x_coords.append(pixel_x)
        y_coords.append(pixel_y)

    y_coords = [-1 * y+ image_height +80 for y in y_coords]
    
    plt.figure(figsize=(10, 5))
    plt.imshow(img, extent=[0, image_width, 0, image_height], aspect='auto')
    plt.scatter(x_coords, y_coords, c='white', s=5) 
    plt.xlim(0, image_width)
    plt.ylim(0, image_height)  
    #plt.grid(True)
    plt.xticks([])
    plt.yticks([])
    plt.show()

if __name__ == "__main__":
    main()