import pandas as pd
import matplotlib.pyplot as plt
import git
from datetime import datetime
import os
import zipfile
import numpy as np


# Extract files from the specified directory within the zip archive
def extract_zip(zip_file, extract_dir):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)


# Implement Signal Logic
def calculate_moving_average(data, window):
    return data['Close'].rolling(window=window).mean()


# Generate buy signals based on crossover of 50-day and 500-day moving averages
def generate_buy_signals(data):
    data['50_MA'] = data['Close'].rolling(window=50).mean()
    data['500_MA'] = data['Close'].rolling(window=500).mean()
    data['Buy_Signal'] = np.where(data['50_MA'] > data['500_MA'], 1, 0)
    return data


# Generate sell signals based on crossover of 20-day and 200-day moving averages
def generate_sell_signals(data):
    data['20_MA'] = data['Close'].rolling(window=20).mean()
    data['200_MA'] = data['Close'].rolling(window=200).mean()
    data['Sell_Signal'] = np.where(data['20_MA'] < data['200_MA'], 1, 0)
    return data


# Close any existing buy positions if a crossover of 10-day and 20-day moving averages takes place
def close_buy_positions(data):
    data['10_MA'] = data['Close'].rolling(window=10).mean()
    data['Close_Buy_Position'] = np.where(
        (data['10_MA'] < data['20_MA']) & (data['10_MA'].shift(1) > data['20_MA'].shift(1)), -1, 0)
    return data


# Close any existing sell positions if a crossover of 5-day and 10-day moving averages takes place
def close_sell_positions(data):
    data['5_MA'] = data['Close'].rolling(window=5).mean()
    data['Close_Sell_Position'] = np.where(
        (data['5_MA'] < data['10_MA']) & (data['5_MA'].shift(1) > data['10_MA'].shift(1)), 1, 0)
    return data


# Calculate Profit and Loss
def calculate_profit_loss(data):
    profit_loss = {}
    for symbol, stock_data in data.items():
        positions = []  # List to track buy positions
        total_profit_loss = 0  # Initialize total profit/loss for the stock

        # Iterate through each row of the DataFrame representing the stock data
        for index, row in stock_data.iterrows():
            # Buy signal detected and no existing positions
            if row['Buy_Signal'] == 1 and not positions:
                # Buy the stock and record transaction details
                buy_price = row['Close']
                quantity = 100  # Example: Buy 100 shares
                positions.append({'buy_price': buy_price, 'quantity': quantity})

            # Sell signal detected and existing buy positions
            elif row['Sell_Signal'] == 1 and positions:
                # Sell the stock and calculate profit/loss
                sell_price = row['Close']
                buy_transaction = positions.pop(0)  # Pop the first buy transaction
                buy_price = buy_transaction['buy_price']
                quantity = buy_transaction['quantity']
                total_profit_loss += (sell_price - buy_price) * quantity

        # Store the overall profit/loss for the stock
        profit_loss[symbol] = total_profit_loss

    return profit_loss


# Visualize Trading Data
def visualize_data(stock_data):
    num_stocks = len(stock_data)
    num_cols = 2  # Number of columns for subplots
    num_rows = (num_stocks + num_cols - 1) // num_cols

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, 8))

    for i, (symbol, data) in enumerate(stock_data.items()):
        row = i // num_cols
        col = i % num_cols
        ax = axs[row, col] if num_stocks > 1 else axs  # Handle single plot case

        ax.plot(data['Date'], data['Close'], label='Close Price', color='black')
        ax.scatter(data[data['Buy_Signal'] == 1]['Date'], data[data['Buy_Signal'] == 1]['Close'], marker='^',
                   color='green', label='Buy Signal')
        ax.scatter(data[data['Sell_Signal'] == 1]['Date'], data[data['Sell_Signal'] == 1]['Close'], marker='v',
                   color='red', label='Sell Signal')
        ax.set_title(f"Stock {symbol} - Buying and Selling Details")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend()
        ax.grid(True)
        ax.tick_params(axis='x', rotation=30)  # Rotate x-axis labels

    plt.tight_layout()
    plt.show()


# Version Control with Git
def commit_changes():
    repo = git.Repo('.')
    repo.git.add('.')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    repo.index.commit(f"Changes committed at {timestamp}")


def write_to_csv(profit_loss, output_file):
    df = pd.DataFrame(profit_loss.items(), columns=['Symbol', 'Profit/Loss'])
    df.to_csv(output_file, index=False)


# Main function
def main():
    # Extract files from the specified directory within the zip archive
    zip_file = 'stock_details.zip'
    extract_dir = 'data'  # Specify the directory within the zip archive containing CSV files
    extract_zip(zip_file, extract_dir)

    # Get list of stock data files
    stock_files = [os.path.join(extract_dir, file) for file in os.listdir(extract_dir) if file.endswith('.csv')]

    # Check if there are any CSV files
    if not stock_files:
        print("No CSV files found in the directory.")
        return

    # Dictionary to store stock data
    stock_data = {}

    # Load stock data and generate signals for each stock
    for stock_file in stock_files:
        symbol = os.path.basename(stock_file).split('.')[0]
        stock_data[symbol] = pd.read_csv(stock_file)
        stock_data[symbol] = generate_buy_signals(stock_data[symbol])
        stock_data[symbol] = generate_sell_signals(stock_data[symbol])
        stock_data[symbol] = close_buy_positions(stock_data[symbol])
        stock_data[symbol] = close_sell_positions(stock_data[symbol])

        # Calculate profit/loss
        profit_loss = calculate_profit_loss(stock_data)
        output_file = 'profit_loss.csv'

    # Write results to CSV
    write_to_csv(profit_loss, output_file)

    print("Overall profit/loss for each stock has been calculated and saved to:", output_file)

    # Print overall profit/loss for each stock
    for symbol, profit_loss in stock_profit_loss.items():
        print(f"Stock {symbol}: Overall Profit/Loss: {profit_loss}")

    # Visualize data
    # visualize_data(stock_data)

    # Commit changes
    commit_changes()


if __name__ == "__main__":
    main()
