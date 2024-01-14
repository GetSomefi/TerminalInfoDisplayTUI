import curses
import time
from datetime import datetime
import json


# Read liputus JSON
def readFile(filename):
    with open(filename, 'r') as file:
        content = json.load(file)
    return content
# Read liputus JSON
#with open('nurmikko.json', 'r') as file:
#    nurmikko = json.load(file)

# Get the current date
current_date = datetime.today()
formatted_date = current_date.strftime("%d.%m.%Y")
# Get the week number
week_number = current_date.isocalendar()[1]

def limit_string_length(input_string, max_length):
    """
    Trim the input string to the specified maximum length.
    """
    if len(input_string) > max_length:
        return input_string[:max_length]
    else:
        return input_string

def get_next_matching_date(date_objects,compare):
    # Find the next matching date
    next_matching_date = None
    for date in sorted(date_objects.keys()):
        if date > compare:
            next_matching_date = date
            break
    return next_matching_date


def clock():
    return time.strftime("%H:%M:%S")

def createPanel(stdscr,width, ph, panel_msg, pos):
    # Create a panel below the line
    panel_height = ph
    panel_msg = " " + panel_msg + " "
    panel_width = min(width, len(panel_msg)+2)  # Adjust the panel width based on message size
    panel = curses.newwin(panel_height, panel_width, pos[0], pos[1])
    panel.box()
    # Add content to the panel
    panel.addstr(1, 1, panel_msg)
    # Refresh the panel to show changes
    panel.refresh()
    stdscr.refresh()

def write_text(stdscr, text, y, x, repeat, color_pair, color_by_row = []):
    # Enable color if supported
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    row_pos = 0
    orig_pos = x
    for row in text:
        for char in row:
            for i in range(repeat):
                color_ = curses.color_pair(color_pair)
                if len(color_by_row)>0:
                    color_ = curses.color_pair(color_by_row[row_pos])
                stdscr.addch(y + row_pos, x, char, color_) #to bold  | curses.A_BOLD
                stdscr.refresh()
                #time.sleep(0.01)  # Optional: Pause to see the effect
            x += 1
        row_pos += 1
        x = orig_pos
        #stdscr.refresh()
        #time.sleep(0.1)

def program(stdscr,loop,once,liputukset,nurmikko):
    curses.curs_set(0)  # Hide the cursor
    #stdscr.clear()



    height, width = stdscr.getmaxyx()

    padding = 2
    start_pos = [padding,padding] #HUOM. y,x
    message = [
        "####################",
        "## INFOTAULU 2000 ##",
        "####################",
        "      by Retro-hiiri"
    ]
    if once[0]:
        write_text(stdscr, message, start_pos[0], start_pos[1], 1, 2)
        # xy = [str(width) + " " + str(height)]
        # posx = width - 4 - len(xy) - padding
        # write_text(stdscr, xy, height-6, posx, 1, 2)

    #loop kerrat
    looped = [str(loop)]
    posx = width - len(looped) - padding
    write_text(stdscr, looped, height-5, posx, 1, 2)

    the_date = f"Tänään on {formatted_date}, viikko {week_number}"
    clock_ = f"Kello {clock()}"
    write_date = [
        "---------------------------------",
        " " + the_date,
        " " + str(clock_),
        "---------------------------------"
    ]
    x = max(0, (width - len(write_date[0])) // 2)
    y = height // 2
    if once[0]:
        write_text(stdscr, write_date, padding, x, 1, 1)

    panel1_pos = [y-8, padding] #nää menee y,x suuntaisesti
    createPanel(stdscr,width, 3, "Liputusvuoro",panel1_pos)

    start_pos = [panel1_pos[0]+3,panel1_pos[1]+padding]

######Liputus
    date_events = liputukset
    
    # Convert date strings to datetime objects
    date_objects = {datetime.strptime(date, "%d.%m.%Y"): event for date, event in date_events.items()}

    next_matching_date = get_next_matching_date(date_objects,current_date)
    flagContent = "Odottaa uusia liputusvuoroja (kontaktoi Virtanen)"
    next_matching_formatted_date = ""
    flagEventApartment = ""
    if next_matching_date:
        next_matching_formatted_date = next_matching_date.strftime('%d.%m.%Y')
        matching_event = date_objects[next_matching_date]
        flagContent = f"Seuraava liputusvuoro {next_matching_formatted_date}"
        flagEventApartment = matching_event.split(' #')
        #convert back to datetime
        next_matching_formatted_date = datetime.strptime(next_matching_formatted_date, '%d.%m.%Y')

    next_matching_date2 = get_next_matching_date(date_objects,next_matching_formatted_date)
    flagContentNext = ":("
    flagEventApartmentNext = ""
    if next_matching_date2:
        next_matching_formatted_date2 = next_matching_date2.strftime('%d.%m.%Y')
        matching_event = date_objects[next_matching_date2]
        flagContentNext = f"Tuleva liputusvuoro {next_matching_formatted_date2}"
        flagEventApartmentNext = matching_event.split(' #')[1]

    message = [
        flagContent,
        limit_string_length(flagEventApartment[0],30),
        " Asunto " + flagEventApartment[1] + " ",
        "",
        flagContentNext,
        "Asunto " + flagEventApartmentNext
    ]
    color_by_row = [1,1,3,1,1,1]
    if once[0]:
        write_text(stdscr, message, start_pos[0], start_pos[1], 1, 3, color_by_row)

#####nurmikko
    panel1_pos = [y+2, padding] #nää menee y,x suuntaisesti
    createPanel(stdscr,width, 3, "Nurmikon ajovuoro",panel1_pos)

    start_pos = [panel1_pos[0]+3,panel1_pos[1]+padding]
    grass = "Ei vuoroja"
    content = nurmikko.get(str(week_number))
    if content:
        grass = "Asunto " + content
    
    grassNext = "Ei vuoroja"
    contentNext = nurmikko.get(str(week_number+1))
    if contentNext:
        grassNext = "Asunto " + contentNext
    
    message = [
        "Viikko " + str(week_number) + ": ",
        grass,
        "",
        "Tulossa seuraavalla viikolla",
        grassNext
    ]
    if once[0]:
        write_text(stdscr, message, start_pos[0], start_pos[1], repeat=1, color_pair=1)

    once = False
    #stdscr.getch()  # Wait for user input


def main(stdscr):
    # Run an update loop
    loop = 0
    once = [True]
    while True:
        loop += 1

        if loop == 1: #first time
            liputukset = readFile('liputus.json')
            nurmikko = readFile('nurmikko.json')

        if loop % 10 == 0: #every 10 times
            liputukset = readFile('liputus.json')
            nurmikko = readFile('nurmikko.json')

        program(stdscr,loop,once,liputukset,nurmikko)
        curses.delay_output(1000)

curses.wrapper(main)
