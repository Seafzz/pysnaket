import random
import curses
import _curses  # Import the _curses module for error handling

# Ask the user some questions before the game starts
player_name = input("What's your name? ")

# Ask if the player has played before
while True:
    played_before = input("Have you played this game before? (yes/no) ").lower()
    if played_before in ['yes', 'no']:
        break
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

# If the player has played before, skip the instructions
if played_before == 'no':
    while True:
        controll_the_snake = input("Use the arrow keys to control the snake.\
        you can hold the arrow down for the snake to go faster.\
        Do not let the snake reach the border of the window or eat itself!\
        Press 'Enter' to continue. ")
        if controll_the_snake == '':
            break
        else:
            print("Invalid input. Please press 'ENTER' to continue.")
# Initialize curses mode
stdscr = curses.initscr()

try:
    # Try to make the cursor invisible
    curses.curs_set(0)
except _curses.error:
    # If the terminal doesn't support it, just ignore the error
    pass

# Initialize the screen
s = curses.initscr()

try:
    # Set the cursor to 0 (invisible)
    curses.curs_set(0)
except _curses.error:
    # If the terminal doesn't support it, just ignore the error
    pass

# Get the height and width of the screen
sh, sw = s.getmaxyx()
# Create a new window using screen height and width
w = curses.newwin(sh, sw, 0, 0)
# Accept keypad input
w.keypad(1)
# Refresh the screen every 100 milliseconds
w.timeout(100)

# Create the snake
snk_x = sw//4
snk_y = sh//2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

# Create the food
food = [sh//2, sw//2]
w.addch(int(food[0]), int(food[1]), curses.ACS_PI)

# Initialize the game state
key = curses.KEY_RIGHT

# Initialize the score
score = 0

while True:
    next_key = w.getch()
    key = key if next_key == -1 else next_key

    if key not in [curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT]:
        continue
    # Check if snake has eaten the food
    if snake[0] == food:
        score += 1  # Increase the score
        # Your food generation code...
    else:
        # Your snake movement code...

        # Check if game over
        if snake[0][0] in [0, sh] or \
            snake[0][1]  in [0, sw] or \
            snake[0] in snake[1:]:
            # End the window
            curses.endwin()
            print(f"Congratulations {player_name}! Your score is {score}.")
            quit()

        # Calculate the new head of the snake
        new_head = [snake[0][0], snake[0][1]]

        # Move the snake
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        # Insert the new head of the snake
        snake.insert(0, new_head)

        # Check if snake has eaten the food
        if snake[0] == food:
            score += 1  # Increase the score
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh-1),
                    random.randint(1, sw-1)
                ]
                # If the new food position is not part of the snake, place the food there
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI)
        else:
            # Remove the tail of the snake
            tail = snake.pop()
            w.addch(int(tail[0]), int(tail[1]), ' ')

        # Add the new head of the snake to the screen
        if 0 <= snake[0][0] < sh and 0 <= snake[0][1] < sw:
            w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
        else:
            # End the window
            curses.endwin()
            print(f"Congratulations {player_name}! Your score is {score}.")
            quit()