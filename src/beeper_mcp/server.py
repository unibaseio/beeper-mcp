import argparse
import asyncio
import logging
import os

from decimal import ROUND_DOWN, Decimal
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from membase.chain.beeper import BeeperClient
from membase.chain.util import BSC_MAINNET_SETTINGS, BSC_TESTNET_SETTINGS
from web3 import Web3

load_dotenv()

mcp = FastMCP(
    "Beeper MCP Server", port=8008
)

chain = os.getenv("MEMBASE_CHAIN")
logging.info(f"Chain: {chain}")

if chain == "bsc":
    chain_settings = BSC_MAINNET_SETTINGS
elif chain == "bsc-testnet":
    chain_settings = BSC_TESTNET_SETTINGS
else:
    raise ValueError(f"Invalid chain: {chain}, must be one of: bsc, bsc-testnet")

wallet_account = os.getenv("MEMBASE_ACCOUNT")
if not wallet_account:  
    raise ValueError("MEMBASE_ACCOUNT is not set")

logging.info(f"Wallet account: {wallet_account}")

wallet_private_key = os.getenv("MEMBASE_SECRET_KEY")
if not wallet_private_key:
    raise ValueError("MEMBASE_SECRET_KEY is not set")

def format_decimal(value, decimal_places=8):
    """
    Formats a Decimal to a specified number of decimal places,
    removes trailing zeros, and avoids scientific notation.
    """

    value = Web3.from_wei(value, 'ether')

    # Ensure input is a Decimal
    if not isinstance(value, Decimal):
        value = Decimal(value)
    
    # Define the quantization level
    quantize_level = Decimal(f"1.{'0' * decimal_places}")
    # Quantize to the required decimal places
    formatted_value = value.quantize(quantize_level, rounding=ROUND_DOWN)
    # Convert to string, remove trailing zeros, and avoid scientific notation
    return f"{formatted_value:.{decimal_places}f}".rstrip("0").rstrip(".")


bc = None

@mcp.tool()
def get_balance(address: str) -> float:
    """Get the balance of an address"""
    global bc
    balance = bc.get_balance(address, "")
    return format_decimal(balance / 10**18)

@mcp.tool()
def get_token_balance(address: str, token_address: str) -> float:
    """Get the token balance of an address"""
    global bc
    balance = bc.get_balance(address, token_address)
    return format_decimal(balance / 10**18)

@mcp.tool()
def transfer(recipient_address: str, amount: Decimal = 0.01) -> int:
    """Transfer BNB to an address with amount"""
    global bc
    amount = int(amount * 10**18)
    return bc.transfer_asset(recipient_address, "", amount)

@mcp.tool()
def transfer_token(recipient_address: str, token_address: str, amount: Decimal = 0.01) -> int:
    """Transfer token to an address with amount"""
    global bc
    amount = int(amount * 10**18)
    return bc.transfer_asset(recipient_address, token_address, amount)

@mcp.tool()
def swap_token(token_in: str, token_out: str, amount: Decimal = 0.01) -> int:
    """Swap token_in to token_out with amount of token_in"""
    global bc
    amount = int(amount * 10**18)
    return bc.make_trade(token_in, token_out, amount)

@mcp.tool()
def get_token_price(token_address: str) -> float:
    """Get the estimated price of a token in BNB"""
    global bc
    return bc.get_raw_price(token_address, "")

@mcp.tool()
def buy_token(token_address: str, amount: Decimal = 0.01) -> int:
    """Buy token with amount of BNB"""
    global bc
    amount = int(amount * 10**18)
    return bc.make_trade("", token_address, amount)

@mcp.tool()
def sell_token(token_address: str, amount: Decimal = 0.01) -> int:
    """Sell amount of token"""
    global bc
    amount = int(amount * 10**18)
    return bc.make_trade(token_address, "", amount)

@mcp.tool()
def claim_rewards(token_address: str):
    """Claim rewards"""
    global bc
    return bc.claim_reward(token_address)

def main():
    logging.info(f"Creating BeeperClient")
    global bc
    bc = BeeperClient(chain_settings, wallet_account, wallet_private_key, False, None)
    logging.info(f"Starting Beeper MCP Server")

    mcp.run(transport="sse")

if __name__ == "__main__":
    main()