import flet as ft
import random
import os
import json
import time
from flet_audio import Audio  # Import Audio from flet-audio package

# Categories data
default_categories = {
    'Animals': [('Elephant', 'It\'s the largest land animal.', 'elepahnt.jpg'),
                ('Tiger', 'Orange fur with black stripes.', 'tigra.jpg'),
                ('Lion', 'This animal is known as the "King of the Jungle" and has a mane.', 'king.jpg'),
                ('Giraffe', 'This animal is known for its long neck and legs.', 'giraf.jpg'),
                ('Zebra', 'It has black and white stripes all over its body.', 'zeb.jpg'),
                ('Kangaroo', 'This animal is known for hopping and has a pouch for its babies.', 'kan.jpg'),
                ('Koala', 'A bear-like marsupial from Australia, loves eucalyptus leaves.', 'ko.jpg'),
                ('Panda', 'This animal is black and white and loves eating bamboo.', 'pan.jpg'),
                ('Cheetah', 'The fastest land animal, known for its speed and spots.', 'che.jpg'),
                ('Gorilla', 'This animal is a large primate and lives in the forests of Africa.', 'gori.jpg')],
    'Countries': [('Brazil', 'Famous for Amazon rainforest.', 'https://images.unsplash.com/photo-1544984243-ec57ce'),
                  ('Australia', 'Home to Great Barrier Reef.', 'https://images.unsplash.com/photo-1506973035872-a4ec'),
                  ('India', 'A large country in Asia, known for its rich culture and the Taj Mahal.', 'indi.jpg'),
                  ('Canada', 'This country is known for its maple syrup, ice hockey, and cold winters.', 'cana.jpg'),
                  ('Russia', 'This is the largest country in the world by land area.', 'rus.jpg'),
                  ('Japan', 'This island country is known for its technology, culture, and sushi.', 'jap.jpg'),
                  ('United States', 'This country is home to New York City, Hollywood, and the Grand Canyon.', 'us.jpg'),
                  ('Mexico', 'This country is known for tacos, tequila, and beautiful beaches.', 'mex.jpg'),
                  ('Germany', 'This country is known for its cars, beer, and the Brandenburg Gate.', 'ger.jpg'),
                  ('China', 'This country has the Great Wall, pandas, and is the most populous country.', 'chi.jpg')],
    'Foods': [('Pizza', 'Popular Italian dish.', 'piz.jpg'),
              ('Burger', 'Sandwich with a patty.', 'bur.jpg'),
              ('Pasta', 'This is a traditional Italian dish made from wheat flour and water.', 'pas.jpg'),
              ('Sushi', 'A Japanese dish consisting of vinegared rice, seafood, and vegetables.', 'sus.jpg'),
              ('Tacos', 'A Mexican dish made with a folded tortilla filled with various ingredients.', 'taco.jpg'),
              ('Burrito', 'A large Mexican dish consisting of a flour tortilla wrapped around filling.', 'burr.jpg'),
              ('Noodles', 'A staple in many Asian cuisines, often made from wheat or rice.', 'nod.jpg'),
              ('Salad', 'A dish made with raw vegetables, fruits, or other ingredients.', 'sal.jpg'),
              ('Steak', 'A cut of beef, usually cooked by grilling or frying.', 'stik.jpg'),
              ('Fried Chicken', 'A popular dish of chicken coated in seasoned batter and deep-fried.', 'fri.jpg')],
    'Movies': [('Titanic', 'Tragic romance on a ship.', 'ti.jpg'),
               ('Avatar', 'Sci-fi on Pandora.', 'ava.jpg'),
               ('Inception', 'A mind-bending thriller about dreams within dreams.', 'inc.jpg'),
               ('The Godfather', 'A classic crime movie about a powerful mafia family.', 'god.jpg'),
               ('The Shawshank Redemption', 'A story about a man imprisoned for a crime he didn’t commit.', 'shaw.jpg'),
               ('The Dark Knight', 'A Batman movie where the hero faces off against the Joker.', 'dar.jpg'),
               ('Forrest Gump', 'A drama about a man with a low IQ who influences major events.', 'for.jpg'),
               ('Gladiator', 'A historical epic about a betrayed Roman general seeking revenge.', 'gla.jpg'),
               ('The Matrix', 'A sci-fi movie exploring the idea of simulated reality.', 'mi.jpg'),
               ('Pulp Fiction', 'A nonlinear crime drama directed by Quentin Tarantino.', 'pulp.jpg')],
    'Sports': [('Soccer', 'World’s most popular sport.', 'sco.jpg'),
               ('Basketball', 'Shoot a ball through a hoop.', 'bas.jpg'),
               ('Tennis', 'A sport where players hit a ball over a net using rackets.', 'ten.jpg'),
               ('Baseball', 'A bat-and-ball game where players hit a pitched ball and run to bases.', 'base.jpg'),
               ('Cricket', 'A bat-and-ball sport played between two teams of 11 players.', 'crick.jpg'),
               ('Rugby', 'A contact sport where teams carry or kick a ball to score.', 'rug.jpg'),
               ('Hockey', 'A sport played on ice where players hit a puck into a goal.', 'hoc.jpg'),
               ('Swimming', 'A sport where individuals race in water by various techniques.', 'swim.jpg'),
               ('Boxing', 'A combat sport where two people fight by punching with gloves.', 'box.jpg'),
               ('Golf', 'A sport where players hit a ball into holes on a course using clubs.', 'golf.jpg')]
}

