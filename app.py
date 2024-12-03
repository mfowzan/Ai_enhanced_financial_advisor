import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Set API Endpoints
API_URL = "http://127.0.0.1:5000/predict"
GLOSSARY_URL = "http://127.0.0.1:5000/get_financial_term"
FINANCIAL_ADVISOR_URL = "http://127.0.0.1:5000/financial_advisor"

# Custom CSS for Modern Design and Tooltip
st.markdown("""
<style>
    .main {
        background-color: #f4f4f4;
        color: #333;
        font-family: 'Roboto', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ddd;
    }
    .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ddd;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted blue;
        cursor: help;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: #f9f9f9;
        color: #333;
        text-align: left;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -150px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    .chatbot-container {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 15px;
        max-height: 500px;
        overflow-y: auto;
    }
    .user-message {
        background-color: #e6f2ff;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .bot-message {
        background-color: #f0f0f0;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

def get_financial_term_explanation(term):
    try:
        response = requests.get(f"{GLOSSARY_URL}?term={term}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching term explanation: {e}")
    return {"definition": "Term explanation unavailable.", "example": ""}

def render_term_with_tooltip(term, display_text=None):
    """Render a term with a tooltip for its explanation."""
    if display_text is None:
        display_text = term.replace('_', ' ').title()
    
    term_info = get_financial_term_explanation(term)
    
    st.markdown(f"""
    <div class="tooltip">{display_text}
        <span class="tooltiptext">
        <strong>Definition:</strong> {term_info['definition']}
        <br><br>
        <strong>Example:</strong> {term_info['example']}
        </span>
    </div>
    """, unsafe_allow_html=True)

def financial_advisor_chat(query):
    """Send query to financial advisor API and get response"""
    try:
        response = requests.post(FINANCIAL_ADVISOR_URL, json={'query': query})
        if response.status_code == 200:
            return response.json().get('response', 'No response received.')
        else:
            return "Sorry, I couldn't process your request at the moment."
    except Exception as e:
        return f"An error occurred: {e}"

def financial_advisor_chatbot():
    """Streamlit component for Financial Advisor Chatbot"""
    st.header("🤖 Financial Advisor Chatbot")
    st.markdown("Ask me anything about personal finance, investments, or financial planning!")

    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Chat input
    user_query = st.text_input("Your Question:", key="financial_advisor_input")

    # Send button
    if st.button("Ask Financial Advisor"):
        if user_query:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_query})

            # Get bot response
            bot_response = financial_advisor_chat(user_query)
            st.session_state.chat_history.append({"role": "bot", "content": bot_response})

    # Display chat history
    if st.session_state.chat_history:
        st.markdown('<div class="chatbot-container">', unsafe_allow_html=True)
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.title("AI Financial Advisor")
    st.subheader("Personalized Investment Intelligence")

    # Tabs for different features
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Financial Analysis", "Investment Insights", "Financial Goals", "AI Financial Advisor", "Tax Optimization"]
    )

    with tab1:
        # Financial Analysis Inputs
        col1, col2 = st.columns(2)

        with col1:
            income = st.number_input("Monthly Income ($):", min_value=0, value=5000, step=100)
            expenses = st.number_input("Monthly Expenses ($):", min_value=0, value=2000, step=100)
            savings = st.number_input("Monthly Savings ($):", min_value=0, value=1000, step=100)
            investment_amount = st.number_input("Investment Amount ($):", min_value=0, value=1500, step=100)

        with col2:
            debt = st.number_input("Debt ($):", min_value=0, value=500, step=100)
            current_savings = st.number_input("Current Savings ($):", min_value=0, value=10000, step=100)
            target_amount = st.number_input("Financial Goal Target ($):", min_value=0, value=50000, step=1000)
            investment_type = st.selectbox("Investment Type:", ["stocks", "bonds", "real_estate", "crypto"])

        # Additional Financial Parameters
        col3, col4 = st.columns(2)

        with col3:
            monthly_savings = st.number_input("Monthly Retirement Savings ($):", min_value=0, value=500, step=50)

        with col4:
            years_to_retire = st.number_input("Years to Retirement:", min_value=0, value=20, step=1)

        # Check for unrealistic values
        if expenses > income:
            st.warning("Warning: Expenses cannot exceed income!")

        # Submit Button
        if st.button("Get Financial Insights"):
            # Prepare data for API
            input_data = {
                "income": income,
                "expenses": expenses,
                "savings": savings,
                "investment_amount": investment_amount,
                "debt": debt,
                "current_savings": current_savings,
                "target_amount": target_amount,
                "investment_type": investment_type,
                "monthly_savings": monthly_savings,
                "years_to_retire": years_to_retire,
            }

            # Send request to API
            with st.spinner("Analyzing Financial Data..."):
                try:
                    response = requests.post(API_URL, json=input_data)
                    if response.status_code == 200:
                        result = response.json()

                        # Financial Overview Tab
                        st.header("Financial Health Dashboard")
    
                        col1, col2, col3 = st.columns(3)
    
                        with col1:
                            st.write("Risk Tolerance: ", end="")
                            render_term_with_tooltip("risk_tolerance", result['risk_tolerance'])
    
                        with col2:
                            st.write("Savings Rate: ", end="")
                            render_term_with_tooltip("savings_rate", result['savings_rate'])
    
                        with col3:
                            st.write("Emergency Fund: ", end="")
                            render_term_with_tooltip("emergency_fund", result['emergency_fund'])

                        # Tax Optimization Display
                        st.header("🧾 Tax Optimization Insights")
                        
                        if result.get('tax_optimization_report'):
                            tax_report = result['tax_optimization_report']
                            
                            # Tax Loss Harvesting Section
                            st.subheader("Tax Loss Harvesting")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Potential Tax Savings", 
                                          f"${tax_report.get('tax_loss_harvesting', {}).get('total_potential_tax_savings', 0):.2f}")
                                st.write("Harvest Candidates:", 
                                         ", ".join(tax_report.get('tax_loss_harvesting', {}).get('harvest_candidates', [])))
                            
                            with col2:
                                st.metric("Max Deductible Loss", 
                                          f"${tax_report.get('tax_loss_harvesting', {}).get('max_deductible_loss', 0):.2f}")
                            
                            # Portfolio Optimization Section
                            st.subheader("Portfolio Tax Optimization")
                            portfolio_opt = tax_report.get('portfolio_optimization', {})
                            
                            # Pie chart for tax-efficient portfolio allocation
                            opt_portfolio = portfolio_opt.get('optimized_portfolio', {})
                            fig_portfolio = px.pie(
                                names=list(opt_portfolio.keys()), 
                                values=list(opt_portfolio.values()), 
                                title='Tax-Efficient Portfolio Allocation'
                            )
                            st.plotly_chart(fig_portfolio)
                            
                            # Tax Efficiency Metrics
                            col3, col4 = st.columns(2)
                            with col3:
                                st.metric("Estimated Tax Efficiency", 
                                          f"{portfolio_opt.get('estimated_tax_efficiency', 0):.2%}")
                            with col4:
                                st.metric("Potential Annual Tax Savings", 
                                          f"${portfolio_opt.get('tax_savings_potential', 0):.2f}")
                            
                            # Recommendations
                            st.subheader("Tax Optimization Recommendations")
                            recommendations = tax_report.get('recommendations', [])
                            for rec in recommendations:
                                st.info(rec)
                        else:
                            st.warning("Tax optimization data not available. Please check your input parameters.")

                except Exception as e:
                    st.error(f"Error: {e}")

    with tab2:
        st.header("Investment Insights")
        # Investment Risk Bar Chart
        risk_data = pd.DataFrame({
            'Category': ['Short-Term', 'Long-Term', 'Investment Type'],
            'Risk Level': [0.7, 0.4, 0.6]  # Simulated risk levels
        })

        fig_risk = px.bar(risk_data, x='Category', y='Risk Level', 
        title='Investment Risk Profile')
        st.plotly_chart(fig_risk)

    with tab3:
        st.header("Financial Goals")
        st.write("Track and manage your financial goals")

    with tab4:
        # New Financial Advisor Chatbot tab
        financial_advisor_chatbot()
    
    with tab5:
        st.header("Advanced Tax Optimization")
        st.markdown("""
        ### AI-Powered Tax Optimization
        Our advanced tax optimization tool helps you:
        - Identify tax loss harvesting opportunities
        - Recommend tax-efficient investment vehicles
        - Dynamically balance short-term tax savings with long-term financial goals
        - Provide region-specific tax optimization strategies
        
        To get detailed tax insights, please use the Financial Analysis tab and submit your financial details.
        """)

        # Optional: Add a direct tax consultation feature
        st.subheader("Quick Tax Strategy Consultation")
        tax_query = st.text_area("Describe your tax situation:")
        if st.button("Get Tax Strategy Advice"):
            # You could integrate a specific tax strategy API call here
            st.info("For personalized tax strategy, consult with a certified tax professional.")

if __name__ == "__main__":
    main()