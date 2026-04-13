import time
import json
import argparse
from datetime import datetime, timedelta
from eth_account import Account

# x402
try:
    from x402 import x402ClientSync
    from x402.mechanisms.evm.exact import ExactEvmScheme
    from x402.http.clients import x402_requests
    X402_OK = True
except ImportError:
    X402_OK = False

class AgentPassport:
    def __init__(self, name: str, owner_private_key: str, daily_limit_usdc: int = 50):
        self.account = Account.from_key(owner_private_key)
        self.file_path = f"{name.lower()}_passport.json"
        self.x402_client = None

        if X402_OK:
            self.x402_client = x402ClientSync()
            self.x402_client.register("eip155:*", ExactEvmScheme(signer=self.account))
            print("🔐 x402 client ready with EVM signer")

        self.passport = {
            "passport_id": f"ap_{int(time.time())}",
            "name": name,
            "owner_address": self.account.address,
            "smart_wallet_address": self.account.address,
            "version": "0.6",
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "rules": {
                "max_daily_usdc": daily_limit_usdc,
                "allowed_actions": ["pay_api", "buy_data", "trade"],
                "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
                "chain": "Base Sepolia"
            },
            "usage": {
                "spent_today_usdc": 0,
                "last_reset_date": datetime.now().date().isoformat()
            }
        }

    def can_spend(self, amount: float) -> bool:
        today = datetime.now().date().isoformat()
        if self.passport["usage"]["last_reset_date"] != today:
            self.passport["usage"]["spent_today_usdc"] = 0
            self.passport["usage"]["last_reset_date"] = today
        return self.passport["usage"]["spent_today_usdc"] + amount <= self.passport["rules"]["max_daily_usdc"]

    def pay(self, url: str, amount: float, description: str = "Autonomous payment"):
        if not X402_OK:
            print("❌ x402 not available")
            return False
        if not self.can_spend(amount):
            print("❌ Daily limit exceeded!")
            return False

        print(f"🔄 Making x402 payment of ${amount} to {url}...")

        try:
            with x402_requests(self.x402_client) as session:
                response = session.get(url)
                print(f"✅ x402 Payment Successful! Status: {response.status_code}")
                self.passport["usage"]["spent_today_usdc"] += amount
                self.save()
                return True
        except Exception as e:
            print(f"❌ x402 Payment Failed: {e}")
            return False

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.passport, f, indent=2)

    def display(self):
        print("\n" + "="*70)
        print("🔖 AGENT PASSPORT")
        print("="*70)
        print(json.dumps(self.passport, indent=2))
        print("="*70)

def main_cli():
    parser = argparse.ArgumentParser(description="Agent Passport")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Create passport")
    create.add_argument("name", nargs="?", default="Agent47")

    pay = subparsers.add_parser("pay", help="Make x402 payment")
    pay.add_argument("url")
    pay.add_argument("amount", type=float)
    pay.add_argument("-d", "--description", default="Autonomous payment")

    args = parser.parse_args()

    if args.command == "create":
        key = input("Enter private key or press Enter for test: ") or "0xb9e40ca9211ec0aaed58550af3a5443691ddd733a72058099dcb011cd78a04b4"
        p = AgentPassport(args.name, key)
        p.display()
        p.save()

    elif args.command == "pay":
        p = AgentPassport("Agent47", "0xb9e40ca9211ec0aaed58550af3a5443691ddd733a72058099dcb011cd78a04b4")
        p.pay(args.url, args.amount, args.description)

if __name__ == "__main__":
    main_cli()
