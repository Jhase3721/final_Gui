import flet as ft
import random
import os

# Categories data (same as your original code)
categories = {
    'Animals': [
        ('Elephant', 'It\'s the largest land animal, with big ears and a long trunk.'),
        ('Tiger', 'This animal is known for its orange fur with black stripes.'),
        ('Giraffe', 'This animal is known for its long neck and legs.'),
        ('Zebra', 'It has black and white stripes all over its body.'),
        ('Lion', 'This animal is known as the "King of the Jungle" and has a mane.'),
        ('Kangaroo', 'This animal is known for hopping and has a pouch for its babies.'),
        ('Koala', 'A bear-like marsupial from Australia, loves eucalyptus leaves.'),
        ('Panda', 'This animal is black and white and loves eating bamboo.'),
        ('Cheetah', 'The fastest land animal, known for its speed and spots.'),
        ('Gorilla', 'This animal is a large primate and lives in the forests of Africa.')
    ],
    'Countries': [
        ('Brazil', 'This country is famous for its Amazon rainforest and the Carnival festival.'),
        ('Australia', 'This country is both a continent and home to the Great Barrier Reef.'),
        ('India', 'A large country in Asia, known for its rich culture and the Taj Mahal.'),
        ('Canada', 'This country is known for its maple syrup, ice hockey, and cold winters.'),
        ('Russia', 'This is the largest country in the world by land area.'),
        ('Japan', 'This island country is known for its technology, culture, and sushi.'),
        ('United States', 'This country is home to New York City, Hollywood, and the Grand Canyon.'),
        ('Mexico', 'This country is known for tacos, tequila, and beautiful beaches.'),
        ('Germany', 'This country is known for its cars, beer, and the Brandenburg Gate.'),
        ('China', 'This country has the Great Wall, pandas, and is the most populous country.')
    ],
    'Foods': [
        ('Pizza', 'This is a popular Italian dish with cheese, sauce, and various toppings.'),
        ('Burger', 'A sandwich with a patty, often served with cheese, lettuce, and tomato.'),
        ('Pasta', 'This is a traditional Italian dish made from wheat flour and water.'),
        ('Sushi', 'A Japanese dish consisting of vinegared rice, seafood, and vegetables.'),
        ('Tacos', 'A Mexican dish made with a folded tortilla filled with various ingredients.'),
        ('Burrito', 'A large Mexican dish consisting of a flour tortilla wrapped around filling.'),
        ('Noodles', 'A staple in many Asian cuisines, often made from wheat or rice.'),
        ('Salad', 'A dish made with raw vegetables, fruits, or other ingredients.'),
        ('Steak', 'A cut of beef, usually cooked by grilling or frying.'),
        ('Fried Chicken', 'A popular dish of chicken coated in seasoned batter and deep-fried.')
    ],
    'Movies': [
        ('Titanic', 'A tragic romance movie set on the famous ship that sank in 1912.'),
        ('Avatar', 'A sci-fi movie about a human who explores a lush, alien world called Pandora.'),
        ('Inception', 'A mind-bending thriller about dreams within dreams.'),
        ('The Godfather', 'A classic crime movie about a powerful mafia family.'),
        ('The Shawshank Redemption', 'A story about a man imprisoned for a crime he didn’t commit.'),
        ('The Dark Knight', 'A Batman movie where the hero faces off against the Joker.'),
        ('Forrest Gump', 'A drama about a man with a low IQ who influences major events.'),
        ('Gladiator', 'A historical epic about a betrayed Roman general seeking revenge.'),
        ('The Matrix', 'A sci-fi movie exploring the idea of simulated reality.'),
        ('Pulp Fiction', 'A nonlinear crime drama directed by Quentin Tarantino.')
    ],
    'Sports': [
        ('Soccer', 'The world’s most popular sport, played with a ball and 11 players.'),
        ('Basketball', 'A sport where teams of five players shoot a ball through a hoop.'),
        ('Tennis', 'A sport where players hit a ball over a net using rackets.'),
        ('Baseball', 'A bat-and-ball game where players hit a pitched ball and run to bases.'),
        ('Cricket', 'A bat-and-ball sport played between two teams of 11 players.'),
        ('Rugby', 'A contact sport where teams carry or kick a ball to score.'),
        ('Hockey', 'A sport played on ice where players hit a puck into a goal.'),
        ('Swimming', 'A sport where individuals race in water by various techniques.'),
        ('Boxing', 'A combat sport where two people fight by punching with gloves.'),
        ('Golf', 'A sport where players hit a ball into holes on a course using clubs.')
    ]
}


# File handling for PIN
def save_pin(pin):
    with open("user_pin.txt", "w") as file:
        file.write(pin)


