import sys
import pygame


class Engine:
    def __init__(self, height, width, **kwargs):
        """
        :param height: height of window in pixels
        :param width:  width of window in pixels
        :param fps: frames per second to update
        """
        self.height = height
        self.width = width
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.update_queue = []
        self.clock = pygame.time.Clock()
        self.fps = kwargs.get('fps', 30)
        if not isinstance(self.fps, int):
            raise TypeError('fps must be an integer')

    def run(self):
        """
        Main loop
        Iterates over input events and calls :function:self.event: with the gathered event.
        Calls child classes methods for updating and drawing
        :return: None
        """
        while True:
            for event in pygame.event.get():
                self.event(event)

            self.update()
            self.draw()
            # TODO work on update queue so that we don't have to update the entire screen for minor changes
            pygame.display.flip()
            self.clock.tick(self.fps)

    def event(self, event):
        """
        Placeholder method for handling events
        Handled by child class
        :param event:
        :return: None
        """
        pass

    def draw(self):
        """
        Placeholder method for drawing contents on screen
        :return:
        """
        pass

    def update(self):
        """
        Placeholder method for updating what *should* be shown on screen
        :return:
        """
        pass

    @staticmethod
    def quit():
        """
        :return: None
        """
        pygame.quit()
        sys.exit(0)
