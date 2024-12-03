import numpy as np
import pandas as pd
from typing import Dict, List, Union, Any

class TaxOptimizationTool:
    def __init__(self, income: float, portfolio: Dict[str, float], region: str = 'US'):
        """
        Initialize tax optimization tool with user financial profile
        
        :param income: Annual income
        :param portfolio: Current investment portfolio allocation
        :param region: Tax jurisdiction (default: US)
        """
        self.income = income
        self.portfolio = portfolio
        self.region = region
        self.tax_rates = self._get_tax_rates()
    
    def _get_tax_rates(self) -> Dict[str, float]:
        """
        Retrieve tax rates based on region and income bracket
        
        :return: Dictionary of tax rates for different investment types
        """
        base_rates = {
            'US': {
                'short_term_capital_gains': 0.37 if self.income > 578125 else 
                           0.35 if self.income > 209425 else 
                           0.32 if self.income > 170050 else 
                           0.24 if self.income > 89075 else 
                           0.22 if self.income > 41775 else 0.12,
                'long_term_capital_gains': 0.20 if self.income > 492300 else 
                              0.15 if self.income > 44625 else 0.0,
                'dividend': 0.20 if self.income > 492300 else 
                           0.15 if self.income > 44625 else 0.0
            }
        }
        return base_rates.get(self.region, base_rates['US'])
    
    def tax_loss_harvesting(self, investment_data: pd.DataFrame) -> Dict[str, Union[float, List[str]]]:
        """
        Identify tax loss harvesting opportunities
        
        :param investment_data: DataFrame with investment performance data
        :return: Dict with tax loss opportunities and potential savings
        """
        unrealized_losses = investment_data[investment_data['return'] < 0]
        total_loss = unrealized_losses['return'].sum()
        
        harvest_candidates = unrealized_losses['ticker'].tolist()
        max_deductible_loss = min(total_loss, 3000)  # Standard US tax rule
        
        return {
            'total_potential_tax_savings': max_deductible_loss * self.tax_rates['short_term_capital_gains'],
            'harvest_candidates': harvest_candidates,
            'max_deductible_loss': max_deductible_loss
        }
    
    def optimize_portfolio_tax_efficiency(self) -> Dict[str, Union[float, Dict]]:
        """
        Recommend tax-efficient portfolio rebalancing
        
        :return: Optimized portfolio allocation with tax considerations
        """
        optimized_allocation = {
            'bonds': 0.3,  # Tax-efficient municipal bonds
            'index_funds': 0.4,  # Lower turnover, more tax-efficient
            'dividend_stocks': 0.2,  # Qualified dividend treatment
            'real_estate': 0.1  # Potential tax advantages
        }
        
        estimated_tax_efficiency = sum([
            rate * allocation 
            for rate, allocation in zip(
                [self.tax_rates['long_term_capital_gains']] * len(optimized_allocation), 
                optimized_allocation.values()
            )
        ])
        
        return {
            'optimized_portfolio': optimized_allocation,
            'estimated_tax_efficiency': estimated_tax_efficiency,
            'tax_savings_potential': estimated_tax_efficiency * self.income * 0.05
        }
    
    def generate_tax_strategy_report(self, investment_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive tax optimization report
        
        :param investment_data: Investment performance data
        :return: Detailed tax optimization insights
        """
        tax_loss_harvest = self.tax_loss_harvesting(investment_data)
        portfolio_optimization = self.optimize_portfolio_tax_efficiency()
        
        return {
            'tax_loss_harvesting': tax_loss_harvest,
            'portfolio_optimization': portfolio_optimization,
            'recommendations': [
                f"Consider harvesting losses from: {', '.join(tax_loss_harvest['harvest_candidates'])}",
                f"Potential tax savings: ${tax_loss_harvest['total_potential_tax_savings']:.2f}",
                f"Recommended portfolio rebalancing for tax efficiency",
                f"Estimated annual tax savings: ${portfolio_optimization['tax_savings_potential']:.2f}"
            ]
        }