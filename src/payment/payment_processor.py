# src/payment/payment_processor.py
import stripe
from typing import Dict, Any
import requests
import os
from dataclasses import dataclass

@dataclass
class PaymentConfig:
    stripe_public_key: str
    stripe_secret_key: str
    buymeacoffee_token: str
    patreon_client_id: str
    patreon_client_secret: str

class PaymentProcessor:
    def __init__(self, config: PaymentConfig):
        self.config = config
        stripe.api_key = self.config.stripe_secret_key

    def create_stripe_checkout_session(self, price_id: str) -> Dict[str, Any]:
        """
        Create a Stripe checkout session for one-time payments
        """
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://example.com/success',
                cancel_url='https://example.com/cancel',
            )
            return {'session_id': session.id, 'url': session.url}
        except stripe.error.StripeError as e:
            return {'error': str(e)}
    
    def create_stripe_subscription(self, price_id: str) -> Dict[str, Any]:
        """
        Create a Stripe subscription checkout session
        """
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url='http://localhost:8501/success',
                cancel_url='http://localhost:8501/cancel',
            )
            return {'session_id': session.id, 'url': session.url}
        except stripe.error.StripeError as e:
            return {'error': str(e)}
        
    def get_buymeacoffee_widget(self) -> str:
        """
        Generate Buy Me a Coffee widget HTML
        """
        return f"""
        <script data-name="BMC-Widget" 
                data-cfasync="false" 
                src="https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js" 
                data-id="{self.config.buymeacoffee_token}" 
                data-description="Support me on Buy me a coffee!" 
                data-message="Thank you for using EduVision!" 
                data-color="#5F7FFF" 
                data-position="right" 
                data-x_margin="18" 
                data-y_margin="18">
        </script>
        """

    def get_patreon_auth_url(self) -> str:
        """
        Generate Patreon OAuth URL
        """
        return f"https://www.patreon.com/oauth2/authorize?" + \
               f"client_id={self.config.patreon_client_id}&" + \
               "response_type=code&" + \
               "redirect_uri=http://localhost:8501/patreon_callback"
    
# Update EnhancedStreamlitApp class to include payment features
import streamlit as st
class PaymentUI:
    def __init__(self, payment_processor: PaymentProcessor):
        self.payment_processor = payment_processor
        
    def render_payment_section(self):
        """
        Render payment options in Streamlit
        """
        import streamlit as st
        
        st.markdown("## 💝 Support EduVision")
        st.markdown("Help us maintain and improve EduVision by supporting our work!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### One-time Support")
            if st.button("☕ Buy me a coffee"):
                st.markdown(
                    self.payment_processor.get_buymeacoffee_widget(),
                    unsafe_allow_html=True
                )
        
        with col2:
            st.markdown("### Monthly Support")
            if st.button("💳 Subscribe via Stripe"):
                result = self.payment_processor.create_stripe_subscription(
                    price_id='price_monthly_subscription_id'
                )
                if 'url' in result:
                    st.markdown(f"[Complete Subscription]({result['url']})")
                else:
                    st.error("Failed to create subscription")
        
        with col3:
            st.markdown("### Become a Patron")
            if st.button("🎭 Support on Patreon"):
                patreon_url = self.payment_processor.get_patreon_auth_url()
                st.markdown(f"[Connect with Patreon]({patreon_url})")