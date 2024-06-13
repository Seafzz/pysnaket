import random
import curses

# Initialize the screen
s = curses.initscr()
# Set the cursor to 0 (invisible)
try:
    curses.curs_set(0)
except curses.error:
    pass

# Get the height and width of the screen
sh, sw = s.getmaxyx()

# Ask for the player's name
s.addstr(sh//2, sw//2, "What's your name?")
s.refresh()
curses.echo()
name = s.getstr().decode('utf-8')

# Ask if the player wants to start the game
s.clear()
s.addstr(sh//2, sw//2, "Do you want to start the game, {}? (Y/N)".format(name))
s.refresh()
start_game = s.getch()

# If the player doesn't want to start the game, then exit
if start_game not in [ord('y'), ord('Y')]:
    curses.endwin()
    quit()

# Turn off echo
curses.noecho()

# Create a new window for the game
w = curses.newwin(sh, sw, 0, 0)

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

# Game loop
while True:
    # Get the next key
    next_key = w.getch()
    # If no key is pressed, then use the current key
    key = key if next_key == -1 else next_key

    # Check if game over
    if snake[0][0] in [0, sh] or \
        snake[0][1]  in [0, sw] or \
        snake[0] in snake[1:]:
        # End the window
        curses.endwin()
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
    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)