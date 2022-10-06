# Open Component Database
 
This is an open database of components and circuit generators for automated circuit board design. Think of it as a software library for electrical engineering. We welcome contributions of component models, as well as parametric circuit generators. If you contribute to this library your expert hardware engineering knowledge becomes reusable and sharable, having the same impact as open-source software.

Components are modeled with the standardized open-source Electronic Systems Intermediate Representation (ESIR) developed by JITX for the national Electronic Resurgence Initiative.

# Organization
| File/Folder   | Description |
| ------------- |-------------|
| `artwork/`      | Examples demonstrating how to add artwork to the design. |
| `components/`      | Component data for electrical components, including circuits specific to a component. |
| `components/<manufacturer>`   | Components are organized into folders based on manufacturer |
| `components/manufacturer/<MPN>.stanza`   | There is one file per component family in the manufacturer folder (e.g. `analog-devices/ADM7150.stanza` models the ADM7150 LDOs). This file contains component data, and component-specific package models and modules.|
| `derating/`      | Contains collections of derating parameters for reliability testing. |
| `derating/space-derating.stanza`      | Derating parameters for spaceflight applications. |
| `designs/`      | Collection of example designs. [More documentation here.](designs/example-designs.md) |
| `doc/`      | Documentation. |
| `manufacturers/`      | Directory of PCB fabrication and manufacturing data like rules and stack-up definitions.|
| `modules/`      | Contains generators for subcircuits. (e.g. passive-circuits.stanza contains generators for circuits like passive filters and voltage dividers) |
| `modules/solvers`      | Contains JITX circuit solvers. (e.g. voltage-divider.stanza contains a solver for creating a resistive voltage divider taking into account component tolerance and availability) |
| `utils/`      | Utilities for modeling components and creating circuit generators|
| `utils/bundles.stanza`      | Definitions for commonly used bundles (e.g. `SPI`) |
| `utils/checks.stanza`      | Checks to run on designs (e.g. `check resistor()`|
| `utils/connects.stanza`      | Connection statements for creating io-translation/conditioning circuitry. (e.g. `isolate()`|
| `utils/generator-utils.stanza`      | General purpose utilities for modeling components and creating circuit generators. |
| `utils/generic-components.stanza`      | Collection of generic components (e.g. generic resistors, or banana-plugs)|
| `utils/landpatterns.stanza`      | Generators for land-pattern geometry (e.g. `make-qfn-landpattern()`)|
| `utils/property-structs.stanza`      | Pre-defined properties that can be applied to components, nets, modules in a design which are helpful to enable checks on the design. |
| `utils/symbols.stanza`      | Pre-defined schematic symbols (e.g. `power symbols, resistors, capacitors, diodes, etc`)|
| `utils/tolerance.stanza`      | Description of `Toleranced()` data-type and associated support functions. |
