#!/bin/bash
admin="tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
echo "COMPILING"
~/smartpy-cli/SmartPy.sh compile ./Dutch.py "DutchAuction()" ./smartpy_generated/
echo "TESTING"
~/smartpy-cli/SmartPy.sh test ./Dutch.py "DutchAuction()"
