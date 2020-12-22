#!/bin/bash
admin="tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
echo "COMPILING"
~/smartpy-cli/SmartPy.sh compile ./Dutch.py "DutchAuction(sp.address(\"$admin\"))" ./smartpy_generated/dutch_auction/
~/smartpy-cli/SmartPy.sh compile ./Dutch.py "NFTWallet(sp.address(\"$admin\"))" ./smartpy_generated/nft_wallet/
#~/smartpy-cli/SmartPy.sh compile ./Dutch.py "Viewer(sp.TBytes)" ./smartpy_generated/
echo "TESTING"
~/smartpy-cli/SmartPy.sh test ./Dutch.py ./smartpy_generated/
