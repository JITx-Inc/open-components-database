#!/usr/bin/env bash
set -e

echo "Launching ocdb tests, they can depend on jitx-client..."
cd open-components-database
jitx run-test tests/test-stm-pin-parsing.stanza
cd ..

echo "Launching ocdb designs..."
cd open-components-database/designs
# Explicitly exclude tutorial.stanza and mcu.stanza because they query octopart more
designs=(ble-mote.stanza
         class-a.stanza
         ethernet-fmc.stanza
         smd-landpatterns.stanza
         test-component-checks.stanza
         voltage-divider.stanza)

for filename in "${designs[@]}"; do
    echo "Running $filename..."
    jitx run $filename
done
cd ../..

echo "Searching for pcb objects and generating tests..."
python3.8 scripts/evaluate_pcb_objects.py
cd test-evaluate/
echo "Launching pcb object tests..."
jitx run-test test/evaluate/api
