import random
import re

def generate_hole(hole_number):

    yards = random.randint(150, 550)
    base_par = 3 if yards <= 250 else 4 if yards <= 470 else 5 # Determine par based on yardage
    difficulty = random.randint(-1, 1)  # -1, 0, or 1 represents the difficulty adjustment
    par = min(max(base_par + difficulty, 3), 5)
    segments = generate_segments(yards, difficulty)
    return {
            "yards": yards,
            "par": par,
            "difficulty": difficulty,
            "segments": segments,
            "hole_number": hole_number
        }

def generate_segments(yards, difficulty):
    segments = "4" * (yards // zoom)

    # Add rough to the fairway
    rough_width = random.randint(1, 3)
    rough_count = random.randint(0, 3)
    rough_positions = random.sample(range(0, len(segments)), rough_count)
    rough_lengths = [random.randint(1, rough_width) for _ in range(rough_count)]

    # Ensure there is always a patch in the first 1/10th of the string
    first_tenth_width = int(len(segments) / 10)
    first_tenth_pos = random.randint(0, first_tenth_width - 1)
    first_tenth_length = random.randint(1, rough_width)
    segments = segments[:first_tenth_pos] + "5" * first_tenth_length + segments[first_tenth_pos + 1:]

    # Ensure there is always a patch in the last 2/3rd of the string
    last_two_third_width = int(len(segments) * 2 / 3)
    last_two_third_pos = random.randint(first_tenth_width, last_two_third_width - 1)
    last_two_third_length = random.randint(1, rough_width) - difficulty
    segments = segments[:last_two_third_pos] + "5" * last_two_third_length + segments[last_two_third_pos + 1:]

    # Add the rest of the rough patches
    for i, r in zip(rough_positions, rough_lengths):
        segments = segments[:i] + "5" * r + segments[i + 1:]

    # Add the B patches (only in the last half of the string)
    num_b_patches = random.randint(1, 4 - difficulty)
    b_positions = random.sample(range(len(segments) // 2, len(segments)), num_b_patches)
    b_lengths = [random.randint(1, 2) for _ in range(num_b_patches)]
    for i, l in zip(b_positions, b_lengths):
        segments = segments[:i] + "1" * l + segments[i + l:]

    # Add the W patch
    w_pos = random.randint(0, len(segments))
    w_len = random.randint(2, 6) - difficulty * 2
    segments = segments[:w_pos] + "0" * w_len + segments[w_pos + w_len:]

    # Add the T, GGG, and F segments
    segments = "2" + segments

    # Calculate the position of the first G
    g_pos = yards // zoom -1

    # Build a string of 1 to 6 Gs
    g_str = "33"
    for i in range(6):
        chance = 1.0 - i * 0.2  # decreasing chance of adding another G
        if random.random() < chance:
            g_str += "3"
            if random.randint(0, 1) == 0:  # 50% chance of shifting left
                g_pos -= 1
        else:
            break  # no more Gs added

    # Add the string of Gs to the segments string at the position
    segments = segments[:g_pos] + g_str + segments[g_pos:]
    return segments

def create_announcer():
    heads = {
        "😸": "Woohoo! You're on a roll!",
        "😀": "Great shot! Keep it up!",
        "🐵": "Uh-oh, better luck next time!"
    }
    head = random.choice(list(heads.keys()))
    Announcer = {"head": head, "text": heads[head]}
    return Announcer

def create_player_dict():
    player = {
        'number': 1,
        'name': 0,
        'position': 0,
        'club': 0
    }
    return player

def init_ball():
    ball = {
        "lie": 2,  # Initialize lie to "tee"
        "stroke": 1,
        "position": 0,
    }
    return ball

def select_club(hole, ball):
    # Calculate the distance to the pin
    distance_to_pin = abs(hole['yards'] - ball['position'])
    clubs_in_range = [(i, max_dist - distance_to_pin)
                      for i, (club_name, min_dist, max_dist, _) in enumerate(CLUB_TUPLE)
                      if distance_to_pin <= max_dist and distance_to_pin >= min_dist]
    if clubs_in_range:
        closest_club = min(clubs_in_range, key=lambda x: abs(x[1]))
        return closest_club[0]
    else:
        longest_club = max(enumerate(CLUB_TUPLE), key=lambda x: x[1][2])
        return longest_club[0]

def hit_ball(hole, player, power, ball):
    hit_distance = int(CLUB_TUPLE[player['club']][2] * (power / 100))
    ball['position'] += hit_distance if ball['position'] <= hole['yards'] else -hit_distance
    ball['stroke'] += 1
    ball['lie'] = int(hole['segments'][ball['position'] // zoom])
    print(f"Hit Distance: {hit_distance}")

def print_segments(hole, ball, player):
    positions = {player['position'] // zoom // 2: "🏌️ ",
                 hole['yards'] // zoom // 2: "🚩",
                 ball['position'] // zoom // 2: ". "}
    segment_display = "".join([positions.get(i, "  ") for i in range(len(hole['segments']*2))])
    print(segment_display)
    new_segments = ''.join([LIE_TUPLE[int(c)][1] for c in hole['segments']])
    print(new_segments)

def display_hole(hole, ball, player):
    print(f"\n*** Hole {hole['hole_number']} ***")
    print(f"Par {hole['par']}, {hole['yards']} yards")
    print(f"")
    print_segments(hole, ball, player)
    print(f"Stroke: {ball['stroke']}, Lie: {LIE_TUPLE[ball['lie']][0]}")
    print(f"Distance to Pin: {hole['yards'] - ball['position']} yards")
    print(f"Club: {CLUB_TUPLE[player['club']][0]} (Max: {CLUB_TUPLE[player['club']][2]} yards)")

zoom = 4

CLUB_TUPLE = (
    ("Driver", 220, 300, 12),
    ("3-wood", 200, 240, 14),
    ("5-wood", 180, 220, 16),
    ("7-wood", 170, 210, 18),
    ("2-iron", 190, 230, 20),
    ("3-iron", 180, 220, 22),
    ("4-iron", 170, 210, 24),
    ("5-iron", 160, 200, 26),
    ("6-iron", 150, 190, 28),
    ("7-iron", 140, 180, 30),
    ("8-iron", 130, 170, 32),
    ("9-iron", 120, 160, 34),
    ("Pitching Wedge", 110, 150, 36),
    ("Sand Wedge", 60, 100, 40),
    ("Putter", 1, 100, 5)
)

LIE_TUPLE = (
    ('Water', '\u001b[34m▅\u001b[0m'),
    ('Bunker', '\u001b[93m▆\u001b[0m'),
    ('Tee', '\u001b[0m█\u001b[0m'),
    ('Green', '\u001b[92m▇\u001b[0m'),
    ('Fairway', '\u001b[32m▇\u001b[0m'),
    ('Rough', '\u001b[32m▓\u001b[0m')
)


holes = []
player = create_player_dict()
Announcer = create_announcer()
print(f"{Announcer['head']} hello")
for i in range(1, 19):  # start from 1, end at 19 (exclusive)
    hole = generate_hole(i)
    holes.append(hole)
# Display the holes to the user
for hole in holes:
    ball = init_ball()
    player['position'] = 0  # Update player's position to 0 when a new hole starts
    while ball['position'] != hole['yards']:
        player['club'] = select_club(hole, ball)
        display_hole(hole, ball, player)
        print(f"Hit Percentage? (1-100)")
        user_input = input()
        try:
            power = int(user_input)
            if 1 <= power <= 100:
                player['position'] = ball['position']
                hit_ball(hole, player, power, ball)  # Pass the club index to hit_ball
            else:
                print("Invalid input. Try again.")
        except ValueError:
            print("Invalid input. Try again.")
    else:
        print(f"{Announcer['head']} You made it! {Announcer['text']}")
