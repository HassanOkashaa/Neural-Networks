import tkinter as tk
import random
import math
import time

# Set up constants
CENTER_SIZE_GENE = [0, 1]  # 0 = SMALL, 1 = BIG

CENTER_RED_GENE = list(range(256))
CENTER_GREEN_GENE = list(range(256))
CENTER_BLUE_GENE = list(range(256))

PETAL_RED_GENE = list(range(256))
PETAL_GREEN_GENE = list(range(256))
PETAL_BLUE_GENE = list(range(256))

NUM_PETALS = list(range(8))  # Petals range from 0 to 7

GARDEN_SIZE = 8  # 8 flowers

class Flower:
    def __init__(self):
        self.center_size = random.choice(CENTER_SIZE_GENE)
        self.center_red = random.choice(CENTER_RED_GENE)
        self.center_green = random.choice(CENTER_GREEN_GENE)
        self.center_blue = random.choice(CENTER_BLUE_GENE)
        self.petal_red = random.choice(PETAL_RED_GENE)
        self.petal_green = random.choice(PETAL_GREEN_GENE)
        self.petal_blue = random.choice(PETAL_BLUE_GENE)
        self.num_petals = random.choice(NUM_PETALS)
        self.fitness = 0  # Initialize fitness to 0
        self.hover_start_time = None  # To track hover start time

garden = []
for _ in range(GARDEN_SIZE):
  flower = Flower()
  garden.append(flower)

# Function to convert RGB values to hex
def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

# Function to draw one flower
def draw_flower(canvas, x, y, flower, flower_index):
    # Set the center size based on the flower's DNA
    radius = 20 if flower.center_size == 0 else 40

    # Get the colors from the flower's DNA
    center_color = rgb_to_hex(flower.center_red, flower.center_green, flower.center_blue)
    petal_color = rgb_to_hex(flower.petal_red, flower.petal_green, flower.petal_blue)

    # Draw the stem (thin black rectangle)
    canvas.create_rectangle(x - 5, y + radius, x + 5, y + 100, fill="black")

    # Get the number of petals and calculate the angle between them
    num_petals = flower.num_petals
    if num_petals > 0:
        angle_step = 360 / num_petals

        # Draw the petals first
        for i in range(num_petals):
            angle = i * angle_step
            petal_radius = radius // 2  # Petals will have a smaller radius
            petal_x = x + radius * math.cos(math.radians(angle))
            petal_y = y + radius * math.sin(math.radians(angle))
            canvas.create_oval(petal_x - petal_radius, petal_y - petal_radius, 
                               petal_x + petal_radius, petal_y + petal_radius, 
                               fill=petal_color)

    # Now draw the flower center on top of the petals
    flower_center = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=center_color)

    # Create fitness text
    fitness_text = canvas.create_text(x, y + 120, text=f'Fitness: {flower.fitness}', tags=f"fitness_{flower_index}")

    # Bind hover event
    def on_hover(event):
        flower.hover_start_time = time.time()  # Record when hover starts
        check_hover_duration(flower, fitness_text)

    # Bind leave event to reset hover duration
    def on_leave(event):
        flower.hover_start_time = None  # Reset hover start time

    canvas.tag_bind(flower_center, '<Enter>', on_hover)
    canvas.tag_bind(flower_center, '<Leave>', on_leave)

# Function to check hover duration and update fitness
def check_hover_duration(flower, fitness_text):
    if flower.hover_start_time is not None:
        elapsed_time = time.time() - flower.hover_start_time  # Calculate elapsed time
        fitness_increment = int(elapsed_time // 2)  # Every 2 seconds increases fitness by 1

        if fitness_increment > flower.fitness:  # Only update if there's an increase
            flower.fitness = fitness_increment
            canvas.itemconfig(fitness_text, text=f'Fitness: {flower.fitness}')

        # Schedule the next check after 100 milliseconds
        canvas.after(100, check_hover_duration, flower, fitness_text)

# Function to draw the garden grid
def draw_garden(canvas, garden_size, canvas_width, canvas_height):

    # Calculate number of columns and rows for the grid
    cols = int(8)
    rows = int(1)

    # Calculate the spacing between flowers
    x_spacing = canvas_width // cols
    y_spacing = canvas_height // rows

    # Draw each flower in the grid
    for i in range(len(garden)):
        row = i // cols
        col = i % cols
        x = (col * x_spacing) + x_spacing // 2
        y = (row * y_spacing) + y_spacing // 2
        flower = Flower()
        draw_flower(canvas, x, y, garden[i], i)

# Function to handle the button click
def evolve_generation():
    print("Evolving new generation...")
    # Put your logic for evolving the flowers here
    # You can clear the canvas and redraw flowers or implement any logic you want

# Main method to run the Tkinter application
def main():
    # Set up tkinter window
    root = tk.Tk()
    root.title("Flower Garden")


    canvas_width = 600
    canvas_height = 600
    global canvas  # Make canvas global to access in other functions
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # Draw the garden with GARDEN_SIZE number of flowers
    draw_garden(canvas, GARDEN_SIZE, canvas_width, canvas_height)

    # Create "Evolve New Generation" button
    evolve_button = tk.Button(root, text="Evolve New Generation", command=evolve_generation)
    evolve_button.pack(pady=10)  # Add some padding for better spacing

    root.mainloop()

# Call the main method to run the program
if __name__ == "__main__":
    main()
