#!/usr/bin/env bash
set -e

echo "Installation details"

jitx version
jitx check-install

echo "/root/.jitx/user.params:"
cat /root/.jitx/user.params

# Tests need to take into account the root stanza.proj so that they find the source files from the ocdb repo and not a pkg from the jitx-client docker image
export JITX_RUN="jitx run /app/open-components-database/stanza.proj"
export JITX_RUN_TEST="jitx run-test /app/open-components-database/stanza.proj"

#==============================================
#=========== Component Models test ============
#==============================================
echo "Checking that ocdb/components files conform \
      to spec and compile."
scripts/gen-components-file.sh
jitx run components.stanza

#==============================================
#==== public pcb-* macro evaluation tests =====
#==============================================

echo "Searching for pcb objects and generating tests..."
python3.8 scripts/evaluate_pcb_objects.py
cd test-evaluate/
echo "Launching pcb object tests..."
$JITX_RUN_TEST test/evaluate/api
cd ..

#==============================================
#================= Unit-tests =================
#==============================================

echo "Launching ocdb tests, they can depend on jitx-client..."
cd open-components-database
$JITX_RUN_TEST tests/test-ocdb.stanza
cd ..

#==============================================
#============= Integration tests ==============
#==============================================

echo "Launching ocdb designs..."
cd open-components-database/designs
# tutorial.stanza and mcu.stanza use part sourcing more
designs=(tutorial.stanza
         ble-mote.stanza
         mcu.stanza
         class-a.stanza
         ethernet-fmc.stanza
         smd-landpatterns.stanza
         test-component-checks.stanza
         voltage-divider.stanza)

for filename in "${designs[@]}"; do
    echo "Running $filename..."
    $JITX_RUN $filename
done
cd ../..

