#!/usr/bin/env python3
"""
Mini client Bitcoin en Python (style Multibit)
- Génère un wallet
- Récupère solde via Electrum API publique
- Envoie une transaction signée

ATTENTION: utilisez TESTNET pour vos essais !
"""

from bitcoinlib.wallets import Wallet
import requests

ELECTRUMX_URL = "https://blockstream.info/testnet/api"  # testnet par défaut

class MiniMultibit:
    def __init__(self, name="MiniWallet", network="testnet"):
        self.network = network
        try:
            self.wallet = Wallet(name)
        except:
            self.wallet = Wallet.create(name, network=network)

    def new_address(self):
        addr = self.wallet.get_key().address
        print("Nouvelle adresse:", addr)
        return addr

    def balance(self):
        addr = self.wallet.get_key().address
        r = requests.get(f"{ELECTRUMX_URL}/address/{addr}")
        data = r.json()
        funded = data['chain_stats']['funded_txo_sum']
        spent = data['chain_stats']['spent_txo_sum']
        balance = (funded - spent) / 1e8
        print(f"Adresse: {addr}\nBalance: {balance} tBTC")
        return balance

    def send_to(self, to_addr, amount_btc, fee=1000):
        """
        Envoie une transaction testnet
        amount_btc en BTC (float)
        fee en satoshis
        """
        tx = self.wallet.send_to(to_addr, amount_btc, fee=fee)
        print("TX envoyée:", tx.txid)
        return tx.txid


if __name__ == "__main__":
    client = MiniMultibit()

    print("1. Créer nouvelle adresse")
    addr = client.new_address()

    print("\n2. Vérifier le solde")
    client.balance()

    # Exemple pour envoyer :
    # client.send_to("tb1q....", 0.0001)
