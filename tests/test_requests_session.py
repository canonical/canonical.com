import unittest
from unittest.mock import patch, MagicMock
from webapp.requests_session import (
    get_requests_session,
    get_requests_session_with_retries,
)


class TestRequestsSession(unittest.TestCase):
    @patch("webapp.requests_session.talisker.requests.configure")
    @patch("webapp.requests_session.requests.Session")
    def test_get_requests_session(self, mock_session_class, mock_configure):
        """Test basic session creation and configuration"""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        result = get_requests_session()

        # Verify Session was created
        mock_session_class.assert_called_once()

        # Verify talisker configuration was applied
        mock_configure.assert_called_once_with(mock_session)

        # Verify the session is returned
        self.assertEqual(result, mock_session)

    @patch("webapp.requests_session.get_requests_session")
    @patch("webapp.requests_session.HTTPAdapter")
    @patch("webapp.requests_session.Retry")
    def test_get_requests_session_with_retries(
        self, mock_retry_class, mock_adapter_class, mock_get_session
    ):
        """Test session creation with retry configuration"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        mock_retry = MagicMock()
        mock_retry_class.return_value = mock_retry

        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter

        result = get_requests_session_with_retries()

        # Verify get_requests_session was called
        mock_get_session.assert_called_once()

        # Verify Retry was created with correct parameters
        mock_retry_class.assert_called_once_with(
            total=5,
            backoff_factor=1,
            backoff_max=5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PATCH", "PUT"],
        )

        # Verify HTTPAdapter was created with the retry strategy
        mock_adapter_class.assert_called_once_with(max_retries=mock_retry)

        # Verify adapters were mounted for http and https
        mock_session.mount.assert_any_call("https://", mock_adapter)
        mock_session.mount.assert_any_call("http://", mock_adapter)

        # Verify the session is returned
        self.assertEqual(result, mock_session)


if __name__ == "__main__":
    unittest.main()
