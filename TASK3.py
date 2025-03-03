import pandas as pd
import os
from tkinter import *
from PIL import Image, ImageTk

# Load the recipe dataset
recipes_df = pd.read_csv('recipes.csv')

def find_recipes(available_ingredients):
    recipe_suggestions = []

    for index, row in recipes_df.iterrows():
        recipe_ingredients = set(row['Ingredients'].split(', '))
        common_ingredients = recipe_ingredients.intersection(available_ingredients)
        missing_ingredients = recipe_ingredients.difference(available_ingredients)
        
        if common_ingredients:
            recipe_suggestions.append({
                'Recipe': row['Recipe'],
                'Common Ingredients': common_ingredients,
                'Missing Ingredients': missing_ingredients
            })

    return recipe_suggestions

def display_recipes(recipe_suggestions):
    if recipe_suggestions:
        for widget in result_frame.winfo_children():
            widget.destroy()
        
        Label(result_frame, text="Here are some recipes you can make (even if some ingredients are missing):", font=("Helvetica", 14)).pack()

        for idx, recipe in enumerate(recipe_suggestions, start=1):
            frame = Frame(result_frame)
            frame.pack(pady=10)

            img_path = f"images/{recipe['Recipe']}.jpg"
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((100, 100), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                img_label = Label(frame, image=img)
                img_label.image = img
                img_label.pack(side=LEFT, padx=10)
            
            text_frame = Frame(frame)
            text_frame.pack(side=LEFT)
            
            Label(text_frame, text=f"{idx}. {recipe['Recipe']}", font=("Helvetica", 12, "bold")).pack(anchor='w')
            Label(text_frame, text=f"Common Ingredients: {', '.join(recipe['Common Ingredients'])}").pack(anchor='w')
            Label(text_frame, text=f"Missing Ingredients: {', '.join(recipe['Missing Ingredients'])}").pack(anchor='w')
    else:
        for widget in result_frame.winfo_children():
            widget.destroy()
        Label(result_frame, text="No recipes found with the given ingredients.", font=("Helvetica", 14)).pack()

def search_recipes():
    available_ingredients_input = ingredients_entry.get()
    available_ingredients = set([ingredient.strip() for ingredient in available_ingredients_input.split(',')])
    
    recipe_suggestions = find_recipes(available_ingredients)
    display_recipes(recipe_suggestions)

# Create the main window
root = Tk()
root.title("Recipe Recommendation Bot")

# Create and place widgets
Label(root, text="Enter your available ingredients, separated by commas:", font=("Helvetica", 14)).pack(pady=10)
ingredients_entry = Entry(root, width=50, font=("Helvetica", 14))
ingredients_entry.pack(pady=5)
Button(root, text="Find Recipes", command=search_recipes, font=("Helvetica", 14)).pack(pady=10)

# Create a frame to display results
result_frame = Frame(root)
result_frame.pack(pady=10)

# Start the main loop
root.mainloop()
