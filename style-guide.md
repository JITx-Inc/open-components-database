# Style Guide

#### Include a space before colon in definition
```stanza
defpackage mydefinition :
```

#### Assign repetitive code to variables
```stanza
val smd-pad = smd-pad(0.55, 0.45)
pad p[1] : {smd-pad} at loc(0.0, 0.5) 
pad p[2] : {smd-pad} at loc(0.5, 0.0)
```

#### Group together pins that can be easily named where it makes sense 
```stanza
pcb-bundle leds :
  pin r
  pin g
  pin b

```

#### Use unified generator to create pins where possible
```stanza
port leds : leds
port p1 : pin[{1 through 4}]
port p2 : pin[{1 3 5}]
```

#### Define pins or ports to externally interface with other modules
```stanza
pcb-bundle leds :
  pin r
  pin g
  pin b

public unique pcb-module lower-level-module :
  port leds : leds
  pin vcc

  inst r-res
  inst g-res
  inst b-res

  net (leds.r, r-res.p[2]) 
  net (leds.g, g-res.p[2])
  net (leds.b, b-res.p[2])

public pcb-module top-level-module :
  inst lower : lower-level-module
  inst r : {gen-res-cmp(100.0)}
  net (lower.leds.r, r.p[1])
```
