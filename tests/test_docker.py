
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class TestDockerConfiguration(unittest.TestCase):

    def test_dockerfile_exists(self):
        dockerfile = PROJECT_ROOT / "Dockerfile"
        self.assertTrue(
            dockerfile.is_file(),
            "Dockerfile is missing",
        )

    def test_compose_file_exists(self):
        compose_file = PROJECT_ROOT / "compose.yaml"
        self.assertTrue(
            compose_file.is_file(),
            "compose.yaml is missing",
        )

    def test_dockerfile_has_python_base_image(self):
        dockerfile = PROJECT_ROOT / "Dockerfile"
        self.assertTrue(dockerfile.is_file())

        content = dockerfile.read_text(encoding="utf-8").lower()

        self.assertIn(
            "from python:",
            content,
            "Dockerfile should specify a Python base image",
        )

    def test_dockerfile_copies_project_files(self):
        dockerfile = PROJECT_ROOT / "Dockerfile"
        self.assertTrue(dockerfile.is_file())

        content = dockerfile.read_text(encoding="utf-8").lower()

        self.assertIn(
            "copy . .",
            content,
            "Dockerfile should copy project files",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
