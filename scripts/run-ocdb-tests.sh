#!/usr/bin/env bash
set -Eeuo pipefail

echo -e "\n\n--------------------------------------------------------------------------------"
echo "Remove TOML file"
echo "--------------------------------------------------------------------------------"
rm slm.toml
echo -e "\n\n--------------------------------------------------------------------------------"
echo "Check TOML file"
echo "--------------------------------------------------------------------------------"
cat slm.toml

#
# This script expects to be run from the `open-components-database` directory
#
if [ "$(basename $PWD)" != "open-components-database" ] ; then
    echo "Error: this script expects to be run from the open-components-database directory"
    exit -1
fi

#
# Defaulted env var inputs - can override if necessary
echo "             PYTHON:" "${PYTHON:=python}"

# check for any optional argument to run fewer tests (skip Octopart queries, for example)
if [[ $# -ne 0 ]]; then
    restrict=true
else
    restrict=false
fi

# Defaulted env var inputs - can override if necessary
echo "JITX_PLATFORM = \"${JITX_PLATFORM:=linux}\""
echo "JITPCB_VERSION = \"${JITPCB_VERSION:=current}\""

JITX_HOME="${HOME}/.jitx"
if [[ "$JITX_PLATFORM" = "windows" ]] ; then
  JITX_HOME="$USERPROFILE/.jitx"
fi
JITX_INSTALL_DIR="${JITX_HOME}/${JITPCB_VERSION}"
echo "JITX_INSTALL_DIR = \"${JITX_INSTALL_DIR}\""

JITX="${JITX_INSTALL_DIR}/jitx"
echo "JITX = \"${JITX}\""

echo -e "\n\n--------------------------------------------------------------------------------"
echo "Installation details"
echo "--------------------------------------------------------------------------------"

"${JITX}" version
"${JITX}" check-install

if [ -e ${JITX_HOME}/user.params ] ; then
  echo "${JITX_HOME}/user.params:"
  echo ----
  cat "${JITX_HOME}/user.params"
  echo ----
else
  echo "${JITX_HOME}/user.params does not exist"
fi

# Tests need to take into account the root stanza.proj so that they find the source files from the ocdb repo and not a pkg from the jitx-client docker image
JITX_RUN="${JITX} run ${PWD}/stanza.proj"  # i.e. open-components-database/stanza.proj
JITX_RUN_TEST="${JITX} run --flags TESTING ${PWD}/stanza.proj"

#==============================================
#=========== Component Models test ============
#==============================================
echo -e "\n\n--------------------------------------------------------------------------------"
echo "Checking that ocdb/components files conform to spec and compile."
echo "--------------------------------------------------------------------------------"
scripts/gen-components-file.sh
${JITX} run components.stanza
rm components.stanza

#==============================================
#==== public pcb-* macro evaluation tests =====
#==============================================
echo -e "\n\n--------------------------------------------------------------------------------"
echo "Searching for pcb objects and generating tests..."
echo "--------------------------------------------------------------------------------"
${PYTHON} scripts/evaluate_pcb_objects.py
(
cd test-evaluate/
echo -e "\n\n--------------------------------------------------------------------------------"
echo "Launching pcb object tests..."
echo "--------------------------------------------------------------------------------"
${JITX_RUN_TEST} test/evaluate/api
cd ..
)
rm -rf test-evaluate

#==============================================
#================= Unit-tests =================
#==============================================
echo -e "\n\n--------------------------------------------------------------------------------"
echo "Launching ocdb tests, they can depend on jitx-client..."
echo "--------------------------------------------------------------------------------"
${JITX_RUN_TEST} tests/all.stanza -not-tagged part-query long not-implemented-yet

#==============================================
#============= Integration tests ==============
#==============================================
echo -e "\n\n--------------------------------------------------------------------------------"
echo "Launching ocdb designs..."
echo -e "--------------------------------------------------------------------------------"
(
cd designs
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
    echo -e "\n\n--------------------------------------------------------------------------------"
    echo "Running $filename..."
    echo "--------------------------------------------------------------------------------"
    ${JITX_RUN} $filename
done

cd ..
)
