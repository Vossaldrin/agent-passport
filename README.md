# Agent Passport

**Secure identity + autonomous payments for AI agents.**

Gives your AI agents a cryptographic passport and smart wallet so they can operate independently with rules, limits, and real x402 payments.

## Features
- Verifiable Agent Identity
- Programmable spending rules & daily limits
- Real x402 autonomous payments
- Multi-chain support (Base, Ethereum, Arbitrum, etc.)
- ERC-8004 on-chain identity ready

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python -m agent_passport create "MyAgent" --chain base-sepolia
python -m agent_passport pay https://api.example.com/data 2.5 --description "Fetch data"
