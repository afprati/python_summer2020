# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 10:56:49 2020

@author: Annamaria Prati
"""
from random import uniform

class Portfolio:
    def __init__(self): #initializes class
        self.cash = 0
        self.stock = {}
        self.fund = {}
        self.bond = {} # for ease of adding another asset
        self.log = []
    
    def __str__(self): #allows for printing
        return ("You have $" + str("{:.2f}".format(self.cash)) + " in cash, "  
                + str(sum(i for i, _ in self.stock.values())) 
                + " shares of stock, and " 
                + str(sum(i for i, _ in self.fund.values())) 
                + " shares of mutual funds.")
    
    def history(self):
        print('\nHistory:')
        print('\n'.join(self.log)) #adding line breaks for readability
    
    def addCash(self, amount):
        try:
            self.cash += amount
            self.log.append("Added $%.2f in cash."%amount)
            #print ("Added $%.2f in cash."%amount)
            return True
       
        except TypeError:
            print("Cash amount must be a number.")
        
        else:
            print("Error adding cash, enter a valid dollar amount.")
    
    def withdrawCash(self, amount):
        try:
            if self.cash <= amount:
                raise insufficientCash("Error, not enough cash.")
            else:
                self.cash -= amount
                self.log.append("Withdrew $%.2f in cash"%amount)
                #print( "Withdrew $%.2f in cash."%amount)
                return True
        except TypeError:
            print("Cash amount must be a number.")
        else:
            print("Error withdrawing cash, enter a valid dollar amount")
    
    #buying/selling functions defined in subclasses
    def buyStock(self, quantity, stock):
        #print("Buying {} of {}".format(quantity, stock))
        return stock.buy(quantity, self)
    
    def sellStock(self, symbol, quantity):
        if symbol in portfolio.stock.keys():
            stock_price = portfolio.stock[symbol][1]
            stock_to_sell = Stock(stock_price, symbol)
            #print("Selling {} of {}".format(quantity, symbol))
            return stock_to_sell.sell(quantity, self)
        else:
            print("Don't own any shares of stock {}".format(symbol))
    
    def buyMutualFund(self, quantity, fund):
        #print("Buying {} of {}".format(quantity, fund))
        return fund.buy(quantity, self)
    
    def sellMutualFund(self, symbol, quantity):
        if symbol in portfolio.fund.keys():
            fund_to_sell = MutualFund(symbol)
            #print("Selling {} of {}".format(quantity, symbol))
            return fund_to_sell.sell(quantity, self)
        else:
            print("Don't own any shares of mutual fund {}".format(symbol))
    
    #adding bonds to show how one would add another Asset
    def buyBonds(self, quantity, bond):
        pass
    
    def sellBonds(self, quantity, bond):
        pass

class insufficientCash(Exception): #custom exception for not enough cash
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)
        
    
class Asset():
    def __init__(self, price, symbol): #default price $1
        self.price = price
        self.symbol = symbol
    #would ideally have buy and sell generally defined here    
    def buy(self):
        pass
    
    def sell(self):
        pass
    
          
class Stock(Asset): # NB: must be bought/sold as integer
    def __init__(self, price, symbol):
        Asset.__init__(self, price, symbol) 
        #print("Generated stock {}".format(symbol))   
    
    def buy(self, quantity, portfolio):
        try:
            if quantity%1 ==0: #quantity must be an integer
                #withdrawing cash to pay for funds, which checks there is enough
                portfolio.withdrawCash(self.price*quantity) 
                
                # if already have shares of that fund, don't create new key
                already_owns_stock = self.symbol in portfolio.stock.keys()
                if already_owns_stock: 
                    previous_quantity = portfolio.stock[self.symbol][0]
                    portfolio.stock[self.symbol] = (previous_quantity + quantity, self.price)
                    
                else: # add to dictionary with new key=symbol/value=quantity
                    portfolio.stock[self.symbol] = (quantity, self.price)
                
                portfolio.log.append("Bought {} shares of {} for {} per share"
                                     .format(quantity, self.symbol, self.price))
            return True
        
        except TypeError:
            print ("Quantity must be an integer")
        
        except:
            print("Error buying stock")
        
        #except Exception as e: 
        #    print(e)
        
    def sell(self, sell_quantity, portfolio):
        try:
            if sell_quantity%1 == 0: #quantity must be an integer
                (current_stock_quantity, current_stock_price) = portfolio.stock[self.symbol]
                has_enough_shares = current_stock_quantity >= sell_quantity
                if (has_enough_shares):
                    #rounded for valid $; price from uniform dist
                    sell_price = round(uniform(0.5*current_stock_price, 1.5*current_stock_price), 2) 
                    #decreasing shares
                    portfolio.stock[self.symbol] = (current_stock_quantity - sell_quantity, current_stock_price)
                    portfolio.log.append("Sold {} shares of {} for {} per share"
                                     .format(sell_quantity, self.symbol, sell_price))
                    portfolio.addCash(sell_quantity*sell_price)
                    return True
                else:
                    return "Not enough shares or shares do not exist."
        except TypeError:
            print ("Quantity must be an integer")
        
        except:
            print("Error selling stock")
            

    def __str__(self):
        #return self.symbol + " at $" + "{:.2f}".format(self.price)
        return self.symbol
    
        
class MutualFund(Asset):
    def __init__(self, symbol):
        Asset.__init__(self, 1, symbol) # want $1/unit
        #print("Generated mutual fund {}".format(symbol)) 
    
    def buy(self, quantity, portfolio):
        try:
            #withdrawing cash to pay for funds, which checks there is enough 
            portfolio.withdrawCash(self.price*quantity) 
            
            # if already have shares of that fund, don't create new key
            already_owns_fund = self.symbol in portfolio.fund.keys()
            if already_owns_fund: 
                previous_quantity = portfolio.fund[self.symbol][0]
                portfolio.fund[self.symbol] = (previous_quantity + quantity, self.price)
                
            else: # add to dictionary with new key=symbol/value=quantity
                portfolio.fund[self.symbol] = (quantity, self.price)
            
            portfolio.log.append("Bought {} shares of {} for {} per share"
                                 .format(quantity, self.symbol, self.price))
            return True
        
        except:
            print("Error buying fund")
            
    def sell(self, sell_quantity, portfolio):
        try:
            (current_fund_quantity, current_fund_price) = portfolio.fund[self.symbol]
            has_enough_shares = current_fund_quantity >= sell_quantity
            if (has_enough_shares):
                #rounded for valid $; price from uniform dist
                sell_price = round(uniform(0.9*current_fund_price, 1.2*current_fund_price), 2) 
                #decreasing shares
                portfolio.fund[self.symbol] = (current_fund_quantity - sell_quantity, current_fund_price)
                portfolio.log.append("Sold {} shares of {} for {} per share"
                                 .format(sell_quantity, self.symbol, sell_price))
                portfolio.addCash(sell_quantity*sell_price)
                return True
            else:
                return "Not enough shares."
        
        except:
            print("Error selling fund")
            
    def __str__(self):
        return self.symbol + " at $1 per share."



class Bond(Asset): #to show ease of adding another Asset
    def __init__():
        pass
    
    def buy():
        pass
    
    def sell():
        pass
    
    def __str__():
        pass


"""
To check work:
"""   
    
#Creates a new portfolio
portfolio = Portfolio()
print(portfolio)

#Adds cash to the portfolio 
portfolio.addCash(300.5) 

"""
Begin extra cash tests:
"""
print(portfolio) 
#portfolio.addCash("Hello")
#portfolio.addCash(10.50)
#print(portfolio)
#portfolio.withdrawCash("World")
#portfolio.withdrawCash(10.50)
#print(portfolio)

"""
End extra cash tests:
"""

#Create Stock with price 20 and symbol "HFH"
s = Stock(20.5, "HFH")    

#Buys 5 shares of stock s
portfolio.buyStock(5, s)              

#Create MF with symbol "BRT"
mf1 = MutualFund("BRT")               

#Create MF with symbol "GHT"
mf2 = MutualFund("GHT")

#Buys 10.3 shares of "BRT"
portfolio.buyMutualFund(10.3, mf1)

#Buys 2 shares of "GHT"
portfolio.buyMutualFund(2, mf2)

#Prints portfolio
print(portfolio)
#cash: $140.50, though I think the assignment is wrong
#stock: 5 HFH
#mutual funds: 10.33 BRT
#              2     GHT

#Sells 3 shares of BRT
portfolio.sellMutualFund("BRT", 3)    

#Sells 1 share of HFH
portfolio.sellStock("HFH", 1) 


#Removes $50        
portfolio.withdrawCash(50)            

#Prints a list of all transactions ordered by time
portfolio.history()                   
