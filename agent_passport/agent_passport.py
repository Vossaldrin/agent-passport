import time
import json
import argparse
from datetime import datetime, timedelta
from eth_account import Account
from web3 import Web3

# Chain configurations
CHAINS = {
    "base-sepolia": {"name": "Base Sepolia", "rpc": "https://sepolia.base.org", "chain_id": 84532},
    "base": {"name": "Base", "rpc": "https://mainnet.base.org", "chain_id": 8453},
    "ethereum": {"name": "Ethereum", "rpc": "https://eth.llamarpc.com", "chain_id": 1},
    "arbitrum": {"name": "Arbitrum", "rpc": "https://arb1.arbitrum.io/rpc", "chain_id": 42161},
}

class AgentPassport:
    def __init__(self, name: str, owner_private_key: str, daily_limit_usdc: int = 50, chain: str = "base-sepolia"):
        self.account = Account.from_key(owner_private_key)
        self.chain_config = CHAINS.get(chain.lower(), CHAINS["base-sepolia"])
        self.w3 = Web3(Web3.HTTPProvider(self.chain_config["rpc"]))

        self.file_path = f"{name.lower()}_passport.json"

        self.passport = {
            "passport_id": f"ap_{int(time.time())}",
            "name": name,
            "owner_address": self.account.address,
            "smart_wallet_address": self.account.address,
            "onchain_token_id": None,
            "version": "0.8",
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "chain": self.chain_config["name"],
            "chain_id": self.chain_config["chain_id"],
            "rules": {
                "max_daily_usdc": daily_limit_usdc,
                "allowed_actions": ["pay_api", "buy_data", "trade"],
                "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
            },
            "usage": {"spent_today_usdc": 0, "last_reset_date": datetime.now().date().isoformat()}
        }
        print(f"✅ Agent Passport initialized: {name} on {self.chain_config['name']}")

    def mint_onchain(self):
        print(f"\n🔗 Attempting to mint ERC-8004 Identity on {self.chain_config['name']}...")
        print("   → Preparing verifiable Agent Identity NFT")

        # Simulation for now (real minting requires deployed contract)
        self.passport["onchain_token_id"] = f"erc8004_{int(time.time())}"
        self.save()

        print("✅ ERC-8004 Identity successfully marked as minted!")
        print(f"   Token ID: {self.passport['onchain_token_id']}")
        print("   (Full smart contract deployment coming next)")

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.passport, f, indent=2)

    def display(self):
        print("\n" + "="*70)
        print("🔖 AGENT PASSPORT — ERC-8004 ENABLED")
        print("="*70)
        print(json.dumps(self.passport, indent=2))
        print("="*70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs="?", default="Agent47")
    parser.add_argument("--chain", default="base-sepolia", choices=CHAINS.keys())
    args = parser.parse_args()

    p = AgentPassport(args.name, "0xb9e40ca9211ec0aaed58550af3a5443691ddd733a72058099dcb011cd78a04b4", chain=args.chain)
    p.display()
    p.mint_onchain()
