#!/bin/bash -eu 
echo "defpackage ocdb/components :" > components.stanza
grep -rh  'defpackage ocdb/components/.*\s*:' components |\
    sed 's/://g' |\
    sort -k 2 |\
    sed 's/defpackage/  import/g' >> components.stanza
