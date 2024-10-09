import random
def generate_segments(yards, difficulty, zoom):
    #Create a sting of 4s for the Fairway
    segments = "4" * (yards // zoom)

    # Add Rough to the fairway
    rough_width = random.randint(1, 3)
    rough_count = random.randint(0, 3)
    rough_positions = random.sample(range(0, len(segments)), rough_count)
    rough_lengths = [random.randint(1, rough_width) for _ in range(rough_count)]

    # Ensure there is always a Rough patch in the first 1/10th of the string
    first_tenth_width = int(len(segments) / 10)
    first_tenth_pos = random.randint(0, first_tenth_width - 1)
    first_tenth_length = random.randint(1, rough_width)
    segments = segments[:first_tenth_pos] + "5" * first_tenth_length + segments[first_tenth_pos + 1:]

    # Add Rough patches to the last 2/3rd of the string
    last_two_third_width = int(len(segments) * 2 / 3)
    last_two_third_pos = random.randint(first_tenth_width, last_two_third_width - 1)
    last_two_third_length = random.randint(1, rough_width) - difficulty
    segments = segments[:last_two_third_pos] + "5" * last_two_third_length + segments[last_two_third_pos + 1:]

    # Add the rest of the Rough patches
    for i, r in zip(rough_positions, rough_lengths):
        segments = segments[:i] + "5" * r + segments[i + 1:]

    # Add the Bunker patches (only in the last half of the string)
    num_b_patches = random.randint(1, 4 - difficulty)
    b_positions = random.sample(range(len(segments) // 2, len(segments)), num_b_patches)
    b_lengths = [random.randint(1, 2) for _ in range(num_b_patches)]
    for i, l in zip(b_positions, b_lengths):
        segments = segments[:i] + "1" * l + segments[i + l:]

    # Add the Water patch
    w_pos = random.randint(0, len(segments))
    w_len = random.randint(2, 6) - difficulty * 2
    segments = segments[:w_pos] + "0" * w_len + segments[w_pos + w_len:]

    # Add the Tee
    segments = "2" + segments

    # Calculate the position of the Green
    g_pos = yards // zoom

    # Build a string of 1 to 6 3s for the Green
    g_str = "33"
    for i in range(6):
        chance = 1.0 - i * 0.2  # decreasing chance of adding another 3
        if random.random() < chance:
            g_str += "3"
            if random.randint(0, 1) == 0:  # 50% chance of shifting left
                g_pos -= 1
        else:
            break  # no more Gs added

    # Add the string of Gs to the segments string at the position
    segments = segments[:g_pos] + g_str + segments[g_pos:]
    print(segments)
    return segments

