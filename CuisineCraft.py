import tkinter as tk
import sqlite3
import random
import pandas as pd
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog



################################################################################
# Functions
################################################################################

# function to clear all entries used with button on root window
def clear_entries():
    recept_entry.delete(0, tk.END)
    bereidingstijd_entry.delete(0, tk.END)
    keuken_origine_entry.delete(0, tk.END)
    locatie_bestand_entry.delete(0, tk.END)
    url_entry.delete(0, tk.END)
    gezondheidsgraad_entry.delete(0, tk.END)
    aantal_personen_entry.delete(0, tk.END)

    # delete all entry's
    for i in range(1,15):
        name_entry = "ingredient_entry_" + str(i)
        eval(name_entry + ".delete(0, tk.END)")

# Add data to maaltijden form maaltijden tab.
def insert_data():
    """
    Function collects and insert the data to the database.
    """
    db_weekmenu = "CuisineCraft.db"

    try:
        conn = sqlite3.connect(db_weekmenu)
        c = conn.cursor()

    except Exception as e:
        messagebox.showinfo(message="Was not able to connect to the database !")

    # Get all variables with the get() method
    recept = recept_entry.get()
    aantal_personen = aantal_personen_entry.get()
    bereidingstijd = bereidingstijd_entry.get()
    keuken_origine = keuken_origine_entry.get()
    locatie_bestand = locatie_bestand_entry.get()
    url = url_entry.get()
    gezondheidsgraad = gezondheidsgraad_entry.get()

    # Add data to DB table maaltijden.
    try:
        c.execute("INSERT INTO maaltijden (recept_naam, aantal_personen, bereidingstijd, keuken_origine, locatie_bestand, url, gezondheidsgraad) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (recept, aantal_personen, bereidingstijd, keuken_origine, locatie_bestand, url, gezondheidsgraad))
    except Exception as e:
        messagebox.showinfo(message=str(e))

    conn.commit()
    conn.close()
    messagebox.showinfo("Success", message="Data added successfully!")

# add data to table ingredienten
def insert_data_ingredienten():
    """
    Inserts data into the 'Ingredienten' table in the 'CuisineCraft.db' SQLite database.

    The function connects to the database, fetches the ID of the latest 'maaltijden' entry,
    retrieves ingredient data from tkinter entry fields, and inserts the data into the 'Ingredienten' table.

    Raises:
        Exception: If there is an error connecting to the database.
        messagebox.showerror: If the last ID from 'maaltijden' cannot be fetched.

    Returns:
        None. The data is added to the table and a success message is displayed.
    """
    try:
        conn = sqlite3.connect("CuisineCraft.db")
        c = conn.cursor()

    except Exception as e:
        messagebox.showinfo(message="Was not able to connect to the database !")

    # Fetch the ID of maaltijden and link it to all the ingredients items
    c.execute('SELECT ID FROM maaltijden ORDER BY rowid DESC LIMIT 1')

    # Fetch the ID from maaltijden db
    try:
        id_maaltijden = c.fetchone()[0]
    except:
        messagebox.showerror(message="Not able to fetch last ID from maaltijden.")
        conn.close()

    # Add data to DB table ingredienten
    # Get all variables to list with the get().split(',') method uding for loop and the eval() method
    for i in range(1, 15):
        entry_name = "ingredient_entry_" + str(i)
        entry_data = eval(entry_name + ".get()").split(',')
        
        # Check if the entry_data list contains only zeros
        if all(data == '0' or data == '' for data in entry_data):
            continue

        # Insert ID_maaltijden at the beginning of the list
        entry_data.insert(0, id_maaltijden)

        # Extend the list with 0s if it has fewer than 7 items
        entry_data.extend(['0'] * (7 - len(entry_data)))

        # Insert data into the table
        c.execute('''INSERT INTO Ingredienten 
                (ID_maaltijden, hoeveelheid,eenheid, ingredient, prijs, winkel, datum_prijs)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                tuple(entry_data))

    conn.commit()
    conn.close()
    messagebox.showinfo("Success", message="Data added successfully!")

# Get a list of all recipies from maaltijden table.
def get_recipies():
    """Function executes querie to get all recepies from maaltijden table.

    Returns:
        List: lijst van alle recepten
    #"""

    r_listbox.delete(0, "end")
    try:
        conn = sqlite3.connect("CuisineCraft.db")

    except Exception as e:
        messagebox.showinfo(message="Was not able to connect to the database !")

    # Define an SQL query
    query = "SELECT * FROM maaltijden ORDER BY ID ASC"

    # Use Pandas to query the database and return a DataFrame
    df = pd.read_sql_query(query, conn)

    recepten = df["recept_naam"].to_list()
    meal_ids = df["ID"].to_list()

    # Add meal names + add count/ID to beginnning of name.
    for count in range(len(recepten)):
        recept = recepten[count]
        m_id = meal_ids[count]
        maaltijd = f"{m_id}) {recept}"
        r_listbox.insert(tk.END, maaltijd)

    return df

# Get 7 random meals.
def random_meals():
    """Function executes querie to get 7 random meals."""

    df = get_recipies()

    # Get recepies from table maaltijden.
    df = get_recipies()
    meals = df["recept_naam"].to_list()

    # Randomly select 7 meals.
    random_meals = random.sample(meals, 7)

    # clear the listbox.
    weekgenerator_listbox.delete(0, tk.END)

    # Insert meals into the listbox.
    counter = 0
    for meal in random_meals:
        counter += 1
        meal_counter = str(counter) + ") " + meal 
        weekgenerator_listbox.insert(tk.END, meal_counter)

    # Insert values in treeview
    get_ingredients(random_meals)

    return None

# export the ingredients of the random meals generated:
def get_ingredients(random_meals):
    
    try:
        conn = sqlite3.connect("CuisineCraft.db")

    except Exception as e:
        messagebox.showinfo(message="Was not able to connect to the database !")

    # Define an SQL query
    query = f"""SELECT Ingredienten.ingredient, SUM(Ingredienten.hoeveelheid) AS total_hoeveelheid, Ingredienten.eenheid 
                FROM maaltijden 
                INNER JOIN Ingredienten ON maaltijden.ID = Ingredienten.ID_maaltijden 
                WHERE maaltijden.recept_naam IN ({','.join('?'*len(random_meals))}) 
                GROUP BY Ingredienten.ingredient, Ingredienten.eenheid 
                ORDER BY Ingredienten.ingredient ASC;"""
    
    cursor = conn.cursor()
    cursor.execute(query, random_meals)
    results = cursor.fetchall()
    
    # Create a DataFrame from the SQL query results
    df = pd.DataFrame(results, columns=['ingredient', 'total_hoeveelheid', 'eenheid'])
    
    # Convert the DataFrame to a dictionary
    ingredients_dict = df.to_dict(orient='records')
    
    # Clear the treeview
    for item in ingredienten_rand_meals.get_children():
        ingredienten_rand_meals.delete(item)
    
    # Insert data into the Treeview widget
    for i in range(len(ingredients_dict)):
        ingredienten_rand_meals.insert(parent='', index='end', iid=i, text=i, values=(ingredients_dict[i]['ingredient'], ingredients_dict[i]['total_hoeveelheid'], ingredients_dict[i]['eenheid']))

# export to text file().
def export_to_text_file():
    # Get the selected meals from the listbox
    selected_meals = weekgenerator_listbox.get(0, tk.END)

    # Get the ingredients from the treeview
    ingredients = []
    for item in ingredienten_rand_meals.get_children():
        ingredient = ingredienten_rand_meals.item(item, 'values')
        ingredients.append(','.join(ingredient))

    # Combine the meals and ingredients into a single string
    content = '\n'.join(selected_meals) + '\n' + '\n'.join(ingredients)

    # Open a file dialog to choose the export file path
    file_path = filedialog.asksaveasfilename(
        defaultextension='.txt',
        filetypes=[('Text Files', '*.txt')]
    )

    # Abort the function if file_path is empty
    if not file_path:
        return

    # Write the content to the selected file
    with open(file_path, 'w') as file:
        file.write(content)


################################################################################
# tkinter widgets etc. #########################################################
################################################################################

# create a window (root window)
root = tk.Tk()
root.title("CuisineCraft")
root.geometry("550x800")

# create a notebook and pack it on the root window.
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill='both')

# create multiple tabs for the notebook.
tab_recepten_lijst = ttk.Frame(notebook)
tab_weekmenu_generator = ttk.Frame(notebook)
tab_maaltijden = ttk.Frame(notebook)
tab_ingredienten = ttk.Frame(notebook)

# Add names to the tabs.
notebook.add(tab_recepten_lijst, text='Recepten Lijst')
notebook.add(tab_weekmenu_generator, text='weekmenu generator')
notebook.add(tab_maaltijden, text='Recepten toevoegen')
notebook.add(tab_ingredienten, text='Ingredienten toevoegen aan recept')

############################# Listbox recepten lijst ###########################
# Add a listbox widget to recepten lijst tab with the recepten.
r_listbox = tk.Listbox(tab_recepten_lijst, borderwidth=2)
get_recipies()

# Create a scrollbar for the listbox
scrollbar_listbox_r = tk.Scrollbar(r_listbox)
scrollbar_listbox_r.pack(side='right', fill='y')

# Configure the scrollbar_listbox_r to scroll the listbox
r_listbox.config(yscrollcommand=scrollbar_listbox_r.set)
scrollbar_listbox_r.config(command=r_listbox.yview)

# r_listbox.pack(fill='both', padx=10, pady=10)
r_listbox.pack(fill='both', expand=True, padx=10, pady=(10, 0))

############################# Weekmenu generator ###############################

# Add a listbox to show the 7 randomly selected meals.
weekgenerator_listbox = tk.Listbox(tab_weekmenu_generator, borderwidth=2)

# Create the Treeview widget with two columns
ingredienten_rand_meals = ttk.Treeview(tab_weekmenu_generator, columns=('ingredient', 'hoeveelheid', 'eenheid'), show='headings')

# Add headings for each column
ingredienten_rand_meals.heading('#1', text='Ingredient')
ingredienten_rand_meals.heading('#2', text='Hoeveelheid')
ingredienten_rand_meals.heading('#3', text='eenheid')

# pack the listbox to the tab.
weekgenerator_listbox.pack(fill='both', padx=10, pady=10)

# Button to create the weekmenu.
random_button = tk.Button(
    tab_weekmenu_generator,
    text="Maak een weekMenu",
    command=random_meals) .pack(padx=5, pady=5)

# Button to export the weekmenu and the ingredients list.
# Moet nog functie gemaakt worden voor het exporteren
export_button = tk.Button(
    tab_weekmenu_generator,
    text="Exporteer weekMenu en ingredienten", command=export_to_text_file).pack(padx=5, pady=5)

#Configure the treeview
ingredienten_rand_meals.column(1, width=100)

# Create a scrollbar for the Treeview
scrollbar_treev = ttk.Scrollbar(tab_weekmenu_generator, orient="vertical", command=ingredienten_rand_meals.yview)
scrollbar_treev.pack(side="right", fill="y")
# Configure the scrollbar to scroll the Treeview
ingredienten_rand_meals.configure(yscrollcommand=scrollbar_treev.set)

# Pack the Treeview widget to the tab
ingredienten_rand_meals.pack(fill="y", expand=True, padx=5, pady=5)



################################################################################
############################### Maaltijden tab #################################

# recept
recept_entry_label = tk.Label(tab_maaltijden, text="Naam van het recept")
recept_entry_label.pack(pady=5)
recept_entry = tk.Entry(tab_maaltijden, width=100)
recept_entry.pack(pady=5)

# create a entry for aantal_personen.
aantal_personen_entry_label = tk.Label(tab_maaltijden, text="Aantal personen")
aantal_personen_entry_label.pack(pady=5)
aantal_personen_entry = tk.Entry(tab_maaltijden, width=100)
aantal_personen_entry.pack(pady=5)

# bereidingstijd
bereidingstijd_entry_label = tk.Label(tab_maaltijden, text="Bereidingstijd")
bereidingstijd_entry_label.pack(pady=5)
bereidingstijd_entry = tk.Entry(tab_maaltijden, width=100)
bereidingstijd_entry.pack(pady=5)

# keuken origine
keuken_origine_entry_label = tk.Label(tab_maaltijden, text="Keuken origine")
keuken_origine_entry_label.pack(pady=5)
keuken_origine_entry = tk.Entry(tab_maaltijden, width=100)
keuken_origine_entry.pack(pady=5)

# locatie bestand/recept
locatie_bestand_entry_label = tk.Label(
    tab_maaltijden, text="Locatie van bestand")
locatie_bestand_entry_label.pack(pady=5)
locatie_bestand_entry = tk.Entry(tab_maaltijden, width=100)
locatie_bestand_entry.pack(pady=5)

# url
url_entry_label = tk.Label(tab_maaltijden, text="URL")
url_entry_label.pack(pady=5)
url_entry = tk.Entry(tab_maaltijden, width=100)
url_entry.pack(pady=5)

# gezondheidsgraad
gezondheidsgraad_entry_label = tk.Label(
    tab_maaltijden, text="gezondheidsgraad (1 tot 3 met 1 het gezondste)")
gezondheidsgraad_entry_label.pack(pady=5)
gezondheidsgraad_entry = tk.Entry(tab_maaltijden, width=100)
gezondheidsgraad_entry.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(padx=5, pady=5)

#
##########################END maaltijden widgets ###############################
################################################################################

###########################ingredienten tab widgets ############################

# ingredienten lijst
ingredienten_label = tk.Label(
    tab_ingredienten, text="Geef de ingredienten in als volgt: hoveelheid,eenheid,ingredient").pack(pady=5)
ingredienten_voorbeeld_label = tk.Label(
    tab_ingredienten, text="Voorbeeld = 1,kg,aardappelen").pack(pady=5)

# Add entry's here down.
ingredient_entry_1 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_1.pack(pady=5)

ingredient_entry_2 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_2.pack(pady=5)

ingredient_entry_3 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_3.pack(pady=5)

ingredient_entry_4 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_4.pack(pady=5)

ingredient_entry_5 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_5.pack(pady=5)

ingredient_entry_6 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_6.pack(pady=5)

ingredient_entry_7 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_7.pack(pady=5)

ingredient_entry_8 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_8.pack(pady=5)

ingredient_entry_9 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_9.pack(pady=5)

ingredient_entry_10 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_10.pack(pady=5)

ingredient_entry_11 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_11.pack(pady=5)

ingredient_entry_12 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_12.pack(pady=5)

ingredient_entry_13 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_13.pack(pady=5)

ingredient_entry_14 = tk.Entry(tab_ingredienten, width=100)
ingredient_entry_14.pack(pady=5)


################################# Buttons ######################################

# Add data to database button tab_maaltijden
insert_button = tk.Button(tab_maaltijden, text="Toevoegen",
                          command=insert_data).pack(padx=5, pady=5)

# Button to clear all entries from all tabs
clear_button = tk.Button(
    tab_maaltijden, text="Wis alle invoer", command=clear_entries).pack(padx=5, pady=5)

# Add data to database button tab_ingredienten
insert_button = tk.Button(tab_ingredienten, text="Toevoegen",
                          command=insert_data_ingredienten).pack(padx=5, pady=5)

# Button to clear all entries from all tabs
clear_button = tk.Button(
    tab_ingredienten, text="Wis alle invoer", command=clear_entries).pack(padx=5, pady=5)


# Button to refresch the recepie list.
refresh_button = tk.Button(
    tab_recepten_lijst,
    text="Ververs recepten lijst",
    command=get_recipies).pack(padx=5, pady=5)




root.mainloop()