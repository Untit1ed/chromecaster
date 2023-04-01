import math
import re
from typing import Optional


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
        return f'\033]8;;{url}\a{label}\033]8;;\a'

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

    @staticmethod
    def find_url(text: str) -> str:
        """
        Finds the first URL in a string.

        Args:
            text (str): The input text to search for URLs.

        Returns:
            str: The first URL found in the text, or None if no URLs are found.
        """
        pattern = re.compile(r"(?P<url>https?://[^\s]+)")

        match = re.search(pattern, text)

        if match:
            return match.group("url")

        return None

    @staticmethod
    def get_float(num_st:str) -> float:
        '''
        Check if float
        '''
        try:
            return float(num_st)
        except ValueError:
            return -1


    @staticmethod
    def time_str_to_seconds(time_str: str) -> Optional[int]:
        """
        Converts a time string in the format "NN:NN:NN" to an integer representing the total number of seconds.

        Args:
            time_str (str): A string representing a time in the format "NN:NN:NN".

        Returns:
            int: The number of seconds represented by the input time string.

        Example:
            >>> to_seconds("00:01:23")
            83
        """
        if not StringUtils.is_valid_time_format(time_str):
            return None

        time_parts = time_str.split(":")
        if len(time_parts) == 2:
            time_parts.insert(0, 0)

        hours, minutes, seconds = time_parts
        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)

    @staticmethod
    def is_valid_time_format(time_str:str) -> bool:
        """
        Determines whether a string is in the time format "NN:NN:NN"

        Args:
            time_str (str): A string representing a time.

        Returns:
            bool: True if the input string is in the correct format, False otherwise.
        """

        pattern = re.compile(r"^(([0-1]?[0-9]|2[0-3]):)?[0-5][0-9]:[0-5][0-9]$")
        return pattern.fullmatch(time_str) is not None

    @staticmethod
    def extract_number(string:str) -> float:
        """
        Extracts a number from a string if it follows a plus or minus sign.

        Args:
            string (str): The string to search for a number.

        Returns:
            float or None: The number following a plus or minus sign, or None if the string does not
            start with a plus or minus sign followed by a number.
        """

        pattern = re.compile(r'^[+-]\d+(\.\d+)?$')
        match = pattern.match(string)
        if match:
            return float(match.group(0))

        return None
