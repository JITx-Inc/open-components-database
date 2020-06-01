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

instead of  

```stanza
pad p[1] : {smd-pad(0.55, 0.45)} at loc(0.0, 0.5) 
pad p[2] : {smd-pad(0.55, 0.45)} at loc(0.5, 0.0)
```

#### Use unified generator to create pins where possible
```stanza
port p1 : pin[{1 through 4}]
port p2 : pin[{5 7 9}]
```

instead of  

```stanza
pin p[1]
pin p[2]
pin p[3]
pin p[4]
pin p[5]
pin p[7]
pin p[9]
```

#### Define pins or ports to externally interface with other modules
```stanza
pcb-bundle rgb-led :
  pin r
  pin g
  pin b
  pin a

public unique pcb-module lower-level-module :
  port rgb-led : rgb-led 
  pin vcc

  inst r-res : {gen-res-cmp(470.0)}
  inst g-res : {gen-res-cmp(330.0)}
  inst b-res : {gen-res-cmp(100.0)}

  net (rgb-led.r, r-res.p[2])
  net (rgb-led.g, g-res.p[2])
  net (rgb-led.b, b-res.p[2])
  net (vcc, rgb-led.a)

public unique pcb-module top-level-module :
  inst lower : lower-level-module
  inst r : {gen-res-cmp(100.0)}
  net (lower.rgb-led.r, r.p[1])
```

instead of 

```stanza
public unique pcb-module lower-level-module :
  pin r
  pin g
  pin b
  pin a
  pin vcc

  inst r-res : {gen-res-cmp(470.0)}
  inst g-res : {gen-res-cmp(330.0)}
  inst b-res : {gen-res-cmp(100.0)}

  net r (r-res.p[2])
  net g (g-res.p[2])
  net b (b-res.p[2])
  net vcc (a)

public unique pcb-module top-level-module :
  inst lower : lower-level-module
  inst r : {gen-res-cmp(100.0)}
  net (lower.r, r.p[1])
```

#### Use the grid-locs function to create locations at grids of m rows by n columns spaced dx apart horizontally and dy apart vertically. Locations are ordered left to right row by row.  
1 2 3  
4 5 6  
7 8 9  
```stanza
for (l in grid-locs(2, 2, 3.0, 1.3), i in [4 3 1 2]) do :
  pad p[i] : {smd-pad(1.0, 0.6)} at l
```

instead of

```stanza
val xoff = 1.5
val yoff = 0.65
val xdim = 1.0
val ydim = 0.6
pad p[1] : {smd-pad(xdim, ydim)} at loc((- xoff), (- yoff))
pad p[2] : {smd-pad(xdim, ydim)} at loc(xoff, (- yoff))
pad p[3] : {smd-pad(xdim, ydim)} at loc(xoff, yoff)
pad p[4] : {smd-pad(xdim, ydim)} at loc((- xoff), yoff)
```

#### Ensure all packages have a courtyard
```stanza
layer(Courtyard(Top)) = Rectangle(8.62, 3.03)
layer(Silkscreen("f-silk", Top)) = Rectangle(8.62, 3.03)
```

#### Ensure all pads remain fully within the courtyard
![comp](fig/style-guide-01.png)

instead of  

![comp](fig/style-guide-02.png)

