import requests
import pandas as pd
import asyncio
import aiohttp

class DexScreenerClient:
    BASE_URL = "https://api.dexscreener.com/latest/dex"

    @staticmethod
    def get_token_profile(chain, address):
        """Mengambil data detail token"""
        try:
            url = f"{DexScreenerClient.BASE_URL}/tokens/{address}"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            if data.get('pairs'):
                return data['pairs'][0] # Ambil pair paling liquid
            return None
        except Exception as e:
            return None

    @staticmethod
    def search_pairs(query):
        """Mencari token/pair berdasarkan query"""
        try:
            url = f"{DexScreenerClient.BASE_URL}/search?q={query}"
            resp = requests.get(url, timeout=10)
            return resp.json().get('pairs', [])
        except:
            return []

    @staticmethod
    def get_top_boosted():
        """Mengambil token yang sedang trending/boosted (Simulasi Top 10k activity)"""
        # DexScreener tidak punya endpoint 'all tokens' sederhana, kita gunakan search umum
        # atau hardcode beberapa token populer untuk demo
        popular = ["SOL", "ETH", "BTC", "PEPE", "BONK", "WIF"]
        results = []
        for p in popular:
            pairs = DexScreenerClient.search_pairs(p)
            if pairs:
                results.append(pairs[0])
        return results

async def fetch_pair_data_async(pairs):
    """Async fetch untuk performa tinggi"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for pair in pairs:
            url = f"https://api.dexscreener.com/latest/dex/pairs/{pair['chainId']}/{pair['pairAddress']}"
            tasks.append(session.get(url))
        responses = await asyncio.gather(*tasks)
        return [await r.json() for r in responses]
