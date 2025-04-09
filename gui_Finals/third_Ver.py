import flet as ft
import random
import os

# Categories data
categories = {
    'Animals': [('Elephant', 'It\'s the largest land animal.'), ('Tiger', 'Orange fur with black stripes.'),('Lion', 'This animal is known as the "King of the Jungle" and has a mane.'),('Kangaroo', 'This animal is known for hopping and has a pouch for its babies.'),('Koala', 'A bear-like marsupial from Australia, loves eucalyptus leaves.'),('Panda', 'This animal is black and white and loves eating bamboo.'),('Cheetah', 'The fastest land animal, known for its speed and spots.'),('Gorilla', 'This animal is a large primate and lives in the forests of Africa.')],
    'Countries': [('Brazil', 'Famous for Amazon rainforest.'), ('Australia', 'Home to Great Barrier Reef.'),('India', 'A large country in Asia, known for its rich culture and the Taj Mahal.'),('Canada', 'This country is known for its maple syrup, ice hockey, and cold winters.'),('Russia', 'This is the largest country in the world by land area.'),('Japan', 'This island country is known for its technology, culture, and sushi.'),('United States', 'This country is home to New York City, Hollywood, and the Grand Canyon.'),('Mexico', 'This country is known for tacos, tequila, and beautiful beaches.'),('Germany', 'This country is known for its cars, beer, and the Brandenburg Gate.'),('China', 'This country has the Great Wall, pandas, and is the most populous country.')],
    'Foods': [('Pizza', 'Popular Italian dish.'), ('Burger', 'Sandwich with a patty.'), ('Pasta', 'This is a traditional Italian dish made from wheat flour and water.'),('Sushi', 'A Japanese dish consisting of vinegared rice, seafood, and vegetables.'),('Tacos', 'A Mexican dish made with a folded tortilla filled with various ingredients.'),('Burrito', 'A large Mexican dish consisting of a flour tortilla wrapped around filling.'),('Noodles', 'A staple in many Asian cuisines, often made from wheat or rice.'),('Salad', 'A dish made with raw vegetables, fruits, or other ingredients.'), ('Steak', 'A cut of beef, usually cooked by grilling or frying.'), ('Fried Chicken', 'A popular dish of chicken coated in seasoned batter and deep-fried.')],
    'Movies': [('Titanic', 'Tragic romance on a ship.'), ('Avatar', 'Sci-fi on Pandora.'),('Inception', 'A mind-bending thriller about dreams within dreams.'),('The Godfather', 'A classic crime movie about a powerful mafia family.'),('The Shawshank Redemption', 'A story about a man imprisoned for a crime he didn’t commit.'),('The Dark Knight', 'A Batman movie where the hero faces off against the Joker.'),('Forrest Gump', 'A drama about a man with a low IQ who influences major events.'),('Gladiator', 'A historical epic about a betrayed Roman general seeking revenge.'),('The Matrix', 'A sci-fi movie exploring the idea of simulated reality.'),('Pulp Fiction', 'A nonlinear crime drama directed by Quentin Tarantino.')],
    'Sports': [('Soccer', 'World’s most popular sport.'), ('Basketball', 'Shoot a ball through a hoop.'), ('Tennis', 'A sport where players hit a ball over a net using rackets.'),('Baseball', 'A bat-and-ball game where players hit a pitched ball and run to bases.'),('Cricket', 'A bat-and-ball sport played between two teams of 11 players.'),('Rugby', 'A contact sport where teams carry or kick a ball to score.'),('Hockey', 'A sport played on ice where players hit a puck into a goal.'),('Swimming', 'A sport where individuals race in water by various techniques.'),('Boxing', 'A combat sport where two people fight by punching with gloves.'),('Golf', 'A sport where players hit a ball into holes on a course using clubs.')]
}

# File handling for PIN
def save_pin(pin):
    try:
        with open("user_pin.txt", "w") as file:
            file.write(pin)
    except Exception as e:
        print(f"Error saving PIN: {e}")

def load_pin():
    try:
        if os.path.exists("user_pin.txt"):
            with open("user_pin.txt", "r") as file:
                return file.read().strip()
        return None
    except Exception as e:
        print(f"Error loading PIN: {e}")
        return None

