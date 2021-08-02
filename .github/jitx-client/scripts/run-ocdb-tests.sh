#!/usr/bin/env bash
set -e

echo "Launching ocdb tests depending on jitx-client..."
jitx run-test open-components-database/tests/test-stm-pin-parsing.stanza

echo "Searching for pcb objects and generating tests..."
python3.8 scripts/evaluate_pcb_objects.py
cd test-evaluate/
echo "Launching pcb object tests..."
jitx run-test test/evaluate/api
