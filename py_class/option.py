import math

class Contract:
    def __init__(self, pricing_date, maturity_date, strike, op_type=None, op_exercice=None):
        self.maturity_date = maturity_date
        self.pricing_date = pricing_date
        self.maturity = ((self.maturity_date - self.pricing_date).days) / 365
        self.strike = strike
        self.op_type = op_type  # "Call" ou "Put"
        self.op_exercice = op_exercice  # "EU" ou "US"
        self.op_multiplicator = 1 if self.op_type == "Call" else -1

    def price_recursively(self, arbre):
        discount_factor = math.exp(-arbre.market.int_rate * arbre.dt)
        return self._recursive_pricer(arbre.racine, discount_factor)
    
    def _recursive_pricer(self, node, df):
        if hasattr(node, 'si2') and node.si2 is not None:
            return node.si2
        if node.next_mid is None:
            payoff = max(0, (node.si - self.strike) * self.op_multiplicator)
            node.si2 = payoff
            return payoff
        EV = (node.p_up * self._recursive_pricer(node.next_up, df) +
              node.p_mid * self._recursive_pricer(node.next_mid, df) +
              node.p_down * self._recursive_pricer(node.next_down, df))
        continuation_value = df * EV
        if self.op_exercice == "US":
            intrinsic = max(0, (node.si - self.strike) * self.op_multiplicator)
            node.si2 = max(continuation_value, intrinsic)
        else:
            node.si2 = continuation_value
        return node.si2

    def price_iteratively(self, arbre, type_option=None, style_option=None):
        r = arbre.market.int_rate
        N = arbre.n_steps
        T = arbre.contract.maturity
        K = arbre.contract.strike
        dt = T / N
        d_f = math.exp(-r * dt)
        type_op = type_option if type_option is not None else arbre.contract.op_type
        op_exercice = style_option if style_option is not None else arbre.contract.op_exercice
        op_multiplicator = 1 if type_op == "Call" else -1
        last_node = arbre.racine
        while last_node.next_mid is not None:
            last_node = last_node.next_mid

        self._set_payoff(last_node, K, op_multiplicator)
        self._roll_back(last_node, d_f, op_exercice, K, op_multiplicator)
        return arbre.racine.si2

    def _set_payoff(self, last_node, K, op_multiplicator):
        # Traverse up
        current_node = last_node
        while current_node is not None:
            current_node.si2 = max((current_node.si - K) * op_multiplicator, 0)
            current_node = current_node.voisin_up
        # Traverse down
        current_node = last_node
        while current_node is not None:
            current_node.si2 = max((current_node.si - K) * op_multiplicator, 0)
            current_node = current_node.voisin_down

    def _roll_back(self, last_node, d_f, op_exercice, K, op_multiplicator):
        while last_node is not None:
            last_node = last_node.voisin_behind
            # Traverse up et roll back les valeurs
            current_node = last_node
            while current_node is not None:
                u = current_node.p_up
                pm = current_node.p_mid
                d = current_node.p_down
                val = (u * current_node.next_mid.voisin_up.si2 +
                       pm * current_node.next_mid.si2 +
                       d * current_node.next_mid.voisin_down.si2) * d_f
                if op_exercice == "US":
                    intrinsic = max((current_node.si - K) * op_multiplicator, 0)
                    current_node.si2 = max(val, intrinsic)
                else:
                    current_node.si2 = val
                current_node = current_node.voisin_up
            # branche Down Aussi
            current_node = last_node
            while current_node is not None:
                u = current_node.p_up
                pm = current_node.p_mid
                d = current_node.p_down
                val = (u * current_node.next_mid.voisin_up.si2 +
                       pm * current_node.next_mid.si2 +
                       d * current_node.next_mid.voisin_down.si2) * d_f
                if op_exercice == "US":
                    intrinsic = max((current_node.si - K) * op_multiplicator, 0)
                    current_node.si2 = max(val, intrinsic)
                else:
                    current_node.si2 = val
                current_node = current_node.voisin_down




# si ex div c est vers la fin de l arbre bah de coup on bouge le prix de strike  while pricer 
