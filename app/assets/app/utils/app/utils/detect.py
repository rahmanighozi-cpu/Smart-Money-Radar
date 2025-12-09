import pandas as pd
import random

class WhaleDetector:
    
    @staticmethod
    def analyze_trades(trades_data):
        """
        Menganalisis list transaksi untuk mencari Whale.
        Data DexScreener tidak memberikan wallet address per trade di endpoint publik standar 
        secara detail historis, jadi kita mensimulasikan logika deteksi berdasarkan volume 
        yang tersedia di data pair.
        """
        whales = []
        
        # Simulasi data transaksi level wallet (karena limitasi API publik tanpa key)
        # Dalam production dengan node berbayar, ini diganti real on-chain data.
        if not trades_data:
            return pd.DataFrame()

        # Logika Deteksi
        for trade in trades_data:
            usd_value = float(trade.get('priceUsd', 0)) * float(trade.get('amount', 0))
            
            label = "Retail"
            if usd_value > 100000:
                label = "🐳 WHALE"
            elif usd_value > 10000:
                label = "🦈 Shark"
            elif usd_value > 5000:
                label = "🐬 Dolphin"
            
            if usd_value > 1000: # Filter remah-remah
                whales.append({
                    "Type": trade.get('type'),
                    "Price": float(trade.get('priceUsd', 0)),
                    "Amount": float(trade.get('amount', 0)),
                    "Value (USD)": usd_value,
                    "Label": label,
                    "Timestamp": trade.get('timestamp') # Biasanya perlu parsing
                })
                
        return pd.DataFrame(whales)

    @staticmethod
    def generate_dummy_wallet_labels():
        """Generate data dummy smart money untuk Leaderboard (Demo)"""
        wallets = []
        labels = ["Smart Money", "Insider", "Sniper Bot", "VC Fund", "Alpha Trader"]
        for i in range(20):
            wallets.append({
                "Wallet": f"0x{random.randint(10000,99999)}...{random.randint(1000,9999)}",
                "Label": random.choice(labels),
                "Win Rate": f"{random.randint(55, 95)}%",
                "PnL (30d)": f"+${random.randint(10000, 500000):,}",
                "Last Buy": random.choice(["PEPE", "WIF", "SOL", "LINK"]),
                "Status": random.choice(["Accumulating", "Dumping", "Holding"])
            })
        return pd.DataFrame(wallets)
