#!/usr/bin/env bash
set -e

echo "Installation details"

jitx version
jitx check-install

echo "/root/.jitx/user.params:"
cat /root/.jitx/user.params

#==============================================
#==== public pcb-* macro evaluation tests =====
#==============================================

# Those macro evaluation tests take into account the root stanza.proj as it is included in the generated test-evaluate/stanza.proj
echo "Searching for pcb objects and generating tests..."
python3.8 scripts/evaluate_pcb_objects.py
cd test-evaluate/
echo "Launching pcb object tests..."
jitx run-test test/evaluate/api
cd ..

#==============================================
#====== Unit-tests and integration-tests ======
#==============================================

# Those tests need to take into account the root stanza.proj so that they find the source files from the ocdb repo and not a pkg from the jitx-client docker image
export STANZA_CONFIG=/app/open-components-database/

echo "Launching ocdb tests, they can depend on jitx-client..."
cd open-components-database
jitx run-test tests/test-ocdb.stanza
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

