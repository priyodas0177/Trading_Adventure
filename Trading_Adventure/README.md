#  Algorithmic Trading Adventure (Task 1)

##  Project Overview
This project implements a class-based algorithmic trading system using Python.  
The system downloads historical stock data, calculates moving averages, detects trading signals (Golden Cross and Death Cross), executes buy/sell decisions with a fixed budget, and evaluates the final profit or loss.

---

##  Features
- Download historical stock data using **yfinance**
- Data cleaning (remove duplicates, handle missing values)
- Calculate:
  - 50-day Moving Average (MA50)
  - 200-day Moving Average (MA200)
- Detect:
  - Golden Cross → Buy signal
  - Death Cross → Sell signal
- Investment strategy with fixed budget ($5000)
- Force close open trade on last day
- Result evaluation

---

##  Trading Strategy Logic

### Golden Cross (Buy Signal)
When:
MA50 today > MA200 today  
AND  
MA50 yesterday ≤ MA200 yesterday  

This indicates a bullish trend.

### Death Cross (Sell Signal)
When:
MA50 today < MA200 today  
AND  
MA50 yesterday ≥ MA200 yesterday  

This indicates a bearish trend.



##  Investment Rules
- Initial budget: **$5000**
- Buy maximum shares possible
- Only one open position at a time
- Sell when death cross occurs
- Force sell on last date if position still open


###  Clone Repository
- git clone https://github.com/priyodas0177/Genuine_Technology_Research_Ltd.git 
- cd Genuine_Technology_Research_Ltd
- cd Trading_Adventure 

###  Install Dependencies
pip install -r requirements.txt  


## How to Run
python main.py


##  Output Example
TRADES
('BUY', 2019-05-06, 49.72, 100)
('SELL', 2022-06-03, 142.65, 100)
('BUY', 2022-09-26, 148.14, 129)
('SELL', 2022-10-07, 137.65, 129)
('BUY', 2023-03-22, 155.57, 236)
('FINAL_SELL', 2023-12-29, 190.55, 236)

RESULT
Initial Budget: 5000  
Final Cash: 81685.88  
Profit/Loss: 76685.88  
Profit %: 1533.72%  

Golden cross (BUY) signals:
Price            Close        MA50       MA200
Date
2019-05-06   49.723335   45.776048   45.656102
2022-09-26  148.144653  157.368102  157.331368
2023-03-22  155.576157  145.571570  145.345217

Death cross (SELL) signals:
Price            Close        MA50       MA200
Date
2018-12-21   35.796196   45.689574   45.797233
2022-06-03  142.650314  155.957857  156.110631
2022-10-07  137.650604  155.902536  156.052521

![image alt](https://github.com/priyodas0177/Genuine_Technology_Research_Ltd/blob/main/Trading_Adventure/Screenshot%202026-02-25%20234016.png)

##  Limitations
- No transaction costs considered
- Moving averages are lagging indicators
- Single stock testing only
- No risk management rules


