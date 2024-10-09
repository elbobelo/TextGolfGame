import random
import re
#Imports a random hole generator
import random_hole
#Imports a random announcer and their sayings.
import Announcer


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
    ('Water', '\u001b[34m▅\u001b[0m', (0,)),  # No clubs allowed on water
    ('Bunker', '\u001b[93m▆\u001b[0m', (13,)),  # Only Sand Wedge allowed in bunker
    ('Tee', '\u001b[0m█\u001b[0m', (0, 1, 2, 3,)),  # Driver and woods allowed on tee
    ('Green', '\u001b[92m▇\u001b[0m', (14,)),  # Only Putter allowed on green
    ('Fairway', '\u001b[32m▇\u001b[0m', (1, 2, 3, 7, 8, 9, 10, 11, 12,)),  # Woods and irons allowed on fairway
    ('Rough', '\u001b[32m▓\u001b[0m', (4, 5, 6, 7, 8, 9, 10, 11, 12,))  # Only irons and pitching wedge allowed in rough
)
def generate_hole(hole_number):

    yards = random.randint(150, 550)
    base_par = 3 if yards <= 250 else 4 if yards <= 470 else 5 # Determine par based on yardage
    difficulty = random.randint(-1, 1)  # -1, 0, or 1 represents the difficulty adjustment
    par = min(max(base_par + difficulty, 3), 5)
    #creates the fairway and hazards and returns it as a string of numbers.
    segments = random_hole.generate_segments(yards, difficulty, zoom)
    return {
            "yards": yards,
            "par": par,
            "difficulty": difficulty,
            "segments": segments,
            "hole_number": hole_number
        }
def create_player_dict():
    player = {
        'number': 1,
        'name': 0,
        'position': 0,
        'club': 0,
        'score': 0
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
    # Define the list of restricted clubs based on the ball's lie
    RESTRICTED_LIST = LIE_TUPLE[ball['lie']][2]
    # Calculate the distance from the ball's current position to the pin
    distance_to_pin = abs(hole['yards'] - ball['position'])
    # Iterate through the list of restricted clubs
    for i, club in enumerate(RESTRICTED_LIST):
        # Check if the club's maximum distance is greater than or equal to the distance to the pin
        if CLUB_TUPLE[club][2] >= distance_to_pin:
            # If it is, continue to the next iteration
            continue
        # If we find a club with a maximum distance less than the distance to the pin,
        # return the previous club in the list (using max to ensure a non-negative index)
        return RESTRICTED_LIST[max(0, i - 1)]
    # If we reach the end of the list without finding a suitable club, return the last club in the list
    return RESTRICTED_LIST[len(RESTRICTED_LIST) - 1]

def hit_ball(hole, player, power, ball):
    #Simulates the player hitting the ball with the selected club and specified power.

    # Calculate the distance the ball travels based on club and power
    club_max_distance = CLUB_TUPLE[player['club']][2]  # Get maximum distance of selected club
    hit_distance = int(club_max_distance * (power / 100))  # Scale distance based on power

    # Update ball position based on direction and prevent going beyond hole length
    if ball['position'] <= hole['yards']:
        new_position = ball['position'] + hit_distance
    else:
        new_position = ball['position'] - hit_distance

    # Update ball stroke count
    ball['stroke'] += 1

    # Update ball lie based on the new position and hole segments
    if 0 <= new_position < len(hole['segments']) * zoom:
        lie = int(hole['segments'][new_position // zoom])
        # Check if the lie is not 0
        if lie != 0:
            ball['lie'] = lie
            ball['position'] = new_position
        else:
            print("WATER")
    else:
        print("OUT OF BOUNDS")

def print_segments(hole, ball, player):
    positions = {player['position'] // zoom: "🏌 ",
                 hole['yards'] // zoom: "",
                 ball['position'] // zoom: ". "}
    segment_display = " " * len(hole['segments'])
    for position, character in positions.items():
        segment_display = segment_display[:position] + character + segment_display[position + 2:]
    print(f"{segment_display}🌳")
    new_segments = ''.join([LIE_TUPLE[int(c)][1] for c in hole['segments']])
    print(new_segments)
    print(hole['segments'])

def display_segments(segments):
    print("\n".join(LIE_TUPLE[int(s)] for s in segments))
def display_hole(hole, ball, player):
    print(f"Hole {hole['hole_number']}, Par {hole['par']}, {hole['yards']} yards")
    print_segments(hole, ball, player)
    print(f"Score: {player['score']}")
    print(f"Stroke: {ball['stroke']}, Lie: {LIE_TUPLE[ball['lie']][0]}")
    print(f"Club: {CLUB_TUPLE[player['club']][0]} (Max: {CLUB_TUPLE[player['club']][2]} yards)")
    print(f"Distance to Pin: {hole['yards'] - ball['position']} yards")

zoom = 4
holes = []
player = create_player_dict()
announcer = Announcer.create_announcer()
print(announcer[0])
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
    player['score'] += ball['stroke'] - hole['par']  # Update player's score
    print(f"Score: {player['score']}")  # Display updated score
    print(announcer[1])
