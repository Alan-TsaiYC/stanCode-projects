"""
File: sierpinski.py
Name: Alan Tsai
---------------------------
This file recursively prints the Sierpinski triangle on GWindow.
The Sierpinski triangle is a fractal described in 1915 by Waclaw Sierpinski.
It is a self similar structure that occurs at different levels of iterations.
"""

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GLine
from campy.gui.events.timer import pause

# Constants
ORDER = 6                  # Controls the order of Sierpinski Triangle
LENGTH = 600               # The length of order 1 Sierpinski Triangle
UPPER_LEFT_X = 150		   # The upper left x coordinate of order 1 Sierpinski Triangle
UPPER_LEFT_Y = 100         # The upper left y coordinate of order 1 Sierpinski Triangle
WINDOW_WIDTH = 950         # The width of the GWindow
WINDOW_HEIGHT = 700        # The height of the GWindow
PAUSE = 0			   	   # The time want to pause

# Global Variable
window = GWindow(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)  # The canvas to draw Sierpinski Triangle


def main():
	"""
	Draw a order:{ORDER}'s Sierpinski Triangle
	"""
	sierpinski_triangle(ORDER, LENGTH, UPPER_LEFT_X, UPPER_LEFT_Y)


def sierpinski_triangle(order, length, upper_left_x, upper_left_y):
	"""
	:param order: int, the level of triangle
	:param length: int, length of line, half in next level
	:param upper_left_x: int, horizontal line's x position coordinate
	:param upper_left_y: int, horizontal line's y position coordinate
	:return: none, refresh window graph
	"""
	# Base Case
	if order == 0:
		return
	else:
		# Draw horizontal line
		l1 = GLine(upper_left_x, upper_left_y, upper_left_x+length, upper_left_y)
		window.add(l1)
		sierpinski_triangle(order-1, length/2, upper_left_x+1/4*length, upper_left_y+0.866/2*length)		# recursion
		pause(PAUSE)

		# Draw left line
		l2 = GLine(upper_left_x, upper_left_y, upper_left_x+1/2*length, upper_left_y+0.866*length)
		window.add(l2)
		sierpinski_triangle(order-1, length/2, upper_left_x+1/2*length, upper_left_y)						# recursion
		pause(PAUSE)

		# Draw right line
		l3 = GLine(upper_left_x+length, upper_left_y, upper_left_x+1/2*length, upper_left_y+0.866*length)
		window.add(l3)
		sierpinski_triangle(order-1, length/2, upper_left_x, upper_left_y)									# recursion
		pause(PAUSE)


if __name__ == '__main__':
	main()
