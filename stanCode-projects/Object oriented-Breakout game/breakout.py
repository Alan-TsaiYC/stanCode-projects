"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

Name: Alan Tsaiee
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000 / 120     # 120 frames per second
NUM_LIVES = 3			    # Number of attempts


def main():
    graphics = BreakoutGraphics()
    lives = NUM_LIVES

    while True:                                                         # main while loop
        pause(1)
        if lives == 0:                                                  # lost game condition
            print(f'game over! left brick:{graphics.brick_num}')
            break

        while graphics.is_running:                                      # while loop of running the ball
            pause(FRAME_RATE)
            graphics.ball.move(graphics.vx, graphics.vy)                # ball move per frame rate

            # lost lives
            if graphics.ball.y > graphics.window.height:                # when ball falls out of window, lives-1
                lives -= 1
                if lives > 0:                                           # when have lives, reset game
                    graphics.is_running = False
                break

            if graphics.brick_num == 0:
                graphics.is_running = False                             # win game condition
                print('Clear')
                break

            #  3 wall rebound
            if not 0 <= graphics.ball.x <= graphics.window.width-graphics.ball.width:
                graphics.vx *= -1
            if not 0 <= graphics.ball.y:
                graphics.vy *= -1

            # def up, down, left ,right 4 point of ball
            ball_u = graphics.window.get_object_at(graphics.ball.x+graphics.ball.width/2, graphics.ball.y-1)
            ball_d = graphics.window.get_object_at(
                graphics.ball.x+graphics.ball.width/2, graphics.ball.y+graphics.ball.height+1)
            ball_l = graphics.window.get_object_at(graphics.ball.x-1, graphics.ball.y+graphics.ball.height/2)
            ball_r = graphics.window.get_object_at(
                graphics.ball.x+graphics.ball.width+1, graphics.ball.y+graphics.ball.height/2)

            not_brick = [graphics.paddle, graphics.ball]                # not brick list (can't remove by ball touch)

            # check what point touch something then rebound, and if it's brick, remove it
            if ball_d is not None and graphics.vy > 0:                  # when ball move down and touch something
                graphics.vy *= -1                                       # y axis rebound
                if ball_d not in not_brick:
                    graphics.window.remove(ball_d)                      # remove brick which touched by ball
                    graphics.brick_num -= 1                             # brick_num -1
            elif ball_l is not None and graphics.vx < 0:
                graphics.vx *= -1
                if ball_l not in not_brick:
                    graphics.window.remove(ball_l)
                    graphics.brick_num -= 1
            elif ball_r is not None and graphics.vx > 0:
                graphics.vx *= -1
                if ball_r not in not_brick:
                    graphics.window.remove(ball_r)
                    graphics.brick_num -= 1
            elif ball_u is not None and graphics.vy < 0:
                graphics.vy *= -1
                if ball_u not in not_brick:
                    graphics.window.remove(ball_u)
                    graphics.brick_num -= 1

            # don't like below condition
            # ball_ul = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y)
            # ball_ur = graphics.window.get_object_at(graphics.ball.x+graphics.ball.width, graphics.ball.y)
            # ball_dl = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y+graphics.ball.height)
            # ball_dr = graphics.window.get_object_at(
            #     graphics.ball.x+graphics.ball.height, graphics.ball.y+graphics.ball.height)


if __name__ == '__main__':
    main()
