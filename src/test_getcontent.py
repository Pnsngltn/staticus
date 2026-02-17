import unittest

from getcontent import extract_title


class TestGetContent(unittest.TestCase):
    def test_get_title(self):
        md = "# This is the title"
        title = extract_title(md)
        self.assertEqual(
            title,
            "This is the title",
        )

    def test_title_not_in_first_line(self):
        md = "This is just text\n# Yet this is a title"
        title = extract_title(md)
        self.assertEqual(
            title,
            "Yet this is a title",
        )

    def test_no_title(self):
        md = "This is text\nBut this is text too"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_no_single_hash(self):
        md = "This is text\n## And this is tricky"
        with self.assertRaises(Exception):
            extract_title(md)
