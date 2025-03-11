import unittest
from unittest.mock import patch, MagicMock
import os

class TestGmailScript(unittest.TestCase):
    
    @patch('googleapiclient.discovery.build')
    def test_get_gmail_service(self, mock_build):
        # Mock the returned service
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        service = get_gmail_service()
        
        # Test if the build function was called
        mock_build.assert_called_with("gmail", "v1", credentials=None)
        self.assertEqual(service, mock_service)
    
    @patch('googleapiclient.discovery.build')
    def test_get_unread_emails(self, mock_build):
        # Mock Gmail API response
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Mock the API call response
        mock_service.users().messages().list.return_value.execute.return_value = {
            "messages": [{"id": "msg1"}, {"id": "msg2"}]
        }
        
        # Call the function
        messages = get_unread_emails(mock_service)
        
        # Test if the API was called with correct parameters
        mock_service.users().messages().list.assert_called_with(userId="me", labelIds=["UNREAD"])
        self.assertEqual(len(messages), 2)
    
    @patch('googleapiclient.discovery.build')
    def test_extract_attachments(self, mock_build):
        # Mock Gmail API response for email parts
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_email = {
            "id": "msg1",
            "payload": {
                "parts": [
                    {"filename": "test.pdf", "mimeType": "application/pdf", "body": {"attachmentId": "att1"}}
                ]
            }
        }
        # Mock the attachment content
        attachment_data = {
            "data": base64.urlsafe_b64encode(b"test content").decode('utf-8')
        }
        mock_service.users().messages().attachments().get.return_value.execute.return_value = attachment_data
        
        # Test if the function downloads and saves the attachment
        file_path = extract_attachments(mock_service, mock_email, "attachments")
        self.assertTrue(os.path.exists(file_path))  # Check if file was saved
        os.remove(file_path)  # Clean up
    
    @patch('pdfplumber.open')
    def test_extract_text_from_pdf(self, mock_pdfplumber):
        # Mock PDF plumper to return fake text
        mock_pdf = MagicMock()
        mock_pdfplumber.return_value = mock_pdf
        mock_pdf.pages = [MagicMock(extract_text=MagicMock(return_value="Fake text"))]
        
        text = extract_text_from_pdf("test.pdf")
        
        self.assertIn("Fake text", text)


if __name__ == '__main__':
    unittest.main()
