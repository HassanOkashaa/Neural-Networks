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
MUT_RATE = 0.05
GENERATION_NUMBER = 0

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

    def get_dna(self):
        return {
            'center_size': self.center_size,
            'center_color': (self.center_red, self.center_green, self.center_blue),
            'petal_color': (self.petal_red, self.petal_green, self.petal_blue),
            'num_petals': self.num_petals,
        }


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
    canvas.create_rectangle(x - 3, y + radius, x + 3, y + 100, fill="black")

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
    # Use two rows
    rows = 1
    cols = 8  # Calculate columns based on number of flowers

    # Calculate the spacing between flowers
    x_spacing = canvas_width // cols
    y_spacing = canvas_height // rows
    fitness_text = canvas.create_text(600, 20, text=f'Generation Number: {GENERATION_NUMBER}')
    # Draw each flower in the grid
    for i in range(len(garden)):
        row = i // cols
        col = i % cols
        x = (col * x_spacing) + x_spacing // 2
        y = (row * y_spacing) + y_spacing // 2
        draw_flower(canvas, x, y, garden[i], i)

# Function to handle the button click
# Function to handle the button click
def evolve_generation():
    global garden  # Make garden global to modify it
    global GENERATION_NUMBER
    print("Evolving new generation...")
    GENERATION_NUMBER += 1
    # Selection
    sorted_garden = sorted(garden, key=lambda flower: flower.fitness, reverse=True)
    half_size = len(sorted_garden) // 2
    selected_for_crossover = sorted_garden[:half_size]
    new_generation = selected_for_crossover.copy()

    print(f"Top {half_size} flowers selected for crossover (based on fitness):")
    for i, flower in enumerate(selected_for_crossover):
        print(f"Flower {i + 1}: DNA: {flower.get_dna()}, Fitness: {flower.fitness}")

    #mutation
    while len(new_generation) < GARDEN_SIZE:
        parent1, parent2 = random.sample(selected_for_crossover, 2)

        child = crossover(parent1, parent2)

        if random.random() < MUT_RATE:  #0-1   0.05 5%
            child.center_red = random.choice(CENTER_RED_GENE)

        new_generation.append(child)

    # Reset fitness of all flowers in the new generation
    for flower in new_generation:
        flower.fitness = 0

    # Update garden with the new generation
    garden = new_generation

    # Redraw the canvas with the new generation
    canvas.delete("all")
    draw_garden(canvas, GARDEN_SIZE, 1200, 300)
    
    for i, flower in enumerate(new_generation):
        print(f"Flower {i + 1}: DNA: {flower.get_dna()}, Fitness: {flower.fitness}")

# Crossover
def crossover(parent1, parent2):
    child = Flower()
    child.center_size = random.choice([parent1.center_size, parent2.center_size])
    child.center_red = random.choice([parent1.center_red, parent2.center_red])
    child.center_green = random.choice([parent1.center_green, parent2.center_green])
    child.center_blue = random.choice([parent1.center_blue, parent2.center_blue])

    child.petal_red = random.choice([parent1.petal_red, parent2.petal_red])
    child.petal_green = random.choice([parent1.petal_green, parent2.petal_green])
    child.petal_blue = random.choice([parent1.petal_blue, parent2.petal_blue])

    child.num_petals = random.choice([parent1.num_petals, parent2.num_petals])

    return child


# Main method to run the Tkinter application
def main():
    # Set up tkinter window
    root = tk.Tk()
    root.title("Flower Garden")

    canvas_width = 1200
    canvas_height = 300
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
