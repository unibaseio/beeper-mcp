# beeper-mcp

A backend service for executing beeper transactions on Binance Smart Chain (BSC). This service provides a set of tools for interacting with the BSC blockchain, including balance checking, token transfers, and token swaps.

## Features

- Get BNB and token balances
- Transfer BNB and tokens
- Swap tokens over Pancakeswap
- Get token prices
- Buy and sell tokens
- Claim rewards of beeper tokens

## Prerequisites

- Python >=3.10
- Access to BSC network (mainnet or testnet)
- Wallet account and private key

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
MEMBASE_CHAIN=<bsc or bsc-testnet>
MEMBASE_ACCOUNT=<your-wallet-address>
MEMBASE_SECRET_KEY=<your-private-key>
```

## API Endpoints

The service exposes the following MCP tools:

### Balance Operations
- `get_balance(address: str) -> float`: Get BNB balance of an address
- `get_token_balance(address: str, token_address: str) -> float`: Get token balance of an address

### Transfer Operations
- `transfer(recipient_address: str, amount: Decimal = 0.01) -> int`: Transfer BNB to an address
- `transfer_token(recipient_address: str, token_address: str, amount: Decimal = 0.01) -> int`: Transfer tokens to an address

### Trading Operations
- `swap_token(token_in: str, token_out: str, amount: Decimal = 0.01) -> int`: Swap between tokens
- `get_token_price(token_address: str) -> float`: Get token price in BNB
- `buy_token(token_address: str, amount: Decimal = 0.01) -> int`: Buy tokens with BNB
- `sell_token(token_address: str, amount: Decimal = 0.01) -> int`: Sell tokens for BNB

### Reward Operations
- `claim_rewards(token_address: str)`: Claim rewards for a token

## Running the Service

```bash
git clone https://github.com/unibaseio/beeper-mcp.git
cd beeper-mcp
# start server over sse
uv run src/beeper_mcp/server.py
```

The service will start on port 8008 by default.

### Configuration on Claude/Windsurf/Cursor/Cline

```json
{
  "mcpServers": {
    "beeper":{
      "transport": "sse",
      "url": "http://127.0.0.1:8008/sse"
    } 
  }
}
```

## Notes

- All amounts are in native units (e.g., BNB, tokens)
- Token addresses should be provided in the correct format
- Make sure you have sufficient BNB for gas fees
- The service supports both BSC mainnet and testnet
