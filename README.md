# Open Component Database

This is an open database of components and circuit generators for automated circuit board design. Think of it as a software library for electrical engineering. We welcome contributions of component models, as well as parametric circuit generators. If you contricute to this library your expert hardware engineering knowledge becomes reusable and sharable, having the same impact as open-source software.

Components are modeled with the standardized open-source Embedded Systems Intermediate Representation (ESIR) developed by JITX for the national Electronic Resurgence Initiative.

# Organization
| File/Folder   | Description |
| ------------- |-------------|
| `components/`      | Component data for electrical components, including circuits specific to a component. |
| `components/manufaturer`   | Components are organized into folders based on manufacturer |
| `components/manufaturer/MPN.stanza`   | There is one file per component family in the manufacturer folder (e.g. `analog-devices/ADM7150.stanza` models the ADM7150 LDOs). This file contains component data, and component-specific package models and modules.|
| `derating/`      | Contains collections of derating parameters for reliability testing. |
| `derating/space-derating.stanza`      | Derating parameters for spaceflight applications. |
| `designs/`      | Collection of example designs. |
| `doc/`      | Documentation. |
| `modules/`      | Contains generators for subcircuits. (e.g. passive-circuits.stanza contains genreators for circuits like passive filters and voltage dividers) |
| `tests/`      | Tests and test utilities. |
| `utils/`      | Utilities for modeling components and creating circuit generators|
| `utils/bundles`      | Definitions for commonly used bundles (e.g. `SPI`) |
| `utils/checks`      | Checks to run on designs (e.g. `check resistor()`|
| `utils/connections`      | Connection statements for creating io-translation/conditioning circuitry. (e.g. `isolate()`|
| `utils/generator-utils`      | General purpose utilities for modeling components and creating circuit generators. |
| `utils/generic-components`      | Collection of generic components (e.g. generic resistors, or banana-plugs)|
| `utils/land-patterns`      | Generators for land-pattern geometry (e.g. `make-qfn-landpattern()`)|
| `utils/pin-spec`      | Convenience function for creating pins/package mappings from datasheet information.|
