import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
import joblib

# Load the models
loaded_rfr_pipeline = joblib.load('random_forest_regressor11.joblib')
loaded_dtr_pipeline = joblib.load('decision_tree_regressor11.joblib')

# Load the data
data = pd.read_csv("C:/Users/Jaydeep/OneDrive/Desktop/Final Crop project/crop_production.csv")
data['Year'] = data['Year'].apply(lambda x: int(x.split('-')[0]))
data_cleaned = data.dropna()

# Helper functions to get unique values
def get_unique_values(column, filter_col=None, filter_val=None):
    if filter_col and filter_val:
        filtered_data = data_cleaned[data_cleaned[filter_col] == filter_val]
    else:
        filtered_data = data_cleaned
    return sorted(filtered_data[column].unique())

# Create the main application window
root = tk.Tk()
root.title("Crop Production Predictor")

# Set full-screen mode
root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen", True))  # Enable full-screen with F11
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))  # Exit full-screen with Escape
root.bind("q", lambda event: root.destroy())  # Close application with 'Q'

# Load and set background image
bg_image_path = "C:/Users/Jaydeep/OneDrive/Desktop/Final Crop project/peakpx.jpg"  # Replace with your image path
bg_image = Image.open(bg_image_path)

# Resize the image to fit the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)  # Use LANCZOS for high-quality resizing
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

def update_districts(*args):
    state = state_var.get()
    if state:
        districts = get_unique_values('District', 'State', state)
        district_combobox['values'] = districts
        district_combobox.set('')
        season_combobox['values'] = []
        crop_combobox['values'] = []

def update_seasons(*args):
    state = state_var.get()
    district = district_var.get()
    if state and district:
        seasons = get_unique_values('Season', 'District', district)
        season_combobox['values'] = seasons
        season_combobox.set('')
        crop_combobox['values'] = []

def update_crops(*args):
    state = state_var.get()
    district = district_var.get()
    season = season_var.get()
    if state and district and season:
        crops = get_unique_values('Crop', 'Season', season)
        crop_combobox['values'] = crops
        crop_combobox.set('')

def get_production():
    state = state_var.get()
    district = district_var.get()
    season = season_var.get()
    crop = crop_var.get()
    area = area_entry.get()
    
    if not state or not district or not season or not crop or not area:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return
    
    try:
        area = float(area)
    except ValueError:
        messagebox.showerror("Input Error", "Area should be a number.")
        return

    year = 2025  # fixed year

    # Prepare the input data for prediction
    input_data = pd.DataFrame([[state, district, crop, season, area, year]],
                              columns=['State', 'District', 'Crop', 'Season', 'Area', 'Year'])

    # Predict using Random Forest and Decision Tree
    rfr_prediction = loaded_rfr_pipeline.predict(input_data)[0]
    dtr_prediction = loaded_dtr_pipeline.predict(input_data)[0]
    
    rfr_output_var.set(f"{rfr_prediction:.2f} Tons")
    dtr_output_var.set(f"{dtr_prediction:.2f} Tons")

# Create a frame for the header
header_frame = tk.Frame(root, bg="#004d00")
header_frame.pack(fill=tk.X, pady=(30, 10))  # Increased top padding to 30

header_label = tk.Label(header_frame, text="Crop Production Predictor", bg="#004d00", fg="white", font=("Algerian", 24, "bold"))
header_label.pack(pady=10, padx=10, fill=tk.X)  # Center the label and fill the width

# Create a frame for inputs and center it on the screen
frame_width = 600  # Set the width for both frames
input_frame = tk.Frame(root, bg="#B8860B", width=frame_width)  # Lime color
input_frame.pack(pady=(20, 10), padx=10, anchor='center')  # Center the input_frame

# State selection
tk.Label(input_frame, text="Select State", bg="#B8860B", font=("Algerian", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
state_var = tk.StringVar()
state_combobox = ttk.Combobox(input_frame, textvariable=state_var, font=("Algerian", 12))
state_combobox['values'] = get_unique_values('State')
state_combobox.grid(row=0, column=1, padx=10, pady=10)
state_combobox.bind("<<ComboboxSelected>>", update_districts)

# District selection
tk.Label(input_frame, text="Select District", bg="#B8860B", font=("Algerian", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
district_var = tk.StringVar()
district_combobox = ttk.Combobox(input_frame, textvariable=district_var, font=("Algerian", 12))
district_combobox.grid(row=1, column=1, padx=10, pady=10)
district_combobox.bind("<<ComboboxSelected>>", update_seasons)

# Season selection
tk.Label(input_frame, text="Select Season", bg="#B8860B", font=("Algerian", 14)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
season_var = tk.StringVar()
season_combobox = ttk.Combobox(input_frame, textvariable=season_var, font=("Algerian", 12))
season_combobox.grid(row=2, column=1, padx=10, pady=10)
season_combobox.bind("<<ComboboxSelected>>", update_crops)

# Crop selection
tk.Label(input_frame, text="Select Crop", bg="#B8860B", font=("Algerian", 14)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
crop_var = tk.StringVar()
crop_combobox = ttk.Combobox(input_frame, textvariable=crop_var, font=("Algerian", 12))
crop_combobox.grid(row=3, column=1, padx=10, pady=10)

# Area input
tk.Label(input_frame, text="Enter Area", bg="#B8860B", font=("Algerian", 14)).grid(row=4, column=0, padx=10, pady=10, sticky="w")
area_entry = tk.Entry(input_frame, font=("Algerian", 12))
area_entry.grid(row=4, column=1, padx=10, pady=10)

# Place buttons individually and center them
calculate_button = tk.Button(text="Get Production", command=get_production, font=("Algerian", 14), bg="#8B0000", fg="white", width=20, height=2)
calculate_button.pack(pady=10)

# Output text boxes frame
output_frame = tk.Frame(root, bg="#B8860B", width=frame_width)  # Lime color
output_frame.pack(pady=10, padx=10, anchor='center')  # Center the output_frame

tk.Label(output_frame, text="Random Forest Output:", bg="#B8860B", font=("Algerian", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
rfr_output_var = tk.StringVar()
rfr_output_box = tk.Entry(output_frame, textvariable=rfr_output_var, font=("Algerian", 12), state="readonly")
rfr_output_box.grid(row=0, column=1, padx=10, pady=10)

tk.Label(output_frame, text="Decision Tree Output:", bg="#B8860B", font=("Algerian", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
dtr_output_var = tk.StringVar()
dtr_output_box = tk.Entry(output_frame, textvariable=dtr_output_var, font=("Algerian", 12), state="readonly")
dtr_output_box.grid(row=1, column=1, padx=10, pady=10)

# Run the application
root.mainloop()
