## Supply pin
This is a pin that supplies a voltage 

voltage:Double 
    - Nominal voltage (V)
voltage:Tuple [min:Double nom:Double max:Double]
    - minimum, nominal, and maximum DC voltage. Doesn't include transients.

## Power pin
Power input pin of a component

power-pin => true
- Identifier
vdd:Double (V)
- Nominal positive supply voltage relative to gnd
rated-voltage:[Double,Double] [min max] (V) 
- Voltage safety limits of power pin relative to gnd

## Single ended receiver
Single ended digital logic receiver

digital-io => true
- Identifier
vi:[Double,Double]
- [Input voltage low (V), Input voltage high (V)]
rated-voltage:[Double,Double] [min max] (V) 
- Voltage safety limits of power pin relative to gnd


# Components

## Generic
This properties apply to all components

temperature:Double
- Temperature of the component (degC)
theta-ja:Double
- Thermal resistance from junction to ambient
rated-temperature:[Toleranced] (degC) 
- Manufacturer rated temperature of component
model-trust:String
- How much do we trust this model?
    + "proxy"
    + "datasheet"

operating-point:Tuple<KeyValue<Symbol,?>>
- Key,Value store for operating point of component
- temperature:Double
    + Temperature of component
- voltage-pk:[Double,Double] [min max](V)
    + Voltage extrema across pin 1 and pin 2
- current-pk (A)
    + Peak current (absolute value)
- current-rms (A)
    + RMS current

## Resistor

resistor => true
- Identifier
type:String (classification of resistor)
- thick-film
- ...
resistance:Double
- Nominal resistance (ohms)
tolerance:Double
- Guaranteed tolerance from manufacturer ohms/ohm
rated-voltage:Double (V)
- Maximum voltage rating from manufacturer
rated-power:Double
- Power dissipation limit as rated by manufacturer (W)
rated-power:Tuple<Tuple<Double, Double>> [[degC, W]]
- Power dissipation limit  as rated by manufacturer 
TCR:Double
- Temperature coefficient of resistance (ohms/ohm*degC)

## Capacitor
capacitor => true
- Identifier
rated-voltage:Double (V)
- Maximum voltage rating from manufacturer
rated-current-pk:Double (A)
- Maximum peak current rating from manufacturer
rated-current-rms:PWL[Temp rms]
- Maximum rms current rating from manufacturer, based on temperature
capacitance:Double
- Nominal capacitance (Farads)
tolerance:Double
- Guaranteed tolerance from manufacturer F/F
type:String (classification of capacitor)
- ceramic
- film
- electrolytic
    + anode:String
        * aluminum
        * tantalum
        * niobium-oxide
    + electrolyte:String
        * polymer
        * manganese-oxide
        * hybrid
        * non-solid
bypass => true
- Indicates if capacitor is used for bypassing
