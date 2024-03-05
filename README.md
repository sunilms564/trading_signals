TradeSignalAnalyzer

Overview

The TradeSignalAnalyzer project is designed to analyze stock data and generate trading signals based on specific conditions. It calculates overall profit and loss for each stock based on the generated signals and visualizes trading data and signal-related transactions.

Setup and Execution Instructions

Note
This project does not utilize a PostgreSQL database. since I had faced problem in istalling software because of my old laptop Instead, the provided stock equities data is loaded directly within the Python script.
git clone https://github.com/sunilms564/TradeSignalAnalyzer.git

data/: Directory containing stock equities data files.
scripts/: Directory containing Python scripts for analyzing stock data and generating trading signals.
README.md: This file providing setup and execution instructions.
Signal Logic
A buy signal is generated if there's a crossover of the 50-day and 500-day moving averages.

A sell signal is generated if there's a crossover of the 20-day and 200-day moving averages.

Existing buy positions are closed if a crossover of the 10-day and 20-day moving averages takes place.

Existing sell positions are closed if a crossover of the 5-day and 10-day moving averages takes place.

Visualization
The project uses matplotlib for visualizing trading data and signal-related transactions.


Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests with any improvements or features.

