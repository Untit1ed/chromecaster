import math


class StringUtils:
    """
    A collection of utilities for working with strings.
    """

    @staticmethod
    def shorten_long_string(long_string: str, limit: int = 50, postfix: str = '...') -> str:
        """
        Shorten a long string by keeping the first and last `limit - len(postfix)/2` characters,
        and appending `postfix` in between.

        Args:
            long_string (str): The long string to be shortened.
            limit (int): The maximum length of the string.
            postfix (str): The string to append between the beginning and end of the shortened string.

        Returns:
            str: The shortened string.

        Example:
            StringUtils.shorten_long_string("This is a very long string that needs to be shortened", limit=21)
            Output: "This is a...shortened"
        """
        if not long_string:
            return long_string

        if len(long_string) <= limit:
            return long_string

        limit = limit - len(postfix)

        return long_string[:math.floor(limit/2)].rstrip() + postfix + long_string[-math.floor(limit/2):]

    @staticmethod
    def make_link(url: str, label: str) -> str:
        '''
        Creates a clickable link with a custom label.

        Args:
            url (str): The URL to link to.
            label (str): The label to display for the link.

        Returns:
            str: The clickable link with the custom label.
        '''
        return '\033]8;;{url}\a{label}\033]8;;\a'.format(url=url, label=label)

    @staticmethod
    def get_percentage(current_time: float, duration: float) -> str:
        """
        Calculates the percentage of media playback completion based on the current time and duration, and returns
        the result as a formatted string.

        Args:
            current_time (float): The current time of the media playback in seconds.
            duration (float): The total duration of the media playback in seconds.

        Returns:
            str: The percentage of completion as a formatted string.
        """
        percentage = 0
        if not duration:
            percentage = 0
        elif current_time >= duration:
            percentage = 1
        else:
            percentage = round((current_time / duration), 2)

        return f"{percentage:.0%}"

    @staticmethod
    def progress_bar(current_time: float, duration: float, length: int = 20) -> str:
        """
        Displays a progress bar in the console based on the current time and duration of a media playback.

        Args:
            current_time (float): The current time of the media playback in seconds.
            duration (float): The total duration of the media playback in seconds.
            length (int): The length of the progress bar in characters. Default is 20.
        """
        percentage = StringUtils.get_percentage(current_time, duration)
        if duration:
            if duration < current_time:
                filled_length = length
            else:
                filled_length = int(length * current_time // duration)

            formatted_time = f"{StringUtils.format_seconds(current_time)} / {StringUtils.format_seconds(duration)}"
        else:
            filled_length = 0
            formatted_time = f"{StringUtils.format_seconds(current_time)} / unknown"



        progress_bar = '█' * filled_length + '-' * (length - filled_length)
        return f'|{progress_bar}| \
            {percentage} \
            {formatted_time}'

    @staticmethod
    def format_seconds(seconds: float) -> str:
        """
        Converts a floating-point number of seconds to an hh:mm:ss formatted string.

        Args:
            seconds: The number of seconds to format.

        Returns:
            A string representing the number of seconds in hh:mm:ss format.
        """

        if seconds is None:
            return ""

        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
