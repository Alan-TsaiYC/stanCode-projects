"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

Draw line chart to show the trend of searched child names.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]        # the year list[int]
GRAPH_MARGIN_SIZE = 20                                                                  # size of space around canvas
COLORS = ['red', 'purple', 'green', 'blue']                                             # color list
TEXT_DX = 2                                                                             # space of y line to text
LINE_WIDTH = 2                                                                          # width of polyline
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    pitch = (width-2*GRAPH_MARGIN_SIZE)/len(YEARS)          # Calculate equal blank spacing
    x_coordinate = GRAPH_MARGIN_SIZE + year_index*pitch     # set x coordinate by year index
    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Write your code below this line
    #################################
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE,                                # the line of y' max
                       CANVAS_WIDTH-GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,                # the line of y's min
                       CANVAS_WIDTH - GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE)
    # draw line with equal space by year
    for i in range(len(YEARS)):
        x = get_x_coordinate(CANVAS_WIDTH, i)                                               # get x by year index
        canvas.create_line(x, 0, x, CANVAS_HEIGHT)                                          # y line
        canvas.create_text(x, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, text=YEARS[i], anchor=tkinter.NW)    # year text


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # Write your code below this line
    #################################
    color_index = 0

    # loop by name
    for name in lookup_names:
        year_index, x0, y0 = 0, 0, 0                        # year index; x0,y0: the x,y coordinate of last year
        # loop by year
        for year in YEARS:
            x1 = get_x_coordinate(CANVAS_WIDTH, year_index)     # set x coordinate by year
            # check the name this year in rank or not
            if str(year) in name_data[name]:
                rank = name_data[name][str(year)]           # get rank
                # set y coordinate by rank
                y1 = GRAPH_MARGIN_SIZE+(CANVAS_HEIGHT-2*GRAPH_MARGIN_SIZE)/MAX_RANK*int(rank)
            else:
                rank = '*'                                  # if out or rank(1000), show '*' as rank
                y1 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE        # set y coordinate at y=0

            # create text
            canvas.create_text(x1+TEXT_DX, y1, text=f'{name} {rank}', fill=COLORS[color_index % 4], anchor=tkinter.SW)
            # draw line, don't draw at 1st year (2nd year will draw line from 1st to 2nd year)
            if year_index > 0:
                canvas.create_line(x0, y0, x1, y1, width=LINE_WIDTH, fill=COLORS[color_index % 4])

            x0, y0 = x1, y1                                 # before next year, set x,y coordinate to last coordinate
            year_index += 1                                 # count year index

        color_index += 1                                    # count color index


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
