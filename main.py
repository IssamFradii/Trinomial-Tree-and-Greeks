# main.py

import xlwings as xw
import datetime
import time

from py_class.arbre import Arbre
from py_class.market import Market
from py_class.option import Contract
from py_class.display import afficher_arbre_et_proba
from py_class.utils import BS

@xw.func
def main():
    wb = xw.Book.caller()
    ws1 = wb.sheets["Pricer"]

    S = ws1.range("I8").value
    r = ws1.range("I9").value
    sigma = ws1.range("I10").value
    
    today = ws1.range("I7").value
    maturity_date = ws1.range("M7").value

    type_op = ws1.range("M8").value
    ex_op = ws1.range("M9").value
    K = ws1.range("M10").value
    N = int(ws1.range("Q7").value)

    T = (maturity_date - today).days / 365
    affichage = ws1.range("Q8").value
    div = ws1.range("I11").value
    div_date = ws1.range("I12").value
    T_div = (div_date - today).days / 365

    m = Market(stock_price=S, int_rate=r, sigma=sigma, div= div, div_date=div_date)
    c = Contract(pricing_date=today, maturity_date=maturity_date, strike=K, op_type=type_op, op_exercice=ex_op)

    start = time.time()
    ar = Arbre(market=m, contract=c, n_steps=N)
    end = time.time()
    elapsed_time = end - start
    ws1.range("R19").value = elapsed_time

    bs_price = BS(S, K, T, r, sigma, type_op,div,T_div)
    ws1.range("R16").value = bs_price




    s = time.time()
    backward_tree_price = c.price_iteratively(ar)
    e = time.time()
    tree_pricing_delay = e - s
    ws1.range("R17").value = backward_tree_price  # Backward pricer

    recursive_tree_price = c.price_recursively(ar)
    ws1.range("R22").value = recursive_tree_price  # Recursive pricer

    ws1.range("R20").value = tree_pricing_delay 
    


    if affichage in ["All"]:
        afficher_arbre_et_proba(ar)
        
    print("Done !!!!")


@xw.func
@xw.arg('maturity_date', dates=datetime.date)
@xw.arg('pricing_date', dates=datetime.date)
def OptionPricerPyRec(pricing_date, maturity_date, stock_price, strike, int_rate, sigma, op_type, op_exercice, n_steps):
        market = Market(stock_price=stock_price, int_rate=int_rate, sigma=sigma)
        contract = Contract(pricing_date=pricing_date, maturity_date=maturity_date, strike=strike, op_type=op_type, op_exercice=op_exercice)

        tree = Arbre(market=market, contract=contract, n_steps=int(n_steps))
        price = contract.price_recursively(tree)

        return price

if __name__ == '__main__':
    xw.Book("Projet_Milos_Issam.xlsm").set_mock_caller()
    main()




# pour la semaine pro rajouter les divs et les differents graphn de log steps au niveau de cours 
# continue de coder sur vba la partie de recursive pricing sur vba 
# rajouter une methode pour checker les proba entre 0 et 1 



