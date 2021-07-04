"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

Name: Alan Tsai
"""

from campy.gui.events.timer import pause
from breakoutgraphics_ex import BreakoutGraphics

# ex import
import random


FRAME_RATE = 1000 / 120     # 120 frames per second
NUM_LIVES = 2			    # Number of attempts

g = BreakoutGraphics(brick_cols=3)


def main():

    g.lives = NUM_LIVES                                                 # save lives to g.lives
    g.lives_board.text = f'Lives: {g.lives}'                            # update lives board

    while True:                                                         # main while loop
        pause(FRAME_RATE)
        if g.lives == 0:                                                # lost game condition
            print(f'game over! left brick:{g.brick_num}')
            game_over()
            break

        if g.brick_num == 0:                                            # Win game condition
            g.window.remove(g.bonus_ball)
            game_win()
            break

        # run the ball and count lives
        running_ball()


def running_ball():

    not_brick = [g.paddle, g.ball, g.score_board, g.lives_board, g.bonus_ball]      # not brick list
    no_rebound = [None, g.score_board, g.lives_board, g.bonus_ball]                 # no bound list
    g.bonus_time = 0                                                                # to check bonus state

    while g.is_running:                                     # while loop of running the ball

        pause(FRAME_RATE)                                   # frame rate

        if g.bonus_time > 0 and g.bonus_color == 'green':   # while bonus, do something else
            g.ball.move(g.vx*0.5, g.vy*0.5)                 # green bonus, slower ball
        elif g.bonus_time > 0 and g.bonus_color == 'red':
            g.ball.move(g.vx*2, g.vy*2)                     # red bonus, faster ball
        else:
            g.ball.move(g.vx, g.vy)                         # normal, ball move per frame rate

        g.bonus_ball.move(0, 2)                             # bonus ball fall down v

        # lost lives
        if g.ball.y > g.window.height:                      # when ball falls out of window, lives-1
            g.lives -= 1
            g.lives_board.text = f'Lives:{g.lives}'         # update score
            g.window.remove(g.bonus_ball)
            g.is_running = False                            # update game state
            break

        # win game
        if g.brick_num == 0:                                # win game condition
            g.is_running = False                            # update game state
            break

        #  3 wall rebound
        if not 0 <= g.ball.x <= g.window.width - g.ball.width:
            g.vx *= -1
        if not 0 <= g.ball.y:
            g.vy *= -1

        # def up, down, left ,right 4 point of ball, and get what touched or not
        ball_u = g.window.get_object_at(g.ball.x + g.ball.width / 2, g.ball.y - 1)
        ball_d = g.window.get_object_at(
            g.ball.x + g.ball.width / 2, g.ball.y + g.ball.height + 1)
        ball_l = g.window.get_object_at(g.ball.x - 1, g.ball.y + g.ball.height / 2)
        ball_r = g.window.get_object_at(
            g.ball.x + g.ball.width + 1, g.ball.y + g.ball.height / 2)

        # check what point touched then rebound, if it's brick, remove it
        if ball_d not in no_rebound and g.vy > 0:   # when ball move down and touch something
            g.vy *= -1                              # y axis rebound
            if ball_d not in not_brick:
                eliminate(ball_d)                   # eliminate point and count brick num & score
        elif ball_l not in no_rebound and g.vx < 0:
            g.vx *= -1
            if ball_l not in not_brick:
                eliminate(ball_l)
        elif ball_r not in no_rebound and g.vx > 0:
            g.vx *= -1
            if ball_r not in not_brick:
                eliminate(ball_r)
        elif ball_u not in no_rebound and g.vy < 0:
            g.vy *= -1
            if ball_u not in not_brick:
                eliminate(ball_u)

        # bonus ball
        bonus_ball_d = g.window.get_object_at(                  # get what bonus ball's down point touched
            g.bonus_ball.x+g.bonus_ball.width/2, g.bonus_ball.y+g.bonus_ball.height+1)
        if bonus_ball_d is g.paddle:                            # when paddle get bonus ball
            if g.bonus_color == 'black':                        # black bonus, lives +1
                g.lives += 1
                g.lives_board.text = f'Lives:{g.lives}'
            elif g.bonus_color == 'red':                        # red bonus, more score but move faster
                g.bonus_score = 2
            elif g.bonus_color == 'yellow':                     # yellow bonus, add score
                g.score += 50
                g.score_board.text = f'Score:{g.score}'
            g.ball.fill_color = g.bonus_ball.fill_color
            g.bonus_time = 3*1000/FRAME_RATE
            g.bonus_ball.y += 100                               # fall out of window

        g.bonus_time -= 1                                       # subtract bonus time
        if g.bonus_time <= 0:                                   # when no bonus time, reset bonus state
            g.ball.fill_color = 'black'
            g.bonus_score = 1


def eliminate(point):
    """
    :param point: GObject, which need to eliminate, must check before function.
    """
    g.window.remove(point)                                              # eliminate
    if random.random() < 0.3 and g.bonus_ball.y > g.window.height:      # bonus Trigger conditions
        color = random.choice(['black', 'red', 'green', 'yellow'])      # random bonus color
        g.bonus_color, g.bonus_ball.fill_color = color, color
        g.window.add(g.bonus_ball, point.x+g.ball.width/2, point.y)
    g.brick_num -= 1                                                    # count left brick
    g.score += 10 * g.bonus_score                                       # Scoring
    g.score_board.text = f'Score:{g.score}'                             # update score board


def menu():
    pass


def game_over():                                                        # game over animation
    for y in range(g.brick_rows):                                       # remove left brick by row
        for x in range(g.brick_cols):
            down_brick = g.window.get_object_at(
                x * (g.brick.width + g.brick_spacing),                  # find brick by row
                g.brick.y - y * (g.brick.height + g.brick_spacing))
            g.window.remove(down_brick)
        pause(100)
    g.window.add(g.game_over,                                           # add game over text
                 x=(g.window.width - g.game_over.width) / 2, y=g.window.height / 3)
    pause(500)
    g.score_board.font = g.game_over.font                               # Scale score board ,update and show
    g.window.add(g.score_board,
                 x=(g.window.width - g.score_board.width) / 2, y=g.window.height / 2)
    pause(1000)
    g.score = 0


def game_win():                                                         # game win animation
    g.window.add(g.game_win,
                 x=(g.window.width - g.game_win.width) / 2, y=g.window.height / 3)
    pause(500)
    g.score_board.font = g.game_win.font                                # Scale score board ,update and show
    g.window.add(g.score_board,
                 x=(g.window.width - g.score_board.width) / 2, y=g.window.height / 2)
    pause(500)
    g.score_board.text = f'Score:{g.score+(100*g.lives)}'               # add lives scores
    pause(1000)
    g.score = 0


if __name__ == '__main__':
    main()
