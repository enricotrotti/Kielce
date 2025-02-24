# Importazione delle librerie necessarie
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Definire i titoli del portafoglio
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']  # Sostituisci con i ticker che desideri
start_date = "2018-01-01"
end_date = "2023-01-01"

# 1. Scarica i dati storici
data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

# 2. Calcolo dei rendimenti giornalieri e della matrice di covarianza
returns = data.pct_change().dropna()  # Rendimenti giornalieri
mean_returns = returns.mean()  # Rendimento medio di ciascun titolo
cov_matrix = returns.cov()  # Matrice di covarianza dei rendimenti

# Funzione per il calcolo della volatilità del portafoglio
def portfolio_volatility(weights, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

# Funzione per il calcolo del rendimento atteso del portafoglio
def portfolio_return(weights, mean_returns):
    return np.dot(weights, mean_returns)

# 3. Ottimizzazione del portafoglio con il modello di Markowitz
# Definire i vincoli e la funzione obiettivo per la minimizzazione della volatilità
def objective(weights):
    return portfolio_volatility(weights, cov_matrix)

# Vincoli: somma dei pesi deve essere 1
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
# Limiti: ogni peso deve essere tra 0 e 1
bounds = tuple((0, 1) for _ in range(len(tickers)))

# Pesi iniziali
initial_weights = np.array(len(tickers) * [1. / len(tickers)])

# Risolvi l'ottimizzazione
optimized = minimize(objective, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)

# Pesi ottimali
optimal_weights = optimized.x
print("Pesi ottimali per il portafoglio: ", optimal_weights)

# Rendimento e volatilità del portafoglio ottimizzato
opt_portfolio_return = portfolio_return(optimal_weights, mean_returns)
opt_portfolio_volatility = portfolio_volatility(optimal_weights, cov_matrix)
print("Rendimento atteso del portafoglio ottimizzato: ", opt_portfolio_return)
print("Volatilità del portafoglio ottimizzato: ", opt_portfolio_volatility)

# 4. Simulazione Monte Carlo
num_simulations = 10000
results = np.zeros((3, num_simulations))

for i in range(num_simulations):
    weights = np.random.random(len(tickers))
    weights /= np.sum(weights)  # Normalizzare i pesi
    port_return = portfolio_return(weights, mean_returns)
    port_volatility = portfolio_volatility(weights, cov_matrix)
    results[0,i] = port_volatility
    results[1,i] = port_return
    results[2,i] = port_return / port_volatility  # Rapporto di Sharpe

# 5. Calcolo del Value at Risk (VaR) usando il metodo storico
confidence_level = 0.05  # ad esempio per il 5% di confidenza
portfolio_values = np.dot(returns, optimal_weights)
VaR = np.percentile(portfolio_values, 100 * confidence_level)
print(f"Value at Risk (VaR) a livello di confidenza {confidence_level * 100}%: {VaR}")

# 6. Visualizzazione dei Risultati

# Diagramma della frontiera efficiente
plt.scatter(results[0,:], results[1,:], c=results[2,:], cmap='YlGnBu', marker='o')
plt.title('Frontiera Efficiente Monte Carlo')
plt.xlabel('Volatilità')
plt.ylabel('Rendimento Atteso')
plt.colorbar(label='Rapporto di Sharpe')
plt.scatter(opt_portfolio_volatility, opt_portfolio_return, color='red', marker='*', s=200)  # Portafoglio ottimale
plt.show()

