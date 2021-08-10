#!/usr/bin/env bash
set -e

echo "Launching ocdb tests, they can depend on jitx-client..."
cd open-components-database
jitx run-test tests/test-ocdb.stanza
cd ..

echo "Searching for pcb objects and generating tests..."
python3.8 scripts/evaluate_pcb_objects.py
cd test-evaluate/
echo "Launching pcb object tests..."
jitx run-test test/evaluate/api
