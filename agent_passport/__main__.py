from agent_passport.agent_passport import AgentPassport

if __name__ == "__main__":
    p = AgentPassport("Agent47", "0xb9e40ca9211ec0aaed58550af3a5443691ddd733a72058099dcb011cd78a04b4")
    p.display()
    p.mint_onchain()
