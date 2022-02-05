# SPICE plan

SPICE format: 
_# net .. net parameter=# .. parameter=#

Assumptions: components and nets only, no parameters

Done:
- Generalize circuit imports by prefix
- Start with simple netlist - only component portion, only 2 pin components, no parameters
- Handled nets consisting of only numbers
Doing:
- Add multi-pin components and component type parameter (npm)
- Add parameters to ignore
- Add the commands and comments

Netlist:
```
R3 vcc intc
R1 vcc intb
R2 intb 0
Cout out intc
Cin intb in
```

Netlist:
```
R3 vcc intc 10k
R1 vcc intb 68k
R2 intb 0 10k
Cout out intc 10u
Cin intb in 10u
```
Netlist:
```
R3 vcc intc 10k
R1 vcc intb 68k
R2 intb 0 10k
Cout out intc 10u
Cin intb in 10u
mn0		drain gate gnd gnd 	nmos
```
Netlist:
```
Rmd 134 57 1.5 k noisy =0
mn0		drain gate gnd gnd 	nmos	W=1u L=45n
```


First letter 	 Element description  
A 	 XSPICE code model 
B 	 Behavioral (arbitrary) source  
C 	 Capacitor  
D 	 Diode  
E 	 Voltage-controlled voltage source (VCVS) 
F 	 Current-controlled current source (CCCs)  
G 	 Voltage-controlled current source (VCCS) 
H 	 Current-controlled voltage source (CCVS)  
I 	 Current source  
J 	 Junction field effect transistor (JFET) 
K 	 Coupled (Mutual) Inductors  
L 	 Inductor  
M  	Metal oxide field effect transistor (MOSFET)  
N 	 Numerical device for GSS  
O 	 Lossy transmission line  
P 	 Coupled multiconductor line (CPL)  
Q 	 Bipolar junction transistor (BJT)  
R 	 Resistor  
S 	 Switch (voltage-controlled)  
T 	 Lossless transmission line  
U 	 Uniformly distributed RC line  
V 	 Voltage source  
W 	 Switch (current-controlled)  
X 	 Subcircuit  
Y 	 Single lossy transmission line (TXL)  
Z  	Metal semiconductor field effect transistor (MESFET) 
