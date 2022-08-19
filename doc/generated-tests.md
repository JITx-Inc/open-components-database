# Generated macro validity testing on pull requests

Search for public `pcb-*` macros with 0 or 1 argument of primitive type and make a deftest for each with `print-def` to evaluate them.
Tests for `pcb-module` are not run in this v1 because they can require access to the online part database and take longer to run.

If no annotation is present, default values used are:
```
TYPE_SAMPLE = {
    "Char": '"c"',
    "String": '"hello world"',
    "Byte": '1Y',
    "Int": '1',
    "Long": '1L',
    "Float": '1.0F',
    "Double": '1.0',
    "True|False": 'true'
}
```

The syntax to specify the value to test a macro on is exemplified by:
```
;<test>
n-pins: value1 value2 value3
<test>
public pcb-component component (n-pins:Int) :
```
In this example 3 tests will be generated:
```
deftest test-ocdb_amphenol_minitek127_component:
  print-def(ocdb/components/amphenol/minitek127/component(value1))

deftest test-ocdb_amphenol_minitek127_component:
  print-def(ocdb/components/amphenol/minitek127/component(value2))

deftest test-ocdb_amphenol_minitek127_component:
  print-def(ocdb/components/amphenol/minitek127/component(value3))
```

To use a random even integer between 2 and 100 use:
```
;<test>
n: even positive
<test>
public pcb-landpattern soic127p-landpattern (n:Int) :
```

To skip a test do:
```
;<test>skip
n-pins: value1 value2 value3
<test>
public pcb-component component (n-pins:Int) :
```
or
```
;<test>skip<test>
public pcb-component component :
```
