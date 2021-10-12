# Open Component Database
 
This is an open database of components and circuit generators for automated circuit board design. Think of it as a software library for electrical engineering. We welcome contributions of component models, as well as parametric circuit generators. If you contribute to this library your expert hardware engineering knowledge becomes reusable and sharable, having the same impact as open-source software.

Components are modeled with the standardized open-source Embedded Systems Intermediate Representation (ESIR) developed by JITX for the National Electronic Resurgence Initiative.

# Organization
| File/Folder   | Description |
| ------------- |-------------|
| `components/`      | Component data for electrical components, including circuits specific to a component. |
| `components/<manufacturer>`   | Components are organized into folders based on <manufacturer> |
| `components/<manufacturer>/<MPN>.stanza`   | There is one file per component family in the manufacturer folder (e.g. `analog-devices/ADM7150.stanza` models the ADM7150 LDOs). This file contains component data, and component-specific package models and modules.|
| `derating/`      | Contains collections of derating parameters for reliability testing. |
| `derating/space-derating.stanza`      | Derating parameters for spaceflight applications. |
| `designs/`      | Collection of example designs. |
| `doc/`      | Documentation. |
| `manufacturers/`    | Contains ? |
| `modules/`      | Contains generators for subcircuits. (e.g. passive-circuits.stanza contains generators for circuits like passive filters and voltage dividers) |
| `scripts/`    | Import/export scripts. |
| `style-guide/` | Style guide for entities in this library. |
| `tests/`      | Tests and test utilities. |
| `utils/`      | Utilities for modeling components and creating circuit generators|
| `utils/box-symbol.stanza`      | Generation for symbol outlines with pins |
| `utils/bundles.stanza`      | Definitions for commonly used bundles (e.g. `SPI`) |
| `utils/checks.stanza`      | Checks to run on designs (e.g. `check resistor()`|
| `utils/connects.stanza`      | Connection statements for creating io-translation/conditioning circuitry. (e.g. `isolate()`|
| `utils/db-parts.stanza`      | Definitions of RLC components |
| `utils/debug-utils.stanza`      | Definitions of test points, jumpers, industry standard debug ports |
| `utils/defaults.stanza`      | Generic setup of PCB characteristics |
| `utils/design-vars.stanza`      | Generic setup of project characteristics |
| `utils/generator-utils.stanza`      | General purpose utilities for modeling components and creating circuit generators. |
| `utils/generic-components.stanza`      | Collection of generic components (e.g. generic resistors, or banana-plugs)|
| `utils/interface.stanza`      | Empty file? |
| `utils/land-patterns.stanza`      | Generators for land-pattern geometry (e.g. `make-qfn-landpattern()`)|
| `utils/land-protrusions.stanza`      | Generator for land-pattern fillets  |
| `utils/micro-controllers.stanza`      | Generator for generic microcontroller  |
| `utils/module-utils.stanza`      | Generator for generic debug connector  |
| `utils/property-structs.stanza`      | Generic property definitions  |
| `utils/stm-to-jitx.stanza`      | Routine to import STM microcontroller to JITX  |
| `utils/stm.stanza`      | Routine to convert STM JSON to JITX project  |
| `utils/symbol-utils.stanza`      | Generator for schematic symbol utilities |
| `utils/symbols.stanza`      | Generator for common schematic symbols  |
| `utils/tolerance.stanza`      | Routines to assist with component tolerance management  |

