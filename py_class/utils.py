import numpy as np 
from scipy.stats import norm
import math as m 


from typing import Callable, Any


def BS(S, K, T, r, sigma,type_op,D,T_div):
    # Ajustement du sous-jacent
    S_adj = S   * np.exp(-r * T_div)

    # Calculs standard de Black-Scholes
    N = norm.cdf
    d1 = (np.log(S_adj / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if type_op == "Call":
        prix = S_adj * N(d1) - K * np.exp(-r * T) * N(d2)
    elif type_op == "Put":
        prix = K * np.exp(-r * T) * N(-d2) - S_adj * N(-d1)
    else:
        raise ValueError("type_op doit être 'Call' ou 'Put'")

    return prix


class OneDimDerivative:
    def __init__(
        self,
        function: Callable[[Any, float], float],
        other_parameters: Any,
        shift: float = 1.0
    ):
        self.f: Callable[[Any, float], float] = function
        self.param: Any = other_parameters
        self.shift: float = shift

    def first(self, x: float) -> float:
        # Central difference for Delta
        return (self.f(self.param, x + self.shift) - self.f(self.param, x - self.shift)) / (2 * self.shift)

    def second(self, x: float) -> float:
        # Central difference for Gamma
        return (
            self.f(self.param, x + self.shift)
            + self.f(self.param, x - self.shift)
            - 2 * self.f(self.param, x)
        ) / (self.shift ** 2)

    def vega(self, sigma: float) -> float:
        """
        Central difference for Vega (derivative with respect to sigma).
        Assumes that in self.f, the second argument is the volatility (sigma).
        Use shift = 0.005 for 0.5% diff on sigma.
        """
        return (self.f(self.param, sigma + self.shift) - self.f(self.param, sigma - self.shift)) / (2 * self.shift)


def OptionDeltaTreeBackward(market_range: np.ndarray, pricer_range: np.ndarray, option_range: np.ndarray) -> float:
    """
    Compute Delta (first derivative w.r.t. S0) using finite differences.
    """
    return OneDimDerivative(
        function=_PriceTreeBackward_OneDimPrice,
        other_parameters=OptionPricingParam(market_range, pricer_range, option_range),
        shift=market_range[0] * OptionPricingParam.UND_SHIFT
    ).first(market_range[0])


def OptionGammaTreeBackward(market_range: np.ndarray, pricer_range: np.ndarray, option_range: np.ndarray) -> float:
    """
    Compute Gamma (second derivative w.r.t. S0) using finite differences.
    """
    return OneDimDerivative(
        function=_PriceTreeBackward_OneDimPrice,
        other_parameters=OptionPricingParam(market_range, pricer_range, option_range),
        shift=market_range[0] * OptionPricingParam.UND_SHIFT
    ).second(market_range[0])


def OptionVegaTreeBackward(market_range: np.ndarray, pricer_range: np.ndarray, option_range: np.ndarray) -> float:
    """
    Compute Vega (derivative w.r.t. sigma) using finite differences.
    Assumes market_range[2] is sigma, and shift is 0.005 (0.5%).
    """
    return OneDimDerivative(
        function=_PriceTreeBackward_OneDimPrice,
        other_parameters=OptionPricingParam(market_range, pricer_range, option_range),
        shift=OptionPricingParam.VOL_SHIFT  # e.g., 0.005 for 0.5%
    ).vega(market_range[2])  # market_range[2] is sigma
    


    

