class Market:
    
    def __init__(self,stock_price,int_rate,sigma, div, div_date):
        
        self.stock_price = stock_price
        self.int_rate = int_rate
        self.sigma = sigma
        self.div = div
        self.div_date = div_date
        