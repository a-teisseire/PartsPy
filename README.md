# PartsPy
## What is PartsPy?
PartsPy is a helpful tool written in Python for electronics hobbyist, DIYers, hackers, tinkerers, [insert your favorite term here].  
It can accomplish various tasks:
- Determine the value of color-bands resistors
- Determine the value of SMD resistors
- Determine the value of ceramic capacitors
- Search for a part online with its description and datasheet *(Thanks to alldatasheets.com!)*
- Allows simple conversion between different metric prefixes


## How do I use it?
**Syntax:** `$ ./parts.py command args...`

PartsPy supports the following commands:
- help : Displays the manual
- res : Resistors
- rsmd : SMD Resistors
- cap : Capacitors
- conv : Conversion
- part : Part Search

### Color bands resistors
**Syntax:** `./parts.py res col1 col2 col3 [col4 [col5]]`  
Gives ohm value of 3 to 5 bands resistors.

**Example:** `./parts.py res bk bn bk bn"`  
**Output:**

    ========
    Resistor
    ========
    Value: 1.0 Ohms 1%

#### Color Codes
| Color         | X  | XX    |
|---------------|----|-------|
| Black         | k  | bk    |
| Brown         | n  | bn    |
| Red           | r  | r     |
| Orange        | o  | o     |
| Yellow        | y  | y     |
| Green         | n  | gn    |
| Blue          | u  | bu    |
| Violet/Purple | v  | v     |
| Grey/Slay     | s  | sl,gy |
| White         | w  | w     |
| Silver        | si | si    |
| Gold          | gd | gd    |

### SMD Resistors
**Syntax:** `./parts.py rsmd Code`  
Gives ohm value of 3 and 4 digits SMD resistors (Yes it supports decimals).

**Example:** `./parts.py rsmd 472`  
**Output:**

    ============
    SMD Resistor
    ============
    Value: 4.7 kOhms

### Capacitors
**Syntax:** `./parts.py cap Code [VoltageCode ToleranceCode]`  
Gives capacitance value of ceramic caps with support of voltage and tolerance.

**Example:** `./parts.py cap 104`  
**Output:**

    =========
    Capacitor
    =========
    Value: 100.0 nF

**Example:** `./parts.py cap 104 1H B`  
**Output:**

    =========
    Capacitor
    =========
    Value: 100.0 nF
    Voltage: 50V
    Tolerance: 0.1 pF
    
### Part Search
**Syntax:** `./parts.py part PartName`  
Searches online for descriptions and datasheets of a component. PartsPy lists 4 matching or closely matching components.  
The results are parsed from alldatasheets.com. This website exists thanks to advertising and donations, please consider the latter.

**Example:** `./parts.py part ATMEGA328P-pu`  
**Output:**  

    ===========
    Part Search
    ===========
    Main Result:
      Part: ATMEGA328P-PU
      Description: 8-bit Microcontroller with 4/8/16/32K Bytes In-System Programmable Flash
      Manufactuer: ATMEL Corporation 
      Datasheet: http://www.alldatasheet.com/datasheet-pdf/pdf/392289/ATMEL/ATMEGA328P-PU.html
    Result :
      Part: ATmega328P-15AZ
      Description: 8-bit Microcontroller with 32K Bytes In-System Programmable Flash
      Datasheet: http://www.alldatasheet.com/datasheet-pdf/pdf/313558/ATMEL/ATmega328P-15AZ.html
    Result :
      Part: ATmega328P-15MZ
      Description: 8-bit Microcontroller with 32K Bytes In-System Programmable Flash
      Datasheet: http://www.alldatasheet.com/datasheet-pdf/pdf/313559/ATMEL/ATmega328P-15MZ.html
    Result :
      Part: ATMEGA328P-20AU
      Description: 8-bit Atmel Microcontroller with 4/8/16K Bytes In-System Programmable Flash
      Datasheet: http://www.alldatasheet.com/datasheet-pdf/pdf/520568/ATMEL/ATMEGA328P-20AU.html
    Search results from: www.alldatasheet.com


### Conversion
**Syntax:** `./parts.py conv value[prefix] [toPrefix]  `  
Converts a value from one unit prefix to an other one. Indicate 0 if you want to convert to the base unit.  

**Example:** `./parts.py conv 2k 0`  
**Output:**

    Result : 2000.0

**Example:** `./parts.py conv 222u n`  
**Output:**

    Result : 22000.0 n

## License
PartsPy is released under the MIT licensing terms. Check the LICENSE file in this repository for more information.

Copyright (c) 2016 Anthony Teisseire