# Main Flet app
def main(page: ft.Page):
    page.title = "Guessing Game"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.with_opacity(0.95, ft.colors.BLUE_GREY_900)
    page.window_bgcolor = ft.colors.TRANSPARENT
    page.padding = 0

    # Game state
    lives = 10
    score = 0
    current_category = None
    current_items = []
    current_index = 0

    # UI elements
    pin_input = ft.TextField(
        label="Enter 4-digit PIN",
        password=True,
        width=250,
        border_radius=10,
        border_color=ft.colors.BLUE_700,
        focused_border_color=ft.colors.BLUE_900,
        text_style=ft.TextStyle(size=16),
        hint_text="e.g., 1234",
        on_focus=lambda e: pin_input.update(),
        bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
    )
    message = ft.Text("", size=14, color=ft.colors.WHITE)
    guess_input = ft.TextField(
        label="Your Guess",
        width=300,
        border_radius=10,
        border_color=ft.colors.PURPLE_700,
        focused_border_color=ft.colors.PURPLE_900,
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
        animate_offset=ft.Animation(500, ft.AnimationCurve.BOUNCE_OUT)
    )
    hint_text = ft.Container(
        content=ft.Text(
            "",
            size=16,
            color=ft.colors.WHITE,
        ),
        shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.PURPLE_400)
    )
    lives_text = ft.Text(f"Lives: {lives}", size=14, color=ft.colors.WHITE)
    score_text = ft.Text(f"Score: {score}", size=14, color=ft.colors.WHITE)

    # Category buttons
    category_data = {
        'Animals': "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        'Countries': "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        'Foods': "https://images.unsplash.com/photo-1513106580091-1d82408b8cd6?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        'Movies': "https://images.unsplash.com/photo-1598899134739-24c46f58b1c0?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        'Sports': "https://images.unsplash.com/photo-1579952363873-27f3b2847da0?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
    }
    category_buttons = [
        ft.ElevatedButton(
            content=ft.Container(
                content=ft.Row([
                    ft.Image(src=url, width=50, height=50, fit=ft.ImageFit.COVER, border_radius=8),
                    ft.Text(cat, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.colors.BLUE_600, ft.colors.PURPLE_600]),
                padding=15,
                border_radius=12,
                alignment=ft.alignment.center,
                expand=True
            ),
            on_click=lambda e, c=cat: start_category(c),
            width=350,
            height=70,
            style=ft.ButtonStyle(bgcolor=ft.colors.TRANSPARENT, shape=ft.RoundedRectangleBorder(radius=12), elevation=5, overlay_color=ft.colors.with_opacity(0.15, ft.colors.WHITE)),
            on_hover=lambda e: button_hover(e),
            animate_scale=ft.Animation(200, ft.AnimationCurve.BOUNCE_OUT),
        ) for cat, url in category_data.items()
    ]

    def update_message(text, color="white"):
        message.value = text
        message.color = color
        page.update()

    def register_pin(e):
        pin = pin_input.value
        if len(pin) == 4 and pin.isdigit():
            save_pin(pin)
            update_message("PIN successfully registered!", ft.colors.GREEN_700)
            show_main_menu()
        else:
            update_message("Invalid PIN. Please enter a 4-digit number.", ft.colors.RED_700)

    def verify_pin(e):
        stored_pin = load_pin()
        if not stored_pin:
            update_message("No PIN registered yet. Please register a PIN first.", ft.colors.RED_700)
            show_pin_register()
        elif pin_input.value == stored_pin:
            update_message("PIN verified! Welcome to the game!", ft.colors.GREEN_700)
            show_category_menu()
        else:
            update_message("Incorrect PIN. Access denied.", ft.colors.RED_700)

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
        try:
            item, _ = current_items[current_index]
            if guess == item:
                score += 1
                update_message("Correct!", ft.colors.GREEN_700)
                score_text.value = f"Score: {score}"
            else:
                lives -= 1
                update_message(f"Wrong! The correct answer was {item}.", ft.colors.RED_700)
                lives_text.value = f"Lives: {lives}"

            guess_input.value = ""
            current_index += 1

            if lives <= 0:
                update_message("Game Over! You have no lives left.", ft.colors.RED_700)
                show_category_menu()
            elif current_index >= len(current_items):
                update_message(f"Category completed! Your score: {score}", ft.colors.GREEN_700)
                show_category_menu()
            else:
                show_next_item()
        except IndexError:
            update_message("Error: No more items to guess!", ft.colors.RED_700)
            show_category_menu()

    def show_next_item():
        try:
            item, hint = current_items[current_index]
            hint_text.content.value = f"Hint: {hint}"
            page.update()
        except IndexError:
            update_message("Error: No more items to guess!", ft.colors.RED_700)
            show_category_menu()

    def button_hover(e):
        if e.data == "true":
            e.control.scale = 1.05
            e.control.content.gradient = ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[ft.colors.BLUE_800, ft.colors.PURPLE_800]
            )
        else:
            e.control.scale = 1.0
            e.control.content.gradient = ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[ft.colors.BLUE_600, ft.colors.PURPLE_600]
            )
        e.control.update()

    def show_pin_entry():
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Welcome to the Guessing Game", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900, text_align=ft.TextAlign.CENTER),
                    ft.Text("Please enter your 4-digit PIN to continue", size=16, color=ft.colors.GREY_700, text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    ft.Row([ft.Icon(ft.icons.LOCK, color=ft.colors.BLUE_700), pin_input], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    ft.Row([
                        ft.ElevatedButton("Login", on_click=verify_pin, style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10), padding=15, elevation=5, overlay_color=ft.colors.with_opacity(0.2, ft.colors.BLUE_300)), on_hover=button_hover),
                        ft.ElevatedButton("Register PIN", on_click=lambda e: show_pin_register(), style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10), padding=15, elevation=5, overlay_color=ft.colors.with_opacity(0.2, ft.colors.GREEN_300)), on_hover=button_hover),
                        ft.ElevatedButton("Exit", on_click=lambda e: page.window_close(), style=ft.ButtonStyle(bgcolor=ft.colors.RED_600, color=ft.colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10), padding=15, elevation=5, overlay_color=ft.colors.with_opacity(0.2, ft.colors.RED_300)), on_hover=button_hover)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                    message
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, tight=True),
                padding=20,
                bgcolor=ft.colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.colors.GREY_400, offset=ft.Offset(0, 2)),
                width=400,
                height=350,
                alignment=ft.alignment.center,
                animate_opacity=300,
            )
        )
        page.update()

    def show_pin_register():
        page.controls.clear()
        page.add(
            ft.Column([
                ft.Text("Register a 4-digit PIN", size=20, color=ft.colors.WHITE),
                pin_input,
                ft.ElevatedButton("Save PIN", on_click=register_pin),
                message
            ])
        )
        page.update()

    def show_main_menu():
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Guessing Game", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                    ft.Text("Test your knowledge and have fun!", size=16, color=ft.colors.BLUE_GREY_200, text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                    ft.ElevatedButton("Enter PIN to Play", on_click=lambda e: show_pin_entry(), width=250, height=50, style=ft.ButtonStyle(bgcolor=ft.colors.INDIGO_600, color=ft.colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=15, elevation=5, overlay_color=ft.colors.with_opacity(0.1, ft.colors.WHITE))),
                    ft.ElevatedButton("Register/Update PIN", on_click=lambda e: show_pin_register(), width=250, height=50, style=ft.ButtonStyle(bgcolor=ft.colors.TEAL_600, color=ft.colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=15, elevation=5, overlay_color=ft.colors.with_opacity(0.1, ft.colors.WHITE))),
                    ft.ElevatedButton("Exit", on_click=lambda e: page.window_close(), width=250, height=50, style=ft.ButtonStyle(bgcolor=ft.colors.RED_700, color=ft.colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=15, elevation=5, overlay_color=ft.colors.with_opacity(0.1, ft.colors.WHITE)))
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                padding=40,
                gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.colors.BLUE_GREY_800, ft.colors.INDIGO_900]),
                border_radius=20,
                alignment=ft.alignment.center,
                width=450,
                shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.with_opacity(0.3, ft.colors.BLACK), offset=ft.Offset(0, 5))
            )
        )
        page.update()

    def show_category_menu():
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Choose Your Category", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                    ft.Text("Pick a topic to test your skills!", size=16, color=ft.colors.BLUE_GREY_300, text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                    *category_buttons,
                    ft.ElevatedButton(
                        content=ft.Row([ft.Icon(ft.icons.ARROW_BACK, size=20, color=ft.colors.WHITE), ft.Text("Back to Main Menu", size=16, color=ft.colors.WHITE)], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        on_click=lambda e: show_main_menu(),
                        width=300,
                        height=50,
                        style=ft.ButtonStyle(bgcolor=ft.colors.GREY_700, shape=ft.RoundedRectangleBorder(radius=12), padding=15, elevation=3, overlay_color=ft.colors.with_opacity(0.1, ft.colors.WHITE))
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                padding=40,
                gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.colors.INDIGO_800, ft.colors.PURPLE_900]),
                border_radius=20,
                alignment=ft.alignment.center,
                width=450,
                shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.with_opacity(0.3, ft.colors.BLACK), offset=ft.Offset(0, 5))
            )
        )
        page.update()

    def show_game_screen():
        page.controls.clear()
        category_title = ft.Container(
            content=ft.Text(f"--- {current_category} ---", size=24, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
            shadow=ft.BoxShadow(blur_radius=15, color=ft.colors.PURPLE_500),
            animate_opacity=ft.Animation(1000, ft.AnimationCurve.EASE_IN_OUT),
            opacity=0
        )
        page.add(
            ft.Container(
                content=ft.Column([
                    category_title,
                    hint_text,
                    guess_input,
                    ft.ElevatedButton("Submit Guess", on_click=check_guess, style=ft.ButtonStyle(bgcolor=ft.colors.PURPLE_700, color=ft.colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10), elevation=5)),
                    lives_text,
                    score_text,
                    message
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                gradient=ft.RadialGradient(center=ft.Alignment(0, 0), radius=1.5, colors=[ft.colors.BLUE_GREY_900, ft.colors.PURPLE_900, ft.colors.INDIGO_900]),
                padding=40,
                border_radius=20,
                alignment=ft.alignment.center,
                expand=True
            )
        )
        category_title.opacity = 1
        guess_input.offset = ft.transform.Offset(0, 1)
        guess_input.offset = ft.transform.Offset(0, 0)
        page.update()
        show_next_item()

    show_main_menu()

ft.app(target=main)