def load_pin():
    if os.path.exists("user_pin.txt"):
        with open("user_pin.txt", "r") as file:
            return file.read().strip()
    return None


# Main Flet app
def main(page: ft.Page):
    page.title = "Guessing Game"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Game state
    lives = 10
    score = 0
    current_category = None
    current_items = []
    current_index = 0

    # UI elements
    pin_input = ft.TextField(label="Enter 4-digit PIN", password=True, width=200)
    message = ft.Text("")
    guess_input = ft.TextField(label="Your Guess", width=300)
    hint_text = ft.Text("")
    lives_text = ft.Text(f"Lives: {lives}")
    score_text = ft.Text(f"Score: {score}")
    category_buttons = [
        ft.ElevatedButton(text=cat, on_click=lambda e, c=cat: start_category(c)) for cat in categories.keys()
    ]

    def update_message(text, color="black"):
        message.value = text
        message.color = color
        page.update()

    def register_pin(e):
        pin = pin_input.value
        if len(pin) == 4 and pin.isdigit():
            save_pin(pin)
            update_message("PIN successfully registered!", "green")
            show_main_menu()
        else:
            update_message("Invalid PIN. Please enter a 4-digit number.", "red")

    def verify_pin(e):
        stored_pin = load_pin()
        if not stored_pin:
            update_message("No PIN registered yet. Please register a PIN first.", "red")
            show_pin_register()
        elif pin_input.value == stored_pin:
            update_message("PIN verified! Welcome to the game!", "green")
            show_category_menu()
        else:
            update_message("Incorrect PIN. Access denied.", "red")

    def start_category(category):
        nonlocal current_category, current_items, current_index, lives, score
        current_category = category
        current_items = list(categories[category])
        random.shuffle(current_items)
        current_index = 0
        lives = 10
        score = 0
        lives_text.value = f"Lives: {lives}"
        score_text.value = f"Score: {score}"
        show_game_screen()

    def check_guess(e):
        nonlocal lives, score, current_index
        guess = guess_input.value.capitalize()
        item, _ = current_items[current_index]

        if guess == item:
            score += 1
            update_message("Correct!", "green")
            score_text.value = f"Score: {score}"
        else:
            lives -= 1
            update_message(f"Wrong! The correct answer was {item}.", "red")
            lives_text.value = f"Lives: {lives}"

        guess_input.value = ""
        current_index += 1

        if lives == 0:
            update_message("Game Over! You have no lives left.", "red")
            show_category_menu()
        elif current_index >= len(current_items):
            update_message(f"Category completed! Your score: {score}", "green")
            show_category_menu()
        else:
            show_next_item()

    def show_next_item():
        item, hint = current_items[current_index]
        hint_text.value = f"Hint: {hint}"
        page.update()

    # Screen layouts
    def show_pin_entry():
        page.controls.clear()
        page.add(
            ft.Column([
                ft.Text("--- Main Menu ---", size=20),
                pin_input,
                ft.Row([
                    ft.ElevatedButton("Enter PIN", on_click=verify_pin),
                    ft.ElevatedButton("Register PIN", on_click=lambda e: show_pin_register()),
                    ft.ElevatedButton("Exit", on_click=lambda e: page.window_close())
                ]),
                message
            ])
        )
        page.update()

    def show_pin_register():
        page.controls.clear()
        page.add(
            ft.Column([
                ft.Text("Register a 4-digit PIN", size=20),
                pin_input,
                ft.ElevatedButton("Save PIN", on_click=register_pin),
                message
            ])
        )
        page.update()

    def show_main_menu():
        page.controls.clear()
        page.add(
            ft.Column([
                ft.Text("--- Main Menu ---", size=20),
                ft.ElevatedButton("Enter PIN to Play", on_click=lambda e: show_pin_entry()),
                ft.ElevatedButton("Register/Update PIN", on_click=lambda e: show_pin_register()),
                ft.ElevatedButton("Exit", on_click=lambda e: page.window_close())
            ])
        )
        page.update()

    def show_category_menu():
        page.controls.clear()
        page.add(
            ft.Column([
                ft.Text("--- Category Menu ---", size=20),
                *category_buttons,
                ft.ElevatedButton("Back to Main Menu", on_click=lambda e: show_main_menu())
            ])
        )
        page.update()

    def show_game_screen():
        page.controls.clear()
        page.add(
            ft.Column([
                ft.Text(f"--- {current_category} ---", size=20),
                hint_text,
                guess_input,
                ft.ElevatedButton("Submit Guess", on_click=check_guess),
                lives_text,
                score_text,
                message
            ])
        )
        show_next_item()

    # Start with main menu
    show_main_menu()


ft.app(target=main)