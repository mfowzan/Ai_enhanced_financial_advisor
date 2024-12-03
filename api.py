from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import openai
import os

from optimize import TaxOptimizationTool

app = Flask(__name__)
CORS(app)

# OpenAI API Configuration
openai.api_key = os.getenv('OPENAI_API_KEY', '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')  # Replace with actual key or env variable

# Financial Terms Glossary Dictionary
FINANCIAL_TERMS_GLOSSARY = {
    "risk_tolerance": {
        "definition": "Risk tolerance is the amount of financial uncertainty an investor can handle. It measures how comfortable you are with potential investment losses in pursuit of potential gains.",
        "example": "Someone with high risk tolerance might be willing to invest in volatile stocks, while someone with low risk tolerance prefers stable, low-risk investments."
    },
    "bonds": {
        "definition": "Bonds are fixed-income investments where you lend money to a government or company in exchange for regular interest payments and return of the principal amount at maturity.",
        "example": "Government savings bonds are typically considered low-risk investments with predictable returns."
    },
    "stocks": {
        "definition": "Stocks represent ownership shares in a company. When you buy stocks, you become a partial owner of that company and can potentially benefit from its growth and profits.",
        "example": "Buying Apple stock means you own a small piece of the Apple company."
    },
    "emergency_fund": {
        "definition": "An emergency fund is a savings account set aside to cover unexpected expenses or financial emergencies, typically 3-6 months of living expenses.",
        "example": "If you lose your job, an emergency fund can help you cover basic living expenses while you find new employment."
    },
    "debt_ratio": {
        "definition": "Debt-to-income ratio is a financial metric that compares your monthly debt payments to your monthly income, helping assess your financial health.",
        "example": "If you earn $5000 monthly and have $1500 in debt payments, your debt ratio is 30%."
    },
    "tax_loss_harvesting": {
        "definition": "Tax loss harvesting is an investment strategy where you sell securities at a loss to offset capital gains taxes, potentially reducing your tax liability.",
        "example": "If you have a stock that has decreased in value, selling it can help offset taxes on other investment gains."
    },
    "portfolio_allocation": {
        "definition": "Portfolio allocation is the process of dividing investments among different asset categories like stocks, bonds, and cash to balance risk and reward.",
        "example": "A conservative portfolio might have 70% bonds and 30% stocks, while an aggressive portfolio might reverse those percentages."
    }
}

