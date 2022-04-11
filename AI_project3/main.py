from neuralintents import GenericAssistant
import pandas_datareader as web
import sys

stock_tickers = ['AAPL', 'FB', 'GS', 'TSLA']

todos = ['watching video', 'eating', 'go shopping']

def stock_funct():
    for ticker in stock_tickers:
        data =  web.DataReader(ticker, 'yahoo')
        print(f"the last price of {ticker} was {data['Close'].iloc[-1]}")

def todo_show():
    print("Your todo list:")
    for todo in todos:
        print(todo)

def todo_add():
    todo = input("what todo do you want to add ?: ")
    todos.append(todo)

def todo_remove():
    indx = int(input("which todo to remove? "))
    if indx < len(todos):
        print(f"removing {todos.index(indx)}")
        todos.pop(indx)
    else:
        print("there is not todo at this psition")

def quit():
    print("bye")
    sys.exit(0)


mappings = {
    "stocks": stock_funct,
    "todoshow": todo_show,
    "todoadd": todo_add,
    "todoremov": todo_remove,
    "exit": quit
}
assistenn = GenericAssistant('intents.json', mappings)
assistenn.train_model()
assistenn.save_model()

while True:
    massage = input("massage: ")
    assistenn.request(massage)





