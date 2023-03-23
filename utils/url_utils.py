import re


class UrlUtils:
    """
    A utility class for working with URLs.
    """

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
