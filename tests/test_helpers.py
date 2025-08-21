import unittest
import tempfile
import os
from pathlib import Path
from zipfile import ZipFile
from helpers import get_files_from_zip, parse, load_colleagues


class TestGetFilesFromZip(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.zip_path = Path(self.tmpdir.name) / "test.zip"

    def tearDown(self):
        self.tmpdir.cleanup()

    def create_zip(self, files: dict[str, str]):
        with ZipFile(self.zip_path, "w") as zf:
            for filename, content in files.items():
                zf.writestr(filename, content)

    def test_returns_txt_files(self):
        files = {
            "email1.txt": "Hello World",
            "ignore.bin": "BINARY",
            "Colleagues.txt": "Manager: Alice (alice@example.com)"
        }
        self.create_zip(files)
        result = get_files_from_zip(str(self.zip_path))
        self.assertIn("email1.txt", result)
        self.assertIn("Colleagues.txt", result)
        self.assertNotIn("ignore.bin", result)
        self.assertEqual(result["email1.txt"], "Hello World")

    def test_invalid_path_returns_empty_dict(self):
        result = get_files_from_zip(str(self.zip_path.with_name("missing.zip")))
        self.assertEqual(result, {})

    def test_bad_zipfile(self):
        # Create a fake file instead of a real zip
        bad_path = self.zip_path
        with open(bad_path, "wb") as f:
            f.write(b"not a zip")
        result = get_files_from_zip(str(bad_path))
        # Should gracefully return {}
        self.assertEqual(result, {})


class TestLoadColleagues(unittest.TestCase):
    def test_parses_valid_lines(self):
        data = """Project Manager (PM): Alice Smith (alice@example.com)
Account Manager (AM): Bob Jones (bob@example.com)"""
        result = load_colleagues(data)
        self.assertIn("Alice Smith", result)
        self.assertEqual(result["Alice Smith"]["role"], "Project Manager (PM)")
        self.assertEqual(result["Alice Smith"]["email"], "alice@example.com")
        self.assertIn("Bob Jones", result)

    def test_ignores_invalid_lines(self):
        data = """Invalid line
Developer: Charlie"""
        result = load_colleagues(data)
        self.assertEqual(result, {})

    def test_handles_empty_input(self):
        result = load_colleagues("")
        self.assertEqual(result, {})


class TestParse(unittest.TestCase):
    def test_parse_emails_and_colleagues(self):
        txt_files = {
            "email1.txt": "Hello Alice",
            "email2.txt": "Hello Bob",
            "Colleagues.txt": "Manager: Alice Smith (alice@example.com)"
        }
        colleagues, emails = parse(txt_files)
        self.assertEqual(len(emails), 2)
        self.assertEqual(emails[0]["num"], "1")
        self.assertIn("Alice Smith", colleagues)
        self.assertEqual(colleagues["Alice Smith"]["email"], "alice@example.com")

    def test_parse_ignores_unexpected_files(self):
        txt_files = {
            "random.txt": "ignored",
            "email42.txt": "Conversation"
        }
        colleagues, emails = parse(txt_files)
        self.assertEqual(len(emails), 1)
        self.assertEqual(colleagues, {})


if __name__ == "__main__":
    unittest.main()
