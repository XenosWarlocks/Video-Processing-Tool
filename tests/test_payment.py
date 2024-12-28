import unittest
from unittest.mock import patch, MagicMock
import stripe
from src.payment.payment_processor import PaymentProcessor, PaymentConfig, PaymentUI
import streamlit as st

# Mock Payment Configuration for testing
TEST_CONFIG = PaymentConfig(
    stripe_public_key="pk_test_123",
    stripe_secret_key="sk_test_123",
    buymeacoffee_token="test_bmc_token",
    patreon_client_id="test_patreon_id",
    patreon_client_secret="test_patreon_secret"
)

class TestPaymentProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = PaymentProcessor(TEST_CONFIG)

    @patch('stripe.checkout.Session.create')
    def test_create_stripe_checkout_session_success(self, mock_stripe_create):
        # Mock successful Stripe session creation
        mock_session = MagicMock(id="session_123", url="https://checkout.stripe.com/pay/session_123")
        mock_stripe_create.return_value = mock_session

        result = self.processor.create_stripe_checkout_session("price_123")

        self.assertEqual(result, {'session_id': "session_123", 'url': "https://checkout.stripe.com/pay/session_123"})
        mock_stripe_create.assert_called_once_with(
            payment_method_types=['card'],
            line_items=[{'price': 'price_123', 'quantity': 1}],
            mode='payment',
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel'
        )

    @patch('stripe.checkout.Session.create')
    def test_create_stripe_checkout_session_failure(self, mock_stripe_create):
        # Mock Stripe error
        mock_stripe_create.side_effect = stripe.error.StripeError("API Error")

        result = self.processor.create_stripe_checkout_session("price_123")

        self.assertEqual(result, {'error': "API Error"})

    @patch('stripe.checkout.Session.create')
    def test_create_stripe_subscription_success(self, mock_stripe_create):
        # Mock successful Stripe session creation
        mock_session = MagicMock(id="sub_123", url="https://checkout.stripe.com/pay/sub_123")
        mock_stripe_create.return_value = mock_session

        result = self.processor.create_stripe_subscription("price_monthly_123")

        self.assertEqual(result, {'session_id': "sub_123", 'url': "https://checkout.stripe.com/pay/sub_123"})
        mock_stripe_create.assert_called_once_with(
            payment_method_types=['card'],
            line_items=[{'price': 'price_monthly_123', 'quantity': 1}],
            mode='subscription',
            success_url='http://localhost:8501/success',
            cancel_url='http://localhost:8501/cancel'
        )

    @patch('stripe.checkout.Session.create')
    def test_create_stripe_subscription_failure(self, mock_stripe_create):
        # Mock Stripe error
        mock_stripe_create.side_effect = stripe.error.StripeError("Invalid Price ID")

        result = self.processor.create_stripe_subscription("price_monthly_invalid")

        self.assertEqual(result, {'error': "Invalid Price ID"})

    def test_get_buymeacoffee_widget(self):
        widget_html = self.processor.get_buymeacoffee_widget()
        self.assertIn("test_bmc_token", widget_html)
        self.assertIn("https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js", widget_html)

    def test_get_patreon_auth_url(self):
        auth_url = self.processor.get_patreon_auth_url()
        self.assertIn("test_patreon_id", auth_url)
        self.assertIn("https://www.patreon.com/oauth2/authorize", auth_url)

class TestPaymentUI(unittest.TestCase):
    def setUp(self):
        self.payment_processor = PaymentProcessor(TEST_CONFIG)
        self.payment_ui = PaymentUI(self.payment_processor)

    @patch('streamlit.markdown')
    @patch('streamlit.button')
    def test_create_custom_card(self, mock_button, mock_markdown):
        mock_button.return_value = True  # Simulate button click

        result = self.payment_ui.create_custom_card(
            "Test Card", "Test Description", "$99", "Click Me", "✅"
        )

        self.assertTrue(result)  # Check if button was clicked
        mock_markdown.assert_called()  # Check if markdown was rendered
        self.assertIn("Test Card", mock_markdown.call_args[0][0])
        self.assertIn("$99", mock_markdown.call_args[0][0])

    @patch('streamlit.markdown')
    @patch('streamlit.columns')
    @patch.object(PaymentUI, 'create_custom_card')
    def test_render_payment_section(self, mock_create_card, mock_columns, mock_markdown):
        # Mock column creation
        mock_columns.return_value = [MagicMock(), MagicMock(), MagicMock()]

        # Mock card creation (assuming buttons are not clicked)
        mock_create_card.return_value = False

        self.payment_ui.render_payment_section()

        mock_markdown.assert_called()  # Check if markdown was rendered
        mock_columns.assert_called_once_with(3)  # Check if 3 columns were created
        self.assertEqual(mock_create_card.call_count, 3)  # Check if 3 cards were created

if __name__ == '__main__':
    unittest.main() 