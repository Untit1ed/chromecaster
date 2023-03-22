import unittest

from utils.string_utils import StringUtils


class TestStringUtils(unittest.TestCase):
    """Test cases for the StringUtils class"""

    def test_shorten_long_string(self):
        """Test the shorten_long_string method"""

        self.assertEqual(
            StringUtils.shorten_long_string(
                "This is a very long string that needs to be shortened",
                limit=15),
            "This i...rtened")
        self.assertEqual(StringUtils.shorten_long_string(
               "This is a short string",
               limit=22),
            "This is a short string")

        self.assertEqual(StringUtils.shorten_long_string(
            "This is a short string",
            limit=20),
            "This is...t string")
        self.assertEqual(StringUtils.shorten_long_string("", limit=10), "")

    def test_make_link(self):
        """Test the make_link method"""

        self.assertEqual(StringUtils.make_link("https://example.com", "Example"),
                         "\033]8;;https://example.com\aExample\033]8;;\a")
        self.assertEqual(StringUtils.make_link("", ""), "\033]8;;\a\033]8;;\a")

    def test_get_percentage(self):
        """Test the get_percentage method"""

        self.assertEqual(StringUtils.get_percentage(50, 100), "50%")
        self.assertEqual(StringUtils.get_percentage(101, 200), "51%")
        self.assertEqual(StringUtils.get_percentage(0, 0), "0%")
        self.assertEqual(StringUtils.get_percentage(0, None), "0%")
        self.assertEqual(StringUtils.get_percentage(100, 100), "100%")
        self.assertEqual(StringUtils.get_percentage(300, 100), "100%")

    def test_format_seconds(self):
        """Test the format_seconds method"""

        self.assertEqual(StringUtils.format_seconds(60), "00:01:00")
        self.assertEqual(StringUtils.format_seconds(3600), "01:00:00")
        self.assertEqual(StringUtils.format_seconds(None), "")

    def test_progress_bar(self):
        """Test the progress_bar method"""

        self.assertEqual(StringUtils.progress_bar(60, None, 10),
                         '|----------|             0%             00:01:00 / unknown')

        self.assertEqual(StringUtils.progress_bar(30, 60, 10),
                         '|█████-----|             50%             00:00:30 / 00:01:00')

        self.assertEqual(StringUtils.progress_bar(60, 60, 10),
                         '|██████████|             100%             00:01:00 / 00:01:00')


if __name__ == '__main__':
    unittest.main()