# Load custom categories
def load_custom_categories():
    if os.path.exists("custom_categories.json"):
        with open("custom_categories.json", "r") as file:
            return json.load(file)
    return {}

categories = {**default_categories, **load_custom_categories()}

# File handling
def save_pin(pin):
    with open("user_pin.txt", "w") as file:
        file.write(pin)

def load_pin():
    if os.path.exists("user_pin.txt"):
        with open("user_pin.txt", "r") as file:
            return file.read().strip()
    return None

def save_high_score(score, player_name):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": player_name, "score": score})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard[:10], file)

def load_leaderboard():
    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r") as file:
            return json.load(file)
    return []

def save_stats(stats):
    with open("stats.json", "w") as file:
        json.dump(stats, file)

def load_stats():
    if os.path.exists("stats.json"):
        with open("stats.json", "r") as file:
            return json.load(file)
    return {"games_played": 0, "wins": 0, "total_score": 0, "favorite_category": ""}

def save_achievements(achievements):
    with open("achievements.json", "w") as file:
        json.dump(achievements, file)

def load_achievements():
    if os.path.exists("achievements.json"):
        with open("achievements.json", "r") as file:
            return json.load(file)
    return {}

# Main Flet app
def main(page: ft.Page):
    page.title = "Guessing Game"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.with_opacity(0.95, ft.Colors.BLUE_GREY_900)
    page.window_bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0

    # Game state
    lives = 10
    score = [0, 0]  # Multiplayer scores [P1, P2]
    high_score = max([entry["score"] for entry in load_leaderboard()], default=0)
    current_category = None
    current_items = []
    current_index = 0
    player_turn = 0  # 0 for single player, 1 for P1, 2 for P2
    difficulty = "Medium"
    timer_enabled = False
    multiplayer = False
    time_left = ft.Text("Time Left: 30s", size=14, color=ft.Colors.WHITE)
    hint_image = ft.Image(width=100, height=100, fit=ft.ImageFit.COVER, opacity=0.5)
    player_name = ""
    stats = load_stats()
    achievements = load_achievements()
    sound_enabled = True
    theme = "Dark"

    # UI elements with restricted PIN input
    pin_input = ft.TextField(
        label="Enter 4-digit PIN",
        password=True,
        width=250,
        border_radius=10,
        border_color=ft.Colors.BLUE_700,
        focused_border_color=ft.Colors.BLUE_900,
        text_style=ft.TextStyle(size=16),
        hint_text="e.g., 1234",
        keyboard_type=ft.KeyboardType.NUMBER,  # Restrict to numeric keyboard
        input_filter=ft.InputFilter(regex_string=r"[0-9]"),  # Allow only digits
        max_length=4,  # Limit to 4 characters
        on_change=lambda e: validate_pin_input(e.control.value)  # Real-time validation
    )
    name_input = ft.TextField(label="Enter Your Name", width=250, border_radius=10, border_color=ft.Colors.BLUE_700)
    message = ft.Text("", size=14, color=ft.Colors.WHITE)
    guess_input = ft.TextField(label="Your Guess", width=300, border_radius=10, border_color=ft.Colors.PURPLE_700, focused_border_color=ft.Colors.PURPLE_900, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE), animate_offset=ft.Animation(500, ft.AnimationCurve.BOUNCE_OUT))
    hint_text = ft.Container(content=ft.Text("", size=16, color=ft.Colors.WHITE), shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.PURPLE_400))
    lives_text = ft.Text(f"Lives: {lives}", size=14, color=ft.Colors.WHITE)
    score_text = ft.Text(f"Score: {score[0]}", size=18, color=ft.Colors.YELLOW_700, weight=ft.FontWeight.BOLD)
    score_text_p2 = ft.Text(f"P2 Score: {score[1]}", size=18, color=ft.Colors.YELLOW_700, weight=ft.FontWeight.BOLD)
    high_score_text = ft.Text(f"High Score: {high_score}", size=14, color=ft.Colors.GREEN_400)
    progress_bar = ft.ProgressBar(width=300, value=0, bgcolor=ft.Colors.GREY_700, color=ft.Colors.PURPLE_700)

    # Audio (using flet-audio, added to page.overlay)
    correct_sound = Audio(src="https://freesound.org/data/previews/171/171671_2437358-lq.mp3", autoplay=False)
    wrong_sound = Audio(src="https://freesound.org/data/previews/203/203027_3623647-lq.mp3", autoplay=False)
    game_over_sound = Audio(src="https://freesound.org/data/previews/66/66106_843429-lq.mp3", autoplay=False)
    background_music = Audio(
        src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        autoplay=False,
        volume=0.3,
        release_mode="LOOP"
    )
    page.overlay.extend([correct_sound, wrong_sound, game_over_sound, background_music])

    # Start background music after adding to page
    def start_background_music():
        if sound_enabled:
            background_music.play()

    page.update()
    start_background_music()

    # PIN validation function
    def validate_pin_input(value):
        if len(value) > 0 and (not value.isdigit() or len(value) > 4):
            update_message("Please enter exactly 4 digits.", ft.Colors.RED_700)
        elif len(value) == 4 and value.isdigit():
            update_message("Valid PIN format!", ft.Colors.GREEN_700)
        else:
            update_message("", ft.Colors.WHITE)  # Clear message if incomplete but valid so far

    # Category buttons
    category_data = {
        'Animals': "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        'Countries': "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        'Foods': "fods.jpg",
        'Movies': "movies.jpg",
        'Sports': "sports.jpg"
    }
    category_buttons = []

    def update_category_buttons():
        nonlocal category_buttons
        category_buttons = [
            ft.ElevatedButton(
                content=ft.Container(
                    content=ft.Row([
                        ft.Image(src=url, width=50, height=50, fit=ft.ImageFit.COVER, border_radius=8, error_content=ft.Text("Image not found")),
                        ft.Text(cat, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                    gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.BLUE_600, ft.Colors.PURPLE_600]),
                    padding=15,
                    border_radius=12,
                    alignment=ft.alignment.center,
                    expand=True
                ),
                on_click=lambda e, c=cat: start_category(c),
                width=350,
                height=70,
                style=ft.ButtonStyle(bgcolor=ft.Colors.TRANSPARENT, shape=ft.RoundedRectangleBorder(radius=12), elevation=5, overlay_color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE)),
                on_hover=lambda e: button_hover(e),
                animate_scale=ft.Animation(200, ft.AnimationCurve.BOUNCE_OUT),
            ) for cat, url in {**category_data, **{k: "https://via.placeholder.com/50" for k in load_custom_categories()}}.items()
        ]

    update_category_buttons()

    def update_message(text, color=ft.Colors.WHITE):
        message.value = text
        message.color = color
        page.update()

    def play_sound(sound):
        if sound_enabled:
            sound.play()

    def set_difficulty(diff):
        nonlocal difficulty, lives
        difficulty = diff
        lives = {"Easy": 15, "Medium": 10, "Hard": 5}[difficulty]
        lives_text.value = f"Lives: {lives}"
        update_message(f"Difficulty set to {difficulty}", ft.Colors.YELLOW_700)

    def toggle_timer_mode(e):
        nonlocal timer_enabled
        timer_enabled = not timer_enabled
        update_message(f"Timer Mode: {'On' if timer_enabled else 'Off'}", ft.Colors.YELLOW_700)

    def toggle_multiplayer(e):
        nonlocal multiplayer
        multiplayer = not multiplayer
        update_message(f"Multiplayer Mode: {'On' if multiplayer else 'Off'}", ft.Colors.YELLOW_700)

    def toggle_sound(e):
        nonlocal sound_enabled
        sound_enabled = not sound_enabled
        if sound_enabled:
            background_music.play()
        else:
            background_music.pause()
        update_message(f"Sound: {'On' if sound_enabled else 'Off'}", ft.Colors.YELLOW_700)
        page.update()

    def toggle_theme(e):
        nonlocal theme
        theme = "Light" if theme == "Dark" else "Dark"
        page.bgcolor = ft.Colors.WHITE if theme == "Light" else ft.Colors.with_opacity(0.95, ft.Colors.BLUE_GREY_900)
        update_message(f"Theme: {theme}", ft.Colors.YELLOW_700)
        page.update()

    def register_pin(e):
        pin = pin_input.value
        if len(pin) == 4 and pin.isdigit():
            save_pin(pin)
            update_message("PIN successfully registered!", ft.Colors.GREEN_700)
            show_main_menu()
        else:
            update_message("Invalid PIN. Please enter a 4-digit number.", ft.Colors.RED_700)

    def verify_pin(e):
        stored_pin = load_pin()
        if not stored_pin:
            update_message("No PIN registered yet. Please register a PIN first.", ft.Colors.RED_700)
            show_pin_register()
        elif pin_input.value == stored_pin:
            nonlocal player_name
            player_name = name_input.value if name_input.value else "Player"
            update_message("PIN verified! Welcome to the game!", ft.Colors.GREEN_700)
            show_category_menu()
        else:
            update_message("Incorrect PIN. Access denied.", ft.Colors.RED_700)

    def start_category(category):
        nonlocal current_category, current_items, current_index, lives, score, player_turn
        current_category = category
        if category == "Random":
            all_items = [item for cat in categories.values() for item in cat]
            current_items = random.sample(all_items, min(10, len(all_items)))
        else:
            current_items = list(categories[category])
        random.shuffle(current_items)
        current_index = 0
        lives = {"Easy": 15, "Medium": 10, "Hard": 5}[difficulty]
        score = [0, 0]
        player_turn = 1 if multiplayer else 0
        lives_text.value = f"Lives: {lives}"
        score_text.value = f"Score: {score[0]}"
        score_text_p2.value = f"P2 Score: {score[1]}"
        progress_bar.value = 0
        show_game_screen()

    def check_guess(e):
        nonlocal lives, score, current_index, high_score, player_turn, stats, achievements
        guess = guess_input.value.capitalize()
        try:
            item, _, _ = current_items[current_index]
            if guess == item:
                score[player_turn - 1 if multiplayer else 0] += 1
                update_message("Correct!", ft.Colors.GREEN_700)
                play_sound(correct_sound)
                score_text.value = f"Score: {score[0]}"
                if multiplayer:
                    score_text_p2.value = f"P2 Score: {score[1]}"
                if score[0] > high_score:
                    high_score = score[0]
                    save_high_score(high_score, player_name)
                    high_score_text.value = f"High Score: {high_score}"
                if lives == {"Easy": 15, "Medium": 10, "Hard": 5}[difficulty] and current_index == len(current_items) - 1:
                    achievements["Perfect Score"] = True
            else:
                lives -= 1
                update_message(f"Wrong! The correct answer was {item}.", ft.Colors.RED_700)
                play_sound(wrong_sound)
                lives_text.value = f"Lives: {lives}"

            guess_input.value = ""
            current_index += 1
            progress_bar.value = current_index / len(current_items)

            if multiplayer:
                player_turn = 3 - player_turn  # Switch between 1 and 2
                update_message(f"Player {player_turn}'s turn", ft.Colors.YELLOW_700)

            if lives <= 0:
                stats["games_played"] += 1
                update_message(f"Game Over! Final Score: {score[0]}{f' vs {score[1]}' if multiplayer else ''}", ft.Colors.RED_700)
                play_sound(game_over_sound)
                save_high_score(score[0], f"{player_name} P1")
                if multiplayer:
                    save_high_score(score[1], f"{player_name} P2")
                show_game_over_screen()
            elif current_index >= len(current_items):
                stats["games_played"] += 1
                stats["wins"] += 1
                stats["total_score"] += score[0]
                if stats["favorite_category"] == "":
                    stats["favorite_category"] = current_category
                update_message(f"Category completed! Final Score: {score[0]}{f' vs {score[1]}' if multiplayer else ''}", ft.Colors.GREEN_700)
                save_high_score(score[0], f"{player_name} P1")
                if multiplayer:
                    save_high_score(score[1], f"{player_name} P2")
                show_game_over_screen()
            else:
                show_next_item()
        except IndexError:
            update_message("Error: No more items to guess!", ft.Colors.RED_700)
            show_category_menu()

    def request_hint(e):
        nonlocal lives, score
        if lives > 1:
            lives -= 1
            lives_text.value = f"Lives: {lives}"
            hint_image.opacity = 1.0
            update_message("Hint revealed at the cost of 1 life!", ft.Colors.YELLOW_700)
            page.update()

    def show_next_item():
        try:
            item, hint, img_url = current_items[current_index]
            hint_text.content.value = f"Hint: {hint}"
            hint_image.src = img_url
            hint_image.opacity = 0.01  # Blurred initially
            progress_bar.value = current_index / len(current_items)
            page.update()
            if timer_enabled:
                start_timer()
        except IndexError:
            update_message("Error: No more items to guess!", ft.Colors.RED_700)
            show_category_menu()

    def start_timer():
        nonlocal time_left
        seconds = 30
        def update_timer():
            nonlocal seconds
            if seconds > 0:
                seconds -= 1
                time_left.value = f"Time Left: {seconds}s"
                page.update()
                page.run_task(update_timer, delay=1)
            else:
                check_guess(None)  # Wrong guess on timeout
        page.run_task(update_timer, delay=1)

    def button_hover(e):
        if hasattr(e.control, 'content') and e.control.content is not None and hasattr(e.control.content, 'gradient'):
            if e.data == "true":
                e.control.scale = 1.05
                e.control.content.gradient = ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.BLUE_800, ft.Colors.PURPLE_800])
            else:
                e.control.scale = 1.0
                e.control.content.gradient = ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.BLUE_600, ft.Colors.PURPLE_600])
            e.control.update()

    def show_pin_entry():
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Welcome to the Guessing Game", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900, text_align=ft.TextAlign.CENTER),
                    ft.Text("Please enter your 4-digit PIN to continue", size=16, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
                    name_input,
                    ft.Row([ft.Icon(ft.Icons.LOCK, color=ft.Colors.BLUE_700), pin_input], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    ft.Row([
                        ft.ElevatedButton("Login", on_click=verify_pin, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10), padding=15, elevation=5)),
                        ft.ElevatedButton("Register PIN", on_click=lambda e: show_pin_register(), style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10), padding=15, elevation=5)),
                        ft.ElevatedButton("Exit", on_click=lambda e: page.window.destroy(), style=ft.ButtonStyle(bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10), padding=15, elevation=5))
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                    message
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                padding=20,
                bgcolor=ft.Colors.BLACK54,
                border_radius=15,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.RED),
                width=400,
                height=400,
                alignment=ft.alignment.center,
                animate_opacity=300,
            )
        )
        page.update()

    def show_pin_register():
        page.controls.clear()
        page.add(
            ft.Column([
                ft.Text("Register a 4-digit PIN", size=20, color=ft.Colors.WHITE),
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
                    ft.Text("Guessing Game", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
                    ft.Text("Test your knowledge and have fun!", size=16, color=ft.Colors.BLUE_GREY_200, text_align=ft.TextAlign.CENTER),
                    high_score_text,
                    ft.ElevatedButton("Enter PIN to Play", on_click=lambda e: show_pin_entry(), width=250, height=50, style=ft.ButtonStyle(bgcolor=ft.Colors.INDIGO_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=15, elevation=5)),
                    ft.ElevatedButton("Settings", on_click=lambda e: show_settings(), width=250, height=50, style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=15, elevation=5)),
                    ft.ElevatedButton("Leaderboard", on_click=lambda e: show_leaderboard(), width=250, height=50, style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=15, elevation=5)),
                    ft.ElevatedButton("Achievements", on_click=lambda e: show_achievements(), width=250, height=50, style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=15, elevation=5)),
                    ft.ElevatedButton("Stats", on_click=lambda e: show_stats(), width=250, height=50, style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=15, elevation=5)),
                    ft.ElevatedButton("Custom Categories", on_click=lambda e: show_custom_category(), width=250, height=50, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=15, elevation=5)),
                    ft.ElevatedButton("Exit", on_click=lambda e: page.window.destroy(), width=250, height=50, style=ft.ButtonStyle(bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=15, elevation=5))
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                padding=40,
                gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.BLUE_GREY_800, ft.Colors.INDIGO_900]),
                border_radius=20,
                alignment=ft.alignment.center,
                width=450,
                shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK))
            )
        )
        page.update()

    def show_settings():
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Settings", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.ElevatedButton("Toggle Timer Mode", on_click=toggle_timer_mode, width=250, style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12))),
                    ft.ElevatedButton("Toggle Multiplayer", on_click=toggle_multiplayer, width=250, style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12))),
                    ft.ElevatedButton("Toggle Sound", on_click=toggle_sound, width=250, style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12))),
                    ft.ElevatedButton("Toggle Theme", on_click=toggle_theme, width=250, style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12))),
                    ft.Dropdown(
                        label="Difficulty",
                        options=[ft.dropdown.Option("Easy"), ft.dropdown.Option("Medium"), ft.dropdown.Option("Hard")],
                        value=difficulty,
                        on_change=lambda e: set_difficulty(e.control.value),
                        width=250
                    ),
                    ft.ElevatedButton("Back", on_click=lambda e: show_main_menu(), width=250, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_700, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12)))
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                padding=40,
                gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.BLUE_GREY_800, ft.Colors.INDIGO_900]),
                border_radius=20,
                width=450
            )
        )
        page.update()

    def show_leaderboard():
        leaderboard = load_leaderboard()
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Leaderboard", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    *[ft.Text(f"{i+1}. {entry['name']} - {entry['score']}", size=16, color=ft.Colors.WHITE) for i, entry in enumerate(leaderboard)],
                    ft.ElevatedButton("Back", on_click=lambda e: show_main_menu(), width=250, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_700, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12)))
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                padding=40,
                gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.BLUE_GREY_800, ft.Colors.INDIGO_900]),
                border_radius=20,
                width=450
            )
        )
        page.update()

    def show_achievements():
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Achievements", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Perfect Score: " + ("Unlocked" if achievements.get("Perfect Score") else "Locked"), size=16, color=ft.Colors.WHITE),
                    ft.ElevatedButton("Back", on_click=lambda e: show_main_menu(), width=250, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_700, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12)))
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                padding=40,
                gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.BLUE_GREY_800, ft.Colors.INDIGO_900]),
                border_radius=20,
                width=450
            )
        )
        page.update()

    def show_stats():
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Statistics", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"Games Played: {stats['games_played']}", size=16, color=ft.Colors.WHITE),
                    ft.Text(f"Wins: {stats['wins']}", size=16, color=ft.Colors.WHITE),
                    ft.Text(f"Total Score: {stats['total_score']}", size=16, color=ft.Colors.WHITE),
                    ft.Text(f"Favorite Category: {stats['favorite_category']}", size=16, color=ft.Colors.WHITE),
                    ft.ElevatedButton("Back", on_click=lambda e: show_main_menu(), width=250, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_700, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12)))
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                padding=40,
                gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.BLUE_GREY_800, ft.Colors.INDIGO_900]),
                border_radius=20,
                width=450
            )
        )
        page.update()

    def show_custom_category():
        cat_name = ft.TextField(label="Category Name", width=250)
        item_name = ft.TextField(label="Item Name", width=250)
        item_hint = ft.TextField(label="Hint", width=250)
        item_image = ft.TextField(label="Image URL (optional)", width=250)
        items = []

        def add_item(e):
            items.append((item_name.value, item_hint.value, item_image.value or "https://via.placeholder.com/50"))
            item_name.value = item_hint.value = item_image.value = ""
            update_message(f"Added {len(items)} items", ft.Colors.YELLOW_700)
            page.update()

        def save_category(e):
            if cat_name.value and items:
                custom_cats = load_custom_categories()
                custom_cats[cat_name.value] = items
                with open("custom_categories.json", "w") as file:
                    json.dump(custom_cats, file)
                global categories
                categories = {**default_categories, **custom_cats}
                update_category_buttons()
                show_category_menu()
            else:
                update_message("Please enter a category name and at least one item", ft.Colors.RED_700)

        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Create Custom Category", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    cat_name,
                    item_name,
                    item_hint,
                    item_image,
                    ft.ElevatedButton("Add Item", on_click=add_item, width=250, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12))),
                    ft.ElevatedButton("Save Category", on_click=save_category, width=250, style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12))),
                    ft.ElevatedButton("Back", on_click=lambda e: show_main_menu(), width=250, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_700, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12))),
                    message
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                padding=40,
                gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.BLUE_GREY_800, ft.Colors.INDIGO_900]),
                border_radius=20,
                width=450
            )
        )
        page.update()

    def show_category_menu():
        page.controls.clear()
        page.bgcolor = ft.Colors.TRANSPARENT
        page.add(
            ft.Stack([
                ft.Container(
                    content=ft.Image(src="https://images.unsplash.com/photo-1557683316-973673baf926?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80", fit=ft.ImageFit.COVER, opacity=0.3),
                    width=page.width,
                    height=page.height,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Container(content=ft.Text("Choose Your Category", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER), shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.PURPLE_500)),
                        ft.Text("Pick a topic to test your skills!", size=16, color=ft.Colors.BLUE_GREY_100, text_align=ft.TextAlign.CENTER, italic=True),
                        high_score_text,
                        *category_buttons,
                        ft.ElevatedButton(
                            content=ft.Row([ft.Icon(ft.Icons.SHUFFLE, color=ft.Colors.WHITE), ft.Text("Random", size=16, color=ft.Colors.WHITE)], alignment=ft.MainAxisAlignment.CENTER),
                            on_click=lambda e: start_category("Random"),
                            width=350,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_600, shape=ft.RoundedRectangleBorder(radius=12))
                        ),
                        ft.ElevatedButton(
                            content=ft.Row([ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.WHITE), ft.Text("Back to Main Menu", size=16, color=ft.Colors.WHITE)], alignment=ft.MainAxisAlignment.CENTER),
                            on_click=lambda e: show_main_menu(),
                            width=350,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_700, shape=ft.RoundedRectangleBorder(radius=12))
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                    padding=40,
                    gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.with_opacity(0.8, ft.Colors.INDIGO_800), ft.Colors.with_opacity(0.8, ft.Colors.PURPLE_900)]),
                    border_radius=20,
                    width=450,
                    alignment=ft.alignment.center,
                    animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
                )
            ])
        )
        page.update()

    def show_game_screen():
        page.controls.clear()
        category_title = ft.Container(content=ft.Text(f"--- {current_category} ---", size=24, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD), shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.PURPLE_500), animate_opacity=ft.Animation(1000, ft.AnimationCurve.EASE_IN_OUT), opacity=0)
        bg_image = category_data.get(current_category, "https://images.unsplash.com/photo-1557683316-973673baf926") if current_category != "Random" else "https://images.unsplash.com/photo-1557683316-973673baf926"
        page.add(
            ft.Stack([
                ft.Container(content=ft.Image(src=bg_image, fit=ft.ImageFit.COVER, opacity=0.3), width=page.width, height=page.height),
                ft.Container(
                    content=ft.Column(
                        [
                            category_title,
                            time_left if timer_enabled else ft.Text(""),
                            hint_text,
                            hint_image,
                            ft.ElevatedButton("Reveal Image Hint", on_click=request_hint, style=ft.ButtonStyle(bgcolor=ft.Colors.YELLOW_700, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10))),
                            guess_input,
                            ft.ElevatedButton("Submit Guess", on_click=check_guess, style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_700, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10))),
                            progress_bar,
                            ft.Row([lives_text, score_text, score_text_p2 if multiplayer else ft.Text()], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                            high_score_text,
                            message
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    ),
                    gradient=ft.RadialGradient(center=ft.Alignment(0, 0), radius=1.5, colors=[ft.Colors.BLUE_GREY_900, ft.Colors.PURPLE_900, ft.Colors.INDIGO_900]),
                    padding=40,
                    border_radius=20,
                    alignment=ft.alignment.center,
                    width=450,
                    height=page.height,
                )
            ])
        )
        category_title.opacity = 1
        guess_input.offset = ft.transform.Offset(0, 1)
        guess_input.offset = ft.transform.Offset(0, 0)
        page.update()
        show_next_item()

    def show_game_over_screen():
        save_stats(stats)
        save_achievements(achievements)
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Game Over!", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"Final Score: {score[0]}{f' vs {score[1]}' if multiplayer else ''}", size=24, color=ft.Colors.YELLOW_700, weight=ft.FontWeight.BOLD),
                    high_score_text,
                    ft.ElevatedButton("Back to Categories", on_click=lambda e: show_category_menu(), style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_700, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10)))
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                padding=40,
                gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.BLUE_GREY_800, ft.Colors.INDIGO_900]),
                border_radius=20,
                alignment=ft.alignment.center,
                width=450
            )
        )
        page.update()

    show_main_menu()

ft.app(target=main)