import pytest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import Mock, MagicMock


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def temp_file(temp_dir):
    """Create a temporary file for testing."""
    def _create_temp_file(filename="test.txt", content=""):
        file_path = temp_dir / filename
        file_path.write_text(content)
        return file_path
    return _create_temp_file


@pytest.fixture
def mock_config():
    """Mock configuration object."""
    config = Mock()
    config.output_dir = "/tmp/test_output"
    config.threads = 10
    config.timeout = 30
    config.debug = False
    config.verbose = False
    return config


@pytest.fixture
def mock_requests(monkeypatch):
    """Mock requests module."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><body>Test</body></html>"
    mock_response.json.return_value = {"test": "data"}
    mock_response.headers = {"Content-Type": "text/html"}
    
    mock_get = Mock(return_value=mock_response)
    mock_post = Mock(return_value=mock_response)
    
    monkeypatch.setattr("requests.get", mock_get)
    monkeypatch.setattr("requests.post", mock_post)
    
    return {
        "get": mock_get,
        "post": mock_post,
        "response": mock_response
    }


@pytest.fixture
def mock_dns_resolver(monkeypatch):
    """Mock DNS resolver."""
    mock_resolver = Mock()
    mock_answer = Mock()
    mock_answer.address = "192.168.1.1"
    mock_resolver.resolve.return_value = [mock_answer]
    
    return mock_resolver


@pytest.fixture
def sample_domain_list():
    """Provide sample domain list for testing."""
    return [
        "example.com",
        "test.example.com",
        "subdomain.example.com",
        "api.example.com",
        "www.example.com"
    ]


@pytest.fixture
def sample_ip_list():
    """Provide sample IP list for testing."""
    return [
        "192.168.1.1",
        "10.0.0.1",
        "172.16.0.1",
        "8.8.8.8",
        "1.1.1.1"
    ]


@pytest.fixture
def mock_logger(monkeypatch):
    """Mock logger for testing."""
    logger = Mock()
    logger.info = Mock()
    logger.error = Mock()
    logger.warning = Mock()
    logger.debug = Mock()
    logger.critical = Mock()
    
    return logger


@pytest.fixture
def mock_file_system(monkeypatch):
    """Mock file system operations."""
    mock_open_func = Mock()
    mock_file = MagicMock()
    mock_file.__enter__.return_value = mock_file
    mock_file.__exit__.return_value = None
    mock_file.read.return_value = "test content"
    mock_file.readlines.return_value = ["line1\n", "line2\n"]
    mock_open_func.return_value = mock_file
    
    monkeypatch.setattr("builtins.open", mock_open_func)
    
    return {
        "open": mock_open_func,
        "file": mock_file
    }


@pytest.fixture
def environment_vars(monkeypatch):
    """Set up and clean up environment variables for testing."""
    original_env = os.environ.copy()
    
    def _set_env(**kwargs):
        for key, value in kwargs.items():
            monkeypatch.setenv(key, value)
    
    yield _set_env
    
    # Cleanup is handled by monkeypatch automatically


@pytest.fixture
def mock_subprocess(monkeypatch):
    """Mock subprocess calls."""
    mock_result = Mock()
    mock_result.stdout = "command output"
    mock_result.stderr = ""
    mock_result.returncode = 0
    
    mock_run = Mock(return_value=mock_result)
    monkeypatch.setattr("subprocess.run", mock_run)
    
    return {
        "run": mock_run,
        "result": mock_result
    }


@pytest.fixture(autouse=True)
def reset_singleton_instances():
    """Reset singleton instances between tests."""
    # This is a placeholder for any singleton patterns in the codebase
    # Add any singleton reset logic here if needed
    yield


@pytest.fixture
def capture_output():
    """Capture stdout and stderr for testing."""
    import io
    import sys
    
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    
    sys.stdout = stdout_capture
    sys.stderr = stderr_capture
    
    yield {
        "stdout": stdout_capture,
        "stderr": stderr_capture
    }
    
    sys.stdout = old_stdout
    sys.stderr = old_stderr


@pytest.fixture
def mock_time(monkeypatch):
    """Mock time-related functions."""
    current_time = 1234567890.0
    
    def _time():
        return current_time
    
    def _sleep(seconds):
        nonlocal current_time
        current_time += seconds
    
    monkeypatch.setattr("time.time", _time)
    monkeypatch.setattr("time.sleep", _sleep)
    
    return {
        "time": _time,
        "sleep": _sleep,
        "set_time": lambda t: globals().update(current_time=t)
    }