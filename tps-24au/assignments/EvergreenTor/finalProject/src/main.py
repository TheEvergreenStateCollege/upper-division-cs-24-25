from max_heap import MaxHeap
from dataloader import DataLoader
from leaderboard import Leaderboard
import sys


choices = True

while choices:
    print("Welcome to the soccer leaderboard. Choose an option:")
    print("1: Show leaderboard for 2015")
    print("2: Show leaderboard for 2016")
    print("3: Show leaderboard for 2017")
    print("4: Show leaderboard for 2018")
    print("5: Show leaderboard for 2019")
    print("6: Show leaderboard for 2020")
    print("7: Show leaderboard for 2021")
    print("8: Show leaderboard for 2022")
    print("9: Show leaderboard for 2023")
    print("10: Show leaderboard for 2024")
    print("0: quit")

    try:
        number = 0
        number = int(input("Enter a number: "))
    except ValueError:
        print("Invalid input. Please enter a number.\n")

    if sys.version_info[1] < 12:
        if number == 0:
            choices = False
            print("Have a good day")
        elif number == 1:
            leaderboard = Leaderboard('../data/2015.csv')
            print(leaderboard)
        elif number == 2:
            leaderboard = Leaderboard('../data/2016.csv')
            print(leaderboard)
        elif number == 3:
            leaderboard = Leaderboard('../data/2017.csv')
            print(leaderboard)
        elif number == 4:
            leaderboard = Leaderboard('../data/2018.csv')
            print(leaderboard)
        elif number == 5:
            leaderboard = Leaderboard('../data/2019.csv')
            print(leaderboard)
        elif number == 6:
            leaderboard = Leaderboard('../data/2020.csv')
            print(leaderboard)
        elif number == 7:
            leaderboard = Leaderboard('../data/2021.csv')
            print(leaderboard)
        elif number == 8:
            leaderboard = Leaderboard('../data/2022.csv')
            print(leaderboard)
        elif number == 9:
            leaderboard = Leaderboard('../data/2023.csv')
            print(leaderboard)
        elif number == 10:
            leaderboard = Leaderboard('../data/2024.csv')
            print(leaderboard)
        else:
            rick = f"""             We're no strangers to love
            You know the rules and so do I
            A full commitment's what I'm thinkin' of
            You wouldn't get this from any other guy
            I just wanna tell you how I'm feeling
            Gotta make you understand
            Never gonna give you up
            Never gonna let you down
            Never gonna run around and desert you
            Never gonna make you cry
            Never gonna say goodbye
            Never gonna tell a lie and hurt you
            We've known each other for so long
            Your heart's been aching, but you're too shy to say it
            Inside, we both know what's been going on
            We know the game and we're gonna play it
            And if you ask me how I'm feeling
            Don't tell me you're too blind to see
            Never gonna give you up
            Never gonna let you down
            Never gonna run around and desert you
            Never gonna make you cry
            Never gonna say goodbye
            Never gonna tell a lie and hurt you
            Never gonna give you up
            Never gonna let you down
            Never gonna run around and desert you
            Never gonna make you cry
            Never gonna say goodbye
            Never gonna tell a lie and hurt you
            We've known each other for so long
            Your heart's been aching, but you're too shy to say it
            Inside, we both know what's been going on
            We know the game and we're gonna play it
            I just wanna tell you how I'm feeling
            Gotta make you understand
            Never gonna give you up
            Never gonna let you down
            Never gonna run around and desert you
            Never gonna make you cry
            Never gonna say goodbye
            Never gonna tell a lie and hurt you
            Never gonna give you up
            Never gonna let you down
            Never gonna run around and desert you
            Never gonna make you cry
            Never gonna say goodbye
            Never gonna tell a lie and hurt you
            Never gonna give you up
            Never gonna let you down
            Never gonna run around and desert you
            Never gonna make you cry
            Never gonna say goodbye
            Never gonna tell a lie and hurt you"""
            print(rick)
    elif sys.version_info[1] >= 12:
        match number:
            case 0:
                choices = False
                print("Have a good day")
            case 1:
                leaderboard = Leaderboard('../data/2015.csv')
                print(leaderboard)
            case 2:
                leaderboard = Leaderboard('../data/2016.csv')
                print(leaderboard)
            case 3:
                leaderboard = Leaderboard('../data/2017.csv')
                print(leaderboard)
            case 4:
                leaderboard = Leaderboard('../data/2018.csv')
                print(leaderboard)
            case 5:
                leaderboard = Leaderboard('../data/2019.csv')
                print(leaderboard)
            case 6:
                leaderboard = Leaderboard('../data/2020.csv')
                print(leaderboard)
            case 7:
                leaderboard = Leaderboard('../data/2021.csv')
                print(leaderboard)
            case 8:
                leaderboard = Leaderboard('../data/2022.csv')
                print(leaderboard)
            case 9:
                leaderboard = Leaderboard('../data/2023.csv')
                print(leaderboard)
            case 10:
                leaderboard = Leaderboard('../data/2024.csv')
                print(leaderboard)
            case _:
                rick = f"""             We're no strangers to love
                You know the rules and so do I
                A full commitment's what I'm thinkin' of
                You wouldn't get this from any other guy
                I just wanna tell you how I'm feeling
                Gotta make you understand
                Never gonna give you up
                Never gonna let you down
                Never gonna run around and desert you
                Never gonna make you cry
                Never gonna say goodbye
                Never gonna tell a lie and hurt you
                We've known each other for so long
                Your heart's been aching, but you're too shy to say it
                Inside, we both know what's been going on
                We know the game and we're gonna play it
                And if you ask me how I'm feeling
                Don't tell me you're too blind to see
                Never gonna give you up
                Never gonna let you down
                Never gonna run around and desert you
                Never gonna make you cry
                Never gonna say goodbye
                Never gonna tell a lie and hurt you
                Never gonna give you up
                Never gonna let you down
                Never gonna run around and desert you
                Never gonna make you cry
                Never gonna say goodbye
                Never gonna tell a lie and hurt you
                We've known each other for so long
                Your heart's been aching, but you're too shy to say it
                Inside, we both know what's been going on
                We know the game and we're gonna play it
                I just wanna tell you how I'm feeling
                Gotta make you understand
                Never gonna give you up
                Never gonna let you down
                Never gonna run around and desert you
                Never gonna make you cry
                Never gonna say goodbye
                Never gonna tell a lie and hurt you
                Never gonna give you up
                Never gonna let you down
                Never gonna run around and desert you
                Never gonna make you cry
                Never gonna say goodbye
                Never gonna tell a lie and hurt you
                Never gonna give you up
                Never gonna let you down
                Never gonna run around and desert you
                Never gonna make you cry
                Never gonna say goodbye
                Never gonna tell a lie and hurt you"""
                print(rick)

    



