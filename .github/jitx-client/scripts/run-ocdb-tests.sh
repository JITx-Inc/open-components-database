#!/usr/bin/env bash
set -e

echo "Searching for components and generating tests..."
python3.8 scripts/evaluate_components.py
cd test-evaluate/
echo "Launching component tests..."
jitx run-test test/evaluate-components
