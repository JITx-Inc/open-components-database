#!/usr/bin/env bash
set -e

# check for any optional argument to run fewer tests (skip Octopart queries, for example)
if [[ $# -ne 0 ]]; then
    restrict=true
else
    restrict=false
fi

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
echo "Checking that ocdb/components files conform to spec and compile."
cd open-components-database
scripts/gen-components-file.sh
jitx run components.stanza
cd ..

#==============================================
#==== public pcb-* macro evaluation tests =====
#==============================================

echo "Searching for pcb objects and generating tests..."
python3.10 scripts/evaluate_pcb_objects.py
cd test-evaluate/
echo "Launching pcb object tests..."
$JITX_RUN_TEST test/evaluate/api
cd ..

#==============================================
#================= Unit-tests =================
#==============================================

echo "Launching ocdb tests, they can depend on jitx-client..."
cd open-components-database
$JITX_RUN_TEST tests/all.stanza -not-tagged part-query long not-implemented-yet
cd ..

#==============================================
#============= Integration tests ==============
#==============================================

echo "Launching ocdb designs..."
cd open-components-database/designs
designs=(ble-mote.stanza
         can-stm32.stanza
         class-a.stanza
         comprehensive-checks.stanza
         doc-examples.stanza
         ethernet-fmc.stanza
         grid-resistors.stanza
         lp-examples.stanza
         power-monitor.stanza
         # power-state-demo.stanza       # fails
         smd-landpatterns.stanza
         test-component-checks.stanza
         usb-accel.stanza
         usb-light.stanza          # no board?
         voltage-divider.stanza
         run-checks/checked-design.stanza)

# tutorial.stanza and mcu.stanza use part sourcing more
if [[ $restrict == false ]]; then
    designs+=(mcu.stanza tutorial.stanza)
fi

for filename in "${designs[@]}"; do
    echo "Running $filename..."
    $JITX_RUN $filename
done

cd ../..

