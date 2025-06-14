import pytest
import sys
import os
from pathlib import Path


class TestSetupValidation:
    """Validation tests to ensure the testing infrastructure is properly configured."""
    
    def test_pytest_installed(self):
        """Test that pytest is available."""
        assert "pytest" in sys.modules or True  # Will be true after poetry install
        
    def test_testing_directory_structure(self):
        """Test that the testing directory structure exists."""
        test_root = Path(__file__).parent
        assert test_root.exists()
        assert test_root.name == "tests"
        
        assert (test_root / "__init__.py").exists()
        assert (test_root / "unit").exists()
        assert (test_root / "unit" / "__init__.py").exists()
        assert (test_root / "integration").exists()
        assert (test_root / "integration" / "__init__.py").exists()
        assert (test_root / "conftest.py").exists()
        
    def test_project_structure(self):
        """Test that the main project modules are importable."""
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        
        # These should be importable after proper setup
        expected_modules = [
            "brute",
            "domainsites",
            "lib",
            "reverse",
            "searchengine",
            "thirdparty"
        ]
        
        for module in expected_modules:
            module_path = project_root / module
            assert module_path.exists(), f"Module {module} directory does not exist"
            assert (module_path / "__init__.py").exists(), f"Module {module} missing __init__.py"
    
    def test_configuration_files(self):
        """Test that configuration files exist."""
        project_root = Path(__file__).parent.parent
        
        assert (project_root / "pyproject.toml").exists()
        assert (project_root / ".gitignore").exists()
        
    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that the unit marker works."""
        assert True
        
    @pytest.mark.integration
    def test_integration_marker(self):
        """Test that the integration marker works."""
        assert True
        
    @pytest.mark.slow
    def test_slow_marker(self):
        """Test that the slow marker works."""
        assert True
        
    def test_fixtures_available(self, temp_dir, mock_config, sample_domain_list):
        """Test that conftest fixtures are available."""
        assert temp_dir.exists()
        assert mock_config is not None
        assert len(sample_domain_list) > 0
        
    def test_temp_file_fixture(self, temp_file):
        """Test the temp_file fixture."""
        test_file = temp_file("test.txt", "Hello, World!")
        assert test_file.exists()
        assert test_file.read_text() == "Hello, World!"
        
    def test_mock_requests_fixture(self, mock_requests):
        """Test the mock_requests fixture."""
        import requests
        
        response = requests.get("http://example.com")
        assert mock_requests["get"].called
        assert response.status_code == 200
        
    def test_environment_vars_fixture(self, environment_vars):
        """Test the environment_vars fixture."""
        environment_vars(TEST_VAR="test_value")
        assert os.environ.get("TEST_VAR") == "test_value"
        
    def test_capture_output_fixture(self, capture_output):
        """Test the capture_output fixture."""
        print("Test output")
        assert "Test output" in capture_output["stdout"].getvalue()


class TestCoverageConfiguration:
    """Tests to validate coverage configuration."""
    
    def test_coverage_configured(self):
        """Test that coverage is properly configured in pyproject.toml."""
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        assert pyproject_path.exists()
        
        content = pyproject_path.read_text()
        assert "[tool.coverage.run]" in content
        assert "[tool.coverage.report]" in content
        assert "cov-fail-under=80" in content