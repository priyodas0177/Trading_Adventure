import yfinance as yf
import pandas as pd

class Trading:
    def __init__(self,symbol,start_date,end_date,budget=5000):
        self.symbol=symbol
        self.start_date=start_date
        self.end_date=end_date
        self.budget=budget

        self.data=None #store dataframe
        self.cash=budget    # cash money 
        self.in_position=False
        self.shares=0
        self.trades=[] #store trade histore

    #download data
    def download_data(self):
        df=yf.download(self.symbol, start=self.start_date, end=self.end_date)
        self.data=df
    
    #fix column
    def fixed_column(self):
        if isinstance(self.data.columns, pd.MultiIndex):
            self.data.columns=self.data.columns.get_level_values(0)

    #clean data
    def clean_data(self):
        self.data=self.data[~self.data.index.duplicated(keep="first")] #Remove duplicate date rows (if any)
        self.data.ffill(inplace=True)

    #moving average
    def moving_average(self):
        self.data["MA50"]=self.data["Close"].rolling(window=50).mean() #short trade
        self.data["MA200"]=self.data["Close"].rolling(window=200).mean() #long trade

    #golden cross
    def detect_cross(self):
        self.data["golden_cross"]=(
            (self.data["MA50"]>self.data["MA200"]) &
            (self.data["MA50"].shift(1) <=self.data["MA200"].shift(1))
        )

        #death cross
        self.data["death_cross"]=(
            (self.data["MA50"]<self.data["MA200"]) &
            (self.data["MA50"].shift(1) >=self.data["MA200"].shift(1))

        )
    def trade(self):
        for i in range(1,len(self.data)):
            row=self.data.iloc[i]
            date=self.data.index[i]
            price=float(row["Close"])

            #buy golden cross
            if row ["golden_cross"] and (self.in_position==False):
                qty=int(self.cash//price)
                if qty>0:
                    self.shares=qty
                    self.cash=qty*price
                    self.in_position=True

                    self.trades.append(("BUY", date, price, qty))

            elif row["death_cross"] and (self.in_position==True):
                self.cash +=self.shares*price
                self.trades.append(("SELL",date,price,self.shares))

                self.shares=0
                self.in_position=False

    def force_close(self):
        if self.in_position:
            last_row=self.data.iloc[-1]
            last_date=self.data.index[-1]
            last_price=float(last_row["Close"])

            self.cash+=self.shares *last_price
            self.trades.append(("FINAL_SELL", last_date,last_price,self.shares))

            self.shares=0
            self.in_position=False
    
    def report(self):
        profit=self.cash-self.budget
        profit_percent=(profit/self.budget)*100

        print("\n TRADES ")
        for t in self.trades:
            print(t)
        
        print("\n RESULT ")
        print("Total Trade: ",len(self.trades))
        print("Initial Budget: ",self.budget)
        print("Final Cash: ", round(self.cash,2))
        print("Profit/Loss: ",round(profit,2))
        print("profit %: ",round(profit_percent,2),"%")




#create object   
bot=Trading("AAPL", "2018-01-01", "2023-12-31")

#call method and print
bot.download_data()
bot.fixed_column()
bot.clean_data()
bot.moving_average()
bot.detect_cross()
bot.trade()
bot.force_close()
bot.report()

print(bot.data.isna().sum())
print(bot.data.columns)
print(bot.data.head())
print(bot.data[["Close","MA50","MA200"]].tail())

buy_signals=bot.data[bot.data["golden_cross"]==True]
print("\nGolden cross (BUY) signals: ")
print(buy_signals[["Close", "MA50", "MA200"]].head())

sell_signals=bot.data[bot.data["death_cross"]==True]
print("\nDeath cross (SELL) signals: ")
print(sell_signals[["Close", "MA50", "MA200"]].head())
