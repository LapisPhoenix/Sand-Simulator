import sys
import time
import pygame
from random import uniform, choice


class Color:
    """
    Helper Class to make colors easier to read
    """
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 127, 0)
    MAGENTA = (255, 0, 255)
    PURPLE = (127, 0, 127)

    @staticmethod
    def invert(color) -> tuple[int, int, int]:
        """
        Invert a given color
        :param color:
        :return:
        """
        return 255 - color[0], 255 - color[1], 255 - color[2]


class FallingSand:
    """
    Simple Falling Sand Simulator
    """
    def __init__(self):
        self.debug = True  # Default False
        self.WIDTH = 800
        self.HEIGHT = 800
        self.SIZE = 50
        self.TICKRATE = 30
        self._delta_time = 1 / self.TICKRATE
        self.running = True
        self.RADIUS = 5
        self.CELL_SIZE = min(self.WIDTH // self.SIZE, self.HEIGHT // self.SIZE)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.FPS = pygame.display.get_current_refresh_rate()
        self.clock = pygame.time.Clock()
        self.grid = self.generate_grid()

        pygame.display.set_caption("Falling Sand - q to quit, r or c to clear")
        pygame.mixer.init()

        self.click = pygame.mixer.Sound("./resources/sounds/piano.mp3")
        self.click.set_volume(0.5)

    def generate_grid(self):
        """
        Generates a 2d array, auto populates each cell to 0 (Empty).
        :return:
        """
        grid = []
        for _ in range(self.SIZE):
            grid.append([0] * self.SIZE)
        return grid

    def handle_events(self):
        """
        Handles events
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_r, pygame.K_c):  # Reset Grid
                    self.grid = self.generate_grid()

                    if pygame.mixer.get_busy():
                        pygame.mixer.stop()
                    self.click.play()
                elif event.key == pygame.K_q:  # Quit
                    self.running = False

    def draw_grid(self):
        """
        Draws each cell in the grid
        :return:
        """
        for row in range(self.SIZE):
            for column in range(self.SIZE):
                color = Color.WHITE if self.grid[row][column] == 1 else Color.BLACK  # Control the color of the cell

                pygame.draw.rect(self.screen, color,
                                 (column * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

    def within_rows(self, row):
        """
        Helper Method to check if a given integer is within the row length
        :param row:
        :return:
        """
        return 0 <= row <= self.SIZE - 1

    def within_cols(self, cols):
        """
        Helper Method to check if a given integer is within the col length
        :param cols:
        :return:
        """
        return 0 <= cols <= self.SIZE - 1

    def handle_drag(self, next_grid):
        """
        Handles when the user click and drags the mouse to draw sand
        :param next_grid:
        :return:
        """
        mx, my = pygame.mouse.get_pos()
        mxr, myc = mx // self.CELL_SIZE, my // self.CELL_SIZE

        extent = self.RADIUS // 2

        for row in range(extent):
            for column in range(extent):
                if round(uniform(0, 1), 2) < 0.75:  # 75% Change
                    r = mxr + row
                    c = myc + column
                    if self.within_cols(c) and self.within_rows(r):
                        next_grid[c][r] = 1

    def update_grid(self):
        """
        Updates the grid, triggers each tick
        :return:
        """
        next_grid = self.generate_grid()

        if pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                self.handle_drag(next_grid)

        for row in range(self.SIZE):
            for col in range(self.SIZE):
                cell = self.grid[row][col]
                below = row + 1

                if cell != 1:  # Cell is empty
                    continue

                if self.within_rows(below) and self.grid[below][col] == 0:
                    next_grid[below][col] = 1
                    continue

                # Attempt to move left or right

                dir = choice((-1, 1))

                new_col = col + dir

                if self.within_cols(new_col) and self.within_rows(below) and self.grid[below][new_col] == 0:
                    next_grid[below][new_col] = 1
                    continue

                next_grid[row][col] = cell

        self.grid = next_grid

    def draw(self):
        """
        Draw the grid to the screen
        :return:
        """
        self.screen.fill(Color.BLACK)
        self.draw_grid()
        pygame.display.flip()

    def shutdown(self):
        """
        Handle Shutdown and Clean up
        :return:
        """
        pygame.quit()
        sys.exit()

    def run(self):
        """
        Runs the Sand Simulator
        :return:
        """
        last_update_time = time.time()

        while self.running:
            self.handle_events()

            if not self.running:
                self.shutdown()

            current_time = time.time()
            elapsed_time = current_time - last_update_time

            while elapsed_time >= self._delta_time:     # Tick the "engine"
                self.update_grid()
                elapsed_time -= self._delta_time
                last_update_time += self._delta_time

            self.draw()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    game = FallingSand()
    game.run()
