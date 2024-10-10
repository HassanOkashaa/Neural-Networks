import tkinter as tk
import random
import math
import time

#constants
CENTER_SIZE_GENE = [0, 1]  

CENTER_RED_GENE = list(range(256))
CENTER_GREEN_GENE = list(range(256))
CENTER_BLUE_GENE = list(range(256))

PETAL_RED_GENE = list(range(256))
PETAL_GREEN_GENE = list(range(256))
PETAL_BLUE_GENE = list(range(256))

NUM_PETALS = list(range(8))

GARDEN_SIZE = 8  

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
        self.fitness = 0 
        self.hover_start_time = None 

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

def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


def draw_flower(canvas, x, y, flower, flower_index):
    # center size
    radius = 20 if flower.center_size == 0 else 40

    # center color
    center_color = rgb_to_hex(flower.center_red, flower.center_green, flower.center_blue)
    petal_color = rgb_to_hex(flower.petal_red, flower.petal_green, flower.petal_blue)

    # stem
    canvas.create_rectangle(x - 3, y + radius, x + 3, y + 100, fill="black")

    # petals
    num_petals = flower.num_petals
    if num_petals > 0:
        angle_step = 360 / num_petals

        # Draw petals
        for i in range(num_petals):
            angle = i * angle_step
            petal_radius = radius // 2
            petal_x = x + radius * math.cos(math.radians(angle))
            petal_y = y + radius * math.sin(math.radians(angle))
            canvas.create_oval(petal_x - petal_radius, petal_y - petal_radius, 
                               petal_x + petal_radius, petal_y + petal_radius, 
                               fill=petal_color)

    #center
    flower_center = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=center_color)

    # fitness
    fitness_text = canvas.create_text(x, y + 120, text=f'Fitness: {flower.fitness}', tags=f"fitness_{flower_index}")


    #Hover functions
    def on_hover(event):
        flower.hover_start_time = time.time()
        check_hover_duration(flower, fitness_text)
    def on_leave(event):
        flower.hover_start_time = None

    canvas.tag_bind(flower_center, '<Enter>', on_hover)
    canvas.tag_bind(flower_center, '<Leave>', on_leave)

