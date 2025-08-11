"""
CLI Command Extensions for Flask
"""
from unittest import TestCase
from unittest.mock import patch
from click.testing import CliRunner
from flask.cli import ScriptInfo
from service import app

class TestFlaskCLI(TestCase):
    """Test Flask CLI Commands"""

    def setUp(self):
        self.runner = CliRunner()

    @patch("service.models.db.create_all")
    def test_db_create(self, mock_create_all):
        """It should call the db-create command"""
        mock_create_all.return_value = None
        script_info = ScriptInfo(create_app=lambda: app)
        result = self.runner.invoke(app.cli.commands["db-create"], obj=script_info)
        print("CLI Output:\n", repr(result.output))  # 👈 Use repr to reveal hidden characters
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Database created", result.output)

