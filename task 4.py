import pygame
import time

def PID(current, set):
    dt = 1

    accuracy = 0.1
    error = accuracy

    max_iter = 100
    count_iter = 0

    Kp = 0.4
    Ki = 0.07
    Kd = 0.2

    integral_summary = 0
    previous_error = 0

    measurements = [current]
    errors = [set - current]

    while (abs(error) >= accuracy):

        if count_iter >= max_iter:
            break

        current_error = errors[-1]

        # Prop
        propotional = Kp * current_error

        # Integral
        integral_summary += current_error * dt
        integral_contribution = Ki * integral_summary

        # Diff
        differential = Kd * (current_error - previous_error) / dt

        # PID
        pid = propotional + integral_contribution + differential

        # write to measurements list
        measurements.append(measurements[-1] + pid)

        # error update
        error = set - measurements[-1]
        errors.append(error)

        previous_error = current_error

        count_iter += 1

    return measurements

class Robot:
    y = 0
    vy0 = 10
    vy = 0

    size_x = 10
    size_y = 10

    trace = []

    def move(self, y):
        self.y = y


robot = Robot()

screen_x = 500
screen_y = 500

pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))

pygame.font.init()
my_font = pygame.font.SysFont(None, 30)

done = False

set = 15

robot.trace = PID(robot.y, set)

draw_flight = True

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if draw_flight == True:
        for point in robot.trace:
            screen.fill(color=(25, 200, 10))

            pygame.draw.rect(surface=screen, color=(255, 25, 98), rect=pygame.Rect(250, screen_y - point * 10, 10, 10))

            text_y = f'y = {round(point, 3)}'

            text_surface_y = my_font.render(text_y, False, (255, 255, 255))
            screen.blit(text_surface_y, (0, 30))

            pygame.display.flip()

            time.sleep(0.2)

        draw_flight = False

    pygame.draw.rect(surface=screen, color=(255, 25, 98), rect=pygame.Rect(250, screen_y - robot.trace[-1] * 10, 10, 10))
    pygame.display.flip()

