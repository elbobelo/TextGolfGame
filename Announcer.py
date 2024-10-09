import random
def create_announcer():
    heads = (
        (
            "😸 Meow! Welcome to the golf course, golfers! 🐱 Let's have a purr-fect game!",
            "😸 Purr-fect shot! 🎯 You're on fire, golfers! 🔥",
            "😸 Ooh, that's a wet one! 🌊 Hope you're not feline sorry about that shot! 😹",
            "😸 Sandy paws! 🐾 You're in a tight spot, golfers! 🤣"
        ),
        (
            "😀 Welcome to the course, golfers! 🎉 Let's get this party started! 🎉",
            "😀 Great shot! 🎯 You're on a roll, golfers! 🎉",
            "😀 Oops! 🌊 Better luck next time, golfers! 😞",
            "😀 Uh-oh, sandy shot! 🏖️ Better luck next time, golfers! 😞"
        ),
        (
            "🐵 Welcome to the course, golfers! 🌴 Let's swing into action! 🌴",
            "🐵 Ooh ooh! Great shot! 🎯 You're swinging like a pro, golfers! 🐒",
            "🐵 Ah ah! Water shot! 🌊 Better luck next time, golfers! 🐒",
            "🐵 Uh oh! Sandy shot! 🏖️ Better luck next time, golfers! 🐒"
        )
    )
    return heads[random.randint(0, 2)]