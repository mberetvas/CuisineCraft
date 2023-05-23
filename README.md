# CuisineCraft Recipe Management System

What ? 
The CuisineCraft Recipe Management System is a Python application that provides a Python application for managing recipes, ingredients, and meal planning. The application is built using the tkinter library for creating the graphical user interface (GUI) and SQLite for storing the recipe and ingredient data. 
 
Why ? 
CuisineCraft is an application designed to make your life easier by generating a weekly menu of recipes that you have added to the database. 
It also provides an ingredients list for the entire week's menu, allowing you to conveniently plan your grocery shopping.


## Requirements

To use the CuisineCraft Recipe Management System, you need to have the following installed:

- Python (version 3.7 or later)
- tkinter library (included with most Python installations)
- sqlite3 module (included with Python)
- pandas library (can be installed using pip: `pip install pandas`)

## How to Use 
# With python 
 
1. Clone or download the code files for the CuisineCraft Recipe Management System.
2. Open the terminal or command prompt and navigate to the directory where the code files are located.
3. Run the application by executing the following command: `python main.py`
4. The application window will open, displaying different tabs for recipe management.
5. Use the tabs to perform the following actions:

   - **Recepten Lijst**: View a list of recipes stored in the database.
   - **weekmenu generator**: Generate a weekly menu by randomly selecting meals from the recipe list.
   - **Recepten toevoegen**: Add new recipes to the database.
   - **Ingredienten toevoegen aan recept**: Add ingredients to a recipe in the database.

6. Follow the instructions provided in the application's interface to interact with the different tabs and perform actions such as adding recipes, ingredients, and generating a weekly menu.

## Using the executable.

""" Work in progress """

## Functionality

The CuisineCraft Recipe Management System provides the following functionality:

- View and manage a list of recipes stored in the database.
- Add new recipes with details such as name, number of servings, preparation time, kitchen origin, file location, URL, and health grade.
- Add ingredients to recipes, specifying the quantity, unit, price, store, and price date for each ingredient.
- Generate a random weekly menu by selecting seven meals from the recipe list.
- View the ingredients required for the selected meals in a tabular format.
- Export the generated weekly menu and ingredient list to a text file.

Note: 
Just a heads up, the application uses a database file called "CuisineCraft.db" to store all the recipe and ingredient data. Before you start using the application, it's recommended to delete this database since it will already have my recipes loaded. :)

## "To-Do list"

- Generate an executable (.exe) file for the source code.
- Implement functionality to redirect users to the corresponding recipe website (URL column in database) upon clicking.
- Integrate web scraping capabilities to update the price column of ingredients. This will provide an approximate cost estimation when exporting the ingredients list for the weekmenu.