# Financial Advisor Chatbot Function
def financial_advisor_chat(user_query):
    """
    AI-powered financial advisor chatbot using OpenAI's GPT model
    """
    try:
        # Enhance context with financial domain expertise
        system_prompt = """
        You are an expert financial advisor. Provide clear, professional, 
        and actionable financial advice. Always:
        - Use simple, understandable language
        - Provide practical recommendations
        - Cite general financial principles
        - Avoid specific investment recommendations without disclaimers
        - Prioritize user's financial education
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"I apologize, but I encountered an error processing your query: {str(e)}"

# Feature: Calculate Risk Tolerance
def calculate_risk_tolerance(income, expenses, savings, investment_amount):
    risk = "medium"
    # Simple logic for risk tolerance, can be customized
    if investment_amount / income > 0.2:
        risk = "high"
    elif investment_amount / income < 0.1:
        risk = "low"
    return risk

# Feature: Investment Recommendation Based on Risk Tolerance
def get_investment_recommendation(risk_tolerance):
    recommendations = {
        "low": "We recommend investing in bonds or other low-risk assets.",
        "medium": "Consider diversifying with a mix of stocks and bonds.",
        "high": "You might want to invest in high-risk assets like options or cryptocurrency."
    }
    return recommendations.get(risk_tolerance, "No recommendation available.")

# Feature: Expense Optimization Tips
def get_expense_optimization_tips(income, expenses):
    if expenses > income:
        return "You are spending more than your income. Consider cutting unnecessary expenses."
    elif expenses > income * 0.7:
        return "Your expenses are high relative to your income. Look for opportunities to reduce spending."
    else:
        return "Your expenses seem well managed, keep up the good work!"

# Feature: Emergency Fund Calculator
def calculate_emergency_fund(expenses):
    emergency_fund = expenses * 6  # Assuming 6 months of expenses
    return f"Recommended emergency fund: ${emergency_fund}"

# Feature: Retirement Savings Estimate
def retirement_savings_estimate(current_savings, monthly_savings, years_to_retire):
    estimated_savings = current_savings + (monthly_savings * 12 * years_to_retire)
    return f"Estimated savings at retirement: ${estimated_savings}"

# Feature: Portfolio Allocation Based on Risk Tolerance
def portfolio_allocation(risk_tolerance):
    if risk_tolerance == "low":
        return {"Bonds": 80, "Stocks": 20}
    elif risk_tolerance == "medium":
        return {"Bonds": 50, "Stocks": 50}
    else:
        return {"Bonds": 20, "Stocks": 80}

# Feature: Debt Management Suggestions
def debt_management(income, debt):
    debt_ratio = debt / income
    if debt_ratio > 0.5:
        return "You have a high debt-to-income ratio. Consider focusing on debt repayment."
    elif debt_ratio > 0.3:
        return "Your debt level is manageable. Try to pay it off faster to reduce interest."
    else:
        return "Your debt is under control. Keep it up!"

# Feature: Track Financial Goals
def track_financial_goal(target_amount, current_savings):
    remaining_amount = target_amount - current_savings
    if remaining_amount > 0:
        return f"You need to save ${remaining_amount} more to reach your goal."
    else:
        return "Congratulations! You've reached your financial goal."

# Feature: Investment Risk Assessment
def investment_risk_assessment(investment_type):
    risks = {
        "stocks": "High volatility, but potential for high returns.",
        "bonds": "Stable returns with low volatility.",
        "real_estate": "Moderate risk with relatively stable returns.",
        "crypto": "Extremely high risk, but could yield high returns."
    }
    return risks.get(investment_type, "No data available.")

# Feature: Savings Rate Tracker
def calculate_savings_rate(income, savings):
    savings_rate = (savings / income) * 100
    if savings_rate < 10:
        return "Your savings rate is low. Try to increase your savings by cutting expenses."
    elif savings_rate < 20:
        return "Your savings rate is moderate. Aim for 20% or more for better financial security."
    else:
        return "Great job! Your savings rate is excellent."

# New route for financial term explanations
@app.route('/get_financial_term', methods=['GET'])
def get_financial_term():
    term = request.args.get('term')
    term_info = FINANCIAL_TERMS_GLOSSARY.get(term, {
        "definition": "Term not found in our glossary.",
        "example": "No example available."
    })
    return jsonify(term_info)

# New route for Financial Advisor Chatbot
@app.route('/financial_advisor', methods=['POST'])
def financial_advisor_endpoint():
    data = request.get_json()
    user_query = data.get('query', '')
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    response = financial_advisor_chat(user_query)
    return jsonify({"response": response})

# Existing prediction route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    income = data.get("income")
    expenses = data.get("expenses")
    savings = data.get("savings")
    investment_amount = data.get("investment_amount")
    debt = data.get("debt", 0)
    current_savings = data.get("current_savings", 0)
    target_amount = data.get("target_amount", 0)
    investment_type = data.get("investment_type", "")
    monthly_savings = data.get("monthly_savings", 0)
    years_to_retire = data.get("years_to_retire", 0)

    # Calculate risk tolerance
    risk_tolerance = calculate_risk_tolerance(income, expenses, savings, investment_amount)
    
    # Get investment recommendations
    investment_recommendation = get_investment_recommendation(risk_tolerance)

    # Get expense optimization tips
    expense_optimization_tips = get_expense_optimization_tips(income, expenses)

    # Calculate emergency fund
    emergency_fund = calculate_emergency_fund(expenses)

    # Estimate retirement savings
    retirement_estimate = retirement_savings_estimate(current_savings, monthly_savings, years_to_retire)

    # Calculate portfolio allocation
    portfolio = portfolio_allocation(risk_tolerance)

    # Get debt management advice
    debt_advice = debt_management(income, debt)

    # Track financial goal progress
    goal_tracking = track_financial_goal(target_amount, current_savings)

    # Assess investment risk
    investment_risk = investment_risk_assessment(investment_type)

    # Calculate savings rate
    savings_rate = calculate_savings_rate(income, savings)

    # Tax Optimization Integration
    try:
        # Create tax optimization tool instance
        tax_tool = TaxOptimizationTool(
            income=income * 12,  # Convert monthly to annual
            portfolio=portfolio,
            region='US'
        )

        # Simulate investment data for tax loss harvesting
        investment_data = pd.DataFrame({
            'ticker': list(portfolio.keys()),
            'return': [np.random.uniform(-0.1, 0.1) for _ in portfolio]
        })

        # Generate tax strategy report
        tax_optimization_report = tax_tool.generate_tax_strategy_report(investment_data)

    except Exception as e:
        print(f"Tax optimization error: {e}")
        tax_optimization_report = None

    # Return all recommendations
    return jsonify({
        "risk_tolerance": risk_tolerance,
        "investment_recommendation": investment_recommendation,
        "expense_optimization_tips": expense_optimization_tips,
        "emergency_fund": emergency_fund,
        "retirement_estimate": retirement_estimate,
        "portfolio": portfolio,
        "debt_advice": debt_advice,
        "goal_tracking": goal_tracking,
        "investment_risk": investment_risk,
        "savings_rate": savings_rate,
        "tax_optimization_report": tax_optimization_report
    })

if __name__ == '__main__':
    app.run(debug=True)