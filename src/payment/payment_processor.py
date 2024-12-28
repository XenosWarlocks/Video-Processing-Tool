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
    
##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
import streamlit as st
class PaymentUI:
    def __init__(self, payment_processor: PaymentProcessor):
        self.payment_processor = payment_processor

    def create_custom_card(self, title, description, price, button_text, icon):
        """Create a styled card with hover effects"""
        st.markdown(
            f"""
            <div style="
                padding: 1.5rem;
                border-radius: 10px;
                background: linear-gradient(145deg, #ffffff, #f0f2f6);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s;
                height: 100%;
                cursor: pointer;
                :hover {{
                    transform: translateY(-5px);
                }}
            ">
                <div style="font-size: 2rem; margin-bottom: 1rem; text-align: center;">{icon}</div>
                <h3 style="text-align: center; color: #1f1f1f; margin-bottom: 0.5rem;">{title}</h3>
                <p style="color: #666; text-align: center; margin-bottom: 1rem;">{description}</p>
                <div style="text-align: center; font-size: 1.5rem; font-weight: bold; color: #1f1f1f; margin-bottom: 1rem;">
                    {price}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return st.button(button_text, key=f"btn_{title.lower().replace(' ', '_')}")

    def render_payment_section(self):
        """Enhanced payment section with modern UI elements"""
        st.markdown(
            """
            <div style="text-align: center; padding: 2rem 0;">
                <h1 style="color: #1f1f1f; font-size: 2.5rem;">Support EduVision 💝</h1>
                <p style="color: #666; font-size: 1.2rem; max-width: 600px; margin: 1rem auto;">
                    Help us continue developing AI-powered educational tools and make learning more 
                    accessible for everyone.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Custom CSS for container
        st.markdown(
            """
            <style>
            .stButton button {
                width: 100%;
                background-color: #FF4B4B;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            .stButton button:hover {
                background-color: #FF3333;
                transform: translateY(-2px);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Create three columns for payment options
        col1, col2, col3 = st.columns(3)

        with col1:
            if self.create_custom_card(
                "Coffee Support",
                "Buy us a coffee to fuel our development",
                "$5",
                "☕ Buy a Coffee",
                "☕"
            ):
                st.markdown(
                    self.payment_processor.get_buymeacoffee_widget(),
                    unsafe_allow_html=True
                )

        with col2:
            if self.create_custom_card(
                "Monthly Partner",
                "Become a monthly supporter with exclusive benefits",
                "$10/month",
                "💳 Subscribe",
                "🌟"
            ):
                result = self.payment_processor.create_stripe_subscription(
                    price_id='price_monthly_subscription_id'
                )
                if 'url' in result:
                    st.markdown(
                        f"""
                        <a href="{result['url']}" target="_blank" style="
                            display: inline-block;
                            padding: 0.5rem 1rem;
                            background-color: #FF4B4B;
                            color: white;
                            text-decoration: none;
                            border-radius: 5px;
                            text-align: center;
                            width: 100%;
                        ">Complete Subscription</a>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.error("Failed to create subscription")

        with col3:
            if self.create_custom_card(
                "Patron Member",
                "Join our exclusive community of supporters",
                "Custom Amount",
                "🎭 Become a Patron",
                "👑"
            ):
                patreon_url = self.payment_processor.get_patreon_auth_url()
                st.markdown(
                    f"""
                    <a href="{patreon_url}" target="_blank" style="
                        display: inline-block;
                        padding: 0.5rem 1rem;
                        background-color: #FF4B4B;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        text-align: center;
                        width: 100%;
                    ">Connect with Patreon</a>
                    """,
                    unsafe_allow_html=True
                )

        # Add testimonials section
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: center; padding: 2rem 0;">
                <h2 style="color: #1f1f1f;">What Our Supporters Say</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Testimonials
        test_col1, test_col2 = st.columns(2)
        with test_col1:
            st.markdown(
                """
                <div style="
                    padding: 1.5rem;
                    border-radius: 10px;
                    background: #f8f9fa;
                    margin: 1rem 0;
                ">
                    <p style="font-style: italic; color: #666;">
                        "EduVision has transformed how I create educational content. 
                        Supporting this project was one of the best decisions I've made!"
                    </p>
                    <p style="color: #1f1f1f; font-weight: 500; margin-top: 1rem;">- Sarah K., Educator</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with test_col2:
            st.markdown(
                """
                <div style="
                    padding: 1.5rem;
                    border-radius: 10px;
                    background: #f8f9fa;
                    margin: 1rem 0;
                ">
                    <p style="font-style: italic; color: #666;">
                        "The team's dedication to improving education through AI is inspiring. 
                        Proud to be a monthly supporter!"
                    </p>
                    <p style="color: #1f1f1f; font-weight: 500; margin-top: 1rem;">- Michael R., Tech Enthusiast</p>
                </div>
                """,
                unsafe_allow_html=True
            )