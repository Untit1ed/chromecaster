import itertools
import sys
import time
from threading import Event, Thread


class SpinnerUtil:
    """
    A utility for displaying a spinner animation in the command line.
    """

    __instance = None

    @staticmethod
    def get_instance():
        """
        Gets a singleton instance
        """
        if SpinnerUtil.__instance is None:
            SpinnerUtil()
        return SpinnerUtil.__instance

    def __init__(self):
        if SpinnerUtil.__instance is not None:
            raise Exception("Singleton class, use get_instance() method instead.")

        SpinnerUtil.__instance = self
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.stop_event = Event()

    def spin(self):
        """
        Displays a spinner animation in the command line until the stop method is called.

        The animation consists of a sequence of characters that simulate a spinner.
        This method uses itertools.cycle to cycle through a list of characters,
        and sys.stdout.write and sys.stdout.flush to display the characters in the
        command line. The animation runs indefinitely until the stop method is called.

        Returns:
            None
        """

        while not self.stop_event.is_set():
            sys.stdout.write(next(self.spinner))
            sys.stdout.write('\b')
            sys.stdout.flush()
            time.sleep(0.1)


    @staticmethod
    def start():
        """
        Starts the spinner animation in a background thread.

        Returns:
            None
        """
        instance = SpinnerUtil.get_instance()
        instance.stop_event.clear()
        Thread(target=instance.spin, daemon=True).start()

    @staticmethod
    def stop():
        """
        Stops the spinner animation.

        This method sets the stop_event attribute, which stops the spinner animation
        from running in the spin method.

        Returns:
            None
        """
        instance = SpinnerUtil.get_instance()
        instance.stop_event.set()
        sys.stdout.write(' ')