def check_hover_duration(flower, fitness_text):
    if flower.hover_start_time is not None:
        elapsed_time = time.time() - flower.hover_start_time
        fitness_increment = int(elapsed_time // 1)  #1 sec
        if fitness_increment > flower.fitness:
            flower.fitness = fitness_increment
            canvas.itemconfig(fitness_text, text=f'Fitness: {flower.fitness}')

        #check elapsed time again
        canvas.after(100, check_hover_duration, flower, fitness_text)


def draw_garden(canvas, canvas_width, canvas_height):
    rows = 1
    cols = 8

    #spacing between flowers
    x_spacing = canvas_width // cols
    y_spacing = canvas_height // rows
    fitness_text = canvas.create_text(600, 20, text=f'Generation Number: {GENERATION_NUMBER}')

    # Draw flowers
    for i in range(len(garden)):
        row = i // cols
        col = i % cols
        x = (col * x_spacing) + x_spacing // 2
        y = (row * y_spacing) + y_spacing // 2
        draw_flower(canvas, x, y, garden[i], i)

def selection():
    sorted_garden = sorted(garden, key=lambda flower: flower.fitness, reverse=True)
    half_size = len(sorted_garden) // 2
    selected_for_crossover = sorted_garden[:half_size]
    new_generation = selected_for_crossover.copy()

    print(f"Top {half_size} flowers selected for crossover (based on fitness):")
    for i, flower in enumerate(selected_for_crossover):
        print(f"Flower {i + 1}: DNA: {flower.get_dna()}, Fitness: {flower.fitness}")
    return new_generation

# Crossover
def crossover(parent1, parent2):
    child1 = Flower()
    child2 = Flower()

    child1.center_size = parent1.center_size
    child1.center_red = parent1.center_red
    child1.center_green = parent1.center_green
    child1.center_blue = parent1.center_blue

    child1.petal_red = parent2.petal_red
    child1.petal_green = parent2.petal_green
    child1.petal_blue =  parent2.petal_blue
    child1.num_petals = parent2.num_petals



    child2.center_size =  parent2.center_size
    child2.center_red = parent2.center_red
    child2.center_green = parent2.center_green
    child2.center_blue = parent2.center_blue

    child2.petal_red = parent1.petal_red
    child2.petal_green = parent1.petal_green
    child2.petal_blue = parent1.petal_blue
    child2.num_petals = parent1.num_petals

    return child1, child2


def crossoverHelper(selected_for_crossover):
    new_generation = selected_for_crossover.copy() 
    for i in range(0, len(new_generation) - 1, 2):

        parent1, parent2 = selected_for_crossover[i], selected_for_crossover[i+1]
        child1, child2 = crossover(parent1, parent2)

        new_generation.append(child1)
        new_generation.append(child2)
    return new_generation

def mutation(new_generation):
    flowerChoice1 = random.randint(0,7)
    flowerChoice2 = random.randint(0,7)
    flowerChoice3 = random.randint(0,7)
    flowers_arr= [flowerChoice1,flowerChoice2,flowerChoice3]
    #random bit in every selected flower
    f1bit = random.randint(1,8)
    f2bit = random.randint(1,8)
    f3bit = random.randint(1,8)
    bits_arr=[f1bit,f2bit,f3bit]
    for i in range(3):
        if bits_arr[i] == 1:
            new_value = random.choice([0, 1])
            new_generation[flowers_arr[i]].center_size = new_value
            print(f"Flower {flowers_arr[i] + 1}: center_size set to {new_value}")
            
        if bits_arr[i] == 2:
            new_value = random.randint(0, 255)
            new_generation[flowers_arr[i]].center_red = new_value
            print(f"Flower {flowers_arr[i] + 1}: center_red set to {new_value}")
            
        if bits_arr[i] == 3:
            new_value = random.randint(0, 255)
            new_generation[flowers_arr[i]].center_green = new_value
            print(f"Flower {flowers_arr[i] + 1}: center_green set to {new_value}")
            
        if bits_arr[i] == 4:
            new_value = random.randint(0, 255)
            new_generation[flowers_arr[i]].center_blue = new_value
            print(f"Flower {flowers_arr[i] + 1}: center_blue set to {new_value}")
            
        if bits_arr[i] == 5:
            new_value = random.randint(0, 255)
            new_generation[flowers_arr[i]].petal_red = new_value
            print(f"Flower {flowers_arr[i] + 1}: petal_red set to {new_value}")
            
        if bits_arr[i] == 6:
            new_value = random.randint(0, 255)
            new_generation[flowers_arr[i]].petal_green = new_value
            print(f"Flower {flowers_arr[i] + 1}: petal_green set to {new_value}")
            
        if bits_arr[i] == 7:
            new_value = random.randint(0, 255)
            new_generation[flowers_arr[i]].petal_blue = new_value
            print(f"Flower {flowers_arr[i] + 1}: petal_blue set to {new_value}")
            
        if bits_arr[i] == 8:
            new_value = random.randint(0, 7)
            new_generation[flowers_arr[i]].num_petals = new_value
            print(f"Flower {flowers_arr[i] + 1}: num_petals set to {new_value}")
    return new_generation

def evolve_generation():
    global garden
    global GENERATION_NUMBER
    print("Evolving new generation...")
    GENERATION_NUMBER += 1

    # Selection
    selected_for_crossover = selection()

    #crossover
    new_generation = crossoverHelper(selected_for_crossover)

    new_generation_with_mutation = mutation(new_generation)

    # Reset fitness for next generation
    for flower in new_generation_with_mutation:
        flower.fitness = 0

    # Update garden
    garden = new_generation_with_mutation

    # Redraw canvas
    canvas.delete("all")
    draw_garden(canvas, 1200, 300)
    
    for i, flower in enumerate(new_generation_with_mutation):
        print(f"Flower {i + 1}: DNA: {flower.get_dna()}, Fitness: {flower.fitness}")


def main():
    #window
    root = tk.Tk()
    root.title("Flower Garden")

    #canvas size
    canvas_width = 1200
    canvas_height = 300
    global canvas
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    draw_garden(canvas, canvas_width, canvas_height)

    evolve_button = tk.Button(root, text="Evolve New Generation", command=evolve_generation)
    evolve_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
