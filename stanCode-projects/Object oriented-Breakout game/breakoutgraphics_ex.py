"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

Name: Alan Tsai
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
Ball_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 5    # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:

    def __init__(self, ball_radius = Ball_RADIUS, paddle_width = PADDLE_WIDTH,
                 paddle_height = PADDLE_HEIGHT, paddle_offset = PADDLE_OFFSET,
                 brick_rows = BRICK_ROWS, brick_cols = BRICK_COLS,
                 brick_width = BRICK_WIDTH, brick_height = BRICK_HEIGHT,
                 brick_offset = BRICK_OFFSET, brick_spacing = BRICK_SPACING,
                 title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled, self.paddle.fill_color, self.paddle.color = True, 'black', 'black'
        self.window.add(self.paddle, x=(self.window.width-self.paddle.width)/2,
                        y=self.window.height-paddle_offset)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius * 2, ball_radius * 2)
        self.ball.filled, self.ball.fill_color, self.ball.color = True, 'black', 'black'
        self.window.add(self.ball, x=self.window.width / 2 - ball_radius, y=self.window.height / 2 - ball_radius)

        # Default initial velocity for the ball
        self.__dy = - INITIAL_Y_SPEED
        self.__dx = random.randint(1, MAX_X_SPEED)      # random vx
        if random.random() > 0.5:                       # random vy +/-
            self.__dx = - self.__dx
        self.vx = self.__dx                             # def Getter of vx and vy
        self.vy = self.__dy

        # Initialize our mouse listeners
        self.is_running = False                         # to know is gaming or not, default is False
        self.click_obj = ''
        onmouseclicked(self.click_start)                # when click, do something (ex:start game)
        onmousemoved(self.move_mouse)                   # let paddle follow mouse move

        # Draw bricks
        self.__brick_num = 0                            # count brick num
        self.color = ['red', 'orange', 'yellow', 'green', 'blue']   # define color list
        for y in range(brick_rows):
            for x in range(brick_cols):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled, self.brick.fill_color, self.brick.color = True, self.color[y // 2], 'black'
                self.window.add(self.brick, x=x * (brick_width + brick_spacing),
                                y=y * (brick_height + brick_spacing) + brick_offset)
                self.__brick_num += 1
        self.brick_num = self.__brick_num               # getter: brick num

        # ex function need
        self.brick_rows, self.brick_cols, self.brick_spacing = brick_rows, brick_cols, brick_spacing
        self.score, self.lives = 0, 0
        self.score_board = GLabel(f'Score:{self.score}', x=10, y=self.window.height-10)
        self.lives_board = GLabel(f'lives:  ')
        # score_board
        self.window.add(self.score_board)
        self.window.add(self.lives_board, x=self.window.width-self.lives_board.width-10, y=self.window.height-10)
        # game over and game win label
        self.game_over, self.game_win = GLabel('Game Over'), GLabel('You Win')
        self.game_over.font, self.game_win.font = f'-{str(int(self.window.width/5))}', self.game_over.font
        # bonus function
        self.bonus_ball, self.bonus_ball.filled = GOval(ball_radius, ball_radius, y=self.window.height+1), True
        self.window.add(self.bonus_ball)
        self.bonus_color = ''                           # to know what color of bonus ball now
        self.bonus_time = 0                             # to check bonus state
        self.bonus_score = 1                            # to count bonus score

    def click_start(self, m):
        if self.is_running is False:                    # when not running, click to start running
            self.ball.x = self.paddle.x+(self.paddle.width-self.ball.width)/2   # refresh ball's position before start
            self.ball.y = self.paddle.y-self.ball.height-1
            self.is_running = True
            self.click_obj = self.window.get_object_at(m.x, m.y)

    def move_mouse(self, m):
        if self.paddle.width/2 >= m.x:                  # let paddle follow mouse and in window
            self.paddle.x = 0
        elif m.x >= self.window.width-self.paddle.width/2:
            self.paddle.x = self.window.width-self.paddle.width
        else:
            self.paddle.x = m.x-self.paddle.width/2

        if self.is_running is False:                    # when not running, let ball follow paddle
            self.ball.x = self.paddle.x+(self.paddle.width-self.ball.width)/2
            self.ball.y = self.paddle.y-self.ball.height-1
