#!/usr/bin/python
import sys, re, urllib2
from bs4 import BeautifulSoup

units = [
    ('G', 9),
    ('M', 6),
    ('k', 3),
    ('',  0),
    ('m', -3),
    ('u', -6),
    ('n', -9),
    ('p', -12)
]

def formatToUnit(val, toUnit=None):
    toUnitValue = 0

    if toUnit != None:
        if toUnit == '0':
            toUnit = '' #We don't want to display '0' as the prefix
        else:
            toUnitValue = dict(units)[toUnit]
    else: #Find best suited unit
        for p, u in units:
            if val >= (10 ** u):
                toUnit = p
                toUnitValue = u
                break

    return "%s %s" % (str(float(val) / (10 ** toUnitValue)), toUnit)

def usage(args):
    print "==================="
    print "Parts.py Usage Help"
    print "==================="
    print "Format: ./parts.py Type Values"
    print "\nArgs:"
    print "  Type :"
    print "\thelp : Displays this information"
    print "\tres : Color bands resistor"
    print "\trsmd : SMD resistor"
    print "\tcap : Capacitor"
    print "\tconv : Unit Conversion"
    print "\nColor bands resistors"
    print "  Example: ./parts.py res bk bn bk bn"
    print "  Gives ohm value of 3 to 5 bands resistors"
    print "  Color Codes:"
    print "\tBlack=bk,k ; Brown=bn,n ; Red=r ; Orange=o ; Yellow=y ; Green=gn,n ; Blue=bu,u ;"
    print "\tViolet/Purple=v ; Grey/Slay=s,sl,gy ; White=w ; Silver=si ; Gold=gd ;"
    print "\nSMD Resistors"
    print "  Example: ./parts.py rsmd 102 ; ./parts.py rsmd 22R2"
    print "  Gives ohm value of 3 and 4 digits SMD resistors"
    print "\nCapacitors"
    print "  Example: ./parts.py cap 104 ; ./parts.py cap 104 1H B"
    print "  Gives capacitance value of ceramic caps with support of voltage and tolerance"
    print "\nConversion"
    print "  Example: ./parts.py conv 2000 k ; ./parts.py conv 222p n"
    print "  Format: value[suffix] [toSuffix]"
    print "  Converts a value from one unit prefix to an other one"
    print "\nScript by Anthony Teisseire"

def smd_resistor(args):
    code = args[0].upper()
    val = 0

    if len(code) < 3 or len(code) > 4:
        print "Bad SMD resistor code"
        return

    dec = code.find('R')
    if dec > -1:
        val = float(code.replace('R', '.'))
    else:
        val = int(code[:-1]) * (10 ** int(code[-1]))

    print "============"
    print "SMD Resistor"
    print "============"
    print "Value: %sOhms" % formatToUnit(val) + ('' if val > 1 else (" (%s)" % val))


def resistor(bands):
    band_val = {
        'k': 0, 'bk': 0,
        'n': 1, 'bn': 1,
        'r': 2,
        'o': 3,
        'y': 4,
        'g': 5, 'gn': 5,
        'u': 6, 'bu': 6,
        'v': 7,
        's': 8, 'sl': 8, 'gy': 8, #gy is here for convienence
        'w': 9,

        #multipliers
        'gd': -1,
        'si': -2
    }

    tol_val = {
        'n': 1, 'bn': 1,
        'r': 2,
        'g': 0.5, 'gn': 0.5,
        'u': 0.25, 'bu': 0.25,
        'v': 0.1,
        's': 0.05, 'sl': 0.05, 'gy': 0.05, #gy is still here for convienence

        'gd': 5,
        'si': 10
    }

    valBands = 2 if len(bands) < 5 else 3

    val = 0
    tol = 20
    for b in bands[:valBands]:
        val = val * 10 + band_val[b.lower()]

    val = val * (10 ** band_val[bands[valBands].lower()])

    if len(bands) > 3:
        tol = tol_val[bands[-1].lower()]
    
    print "========"
    print "Resistor"
    print "========"
    print "Value: %sOhms %i%%" % (formatToUnit(val), tol)


def capacitor(args):
    voltage = {
        '1h': 50,
        '2a': 100,
        '2t': 150,
        '2d': 200,
        '2e': 250,
        '2g': 400,
        '2j': 630
    }

    tol = {
        'b': '0.1 pF',
        'c': '0.25 pF',
        'd': '0.5 pF',
        'f': '1%',
        'g': '2%',
        'h': '3%',
        'j': '5%',
        'k': '10%',
        'm': '20%',
        'z': '+80%, -20%'
    }

    argc = len(args)
    code = args[0]

    val = int(code[:-1]) * (10 ** (-12 + int(code[-1]))) #values expressed in pF (-12)
    
    print "========="
    print "Capacitor"
    print "========="
    print "Value: %sF" % (formatToUnit(val))
    
    if argc == 3:
        print "Voltage: %iV" % voltage[args[1].lower()]
        print "Tolerance: %s" % tol[args[2].lower()]

def part_search(args):
    name = args[0]
    endpoint = 'http://www.alldatasheet.com/view.jsp?Searchword=%s'
    html = urllib2.urlopen(endpoint % name).read()

    parsed = BeautifulSoup(html, "html.parser")
    
    tags = parsed.find_all('tr', limit=4, id=re.compile("cell[0-9]{1,2}"))
    tds = tags[0].find_all('td')

    print "==========="
    print "Part Search"
    print "==========="
    print "Main Result:"
    print "  Part: %s" % tds[1].a.get_text().strip()
    print "  Description: %s" % tds[3].string
    print "  Manufactuer: %s " %  tds[0].br.next_sibling
    print "  Datasheet: %s" % tds[1].a['href']

    for tag in tags[1:]:
        tds = tag.find_all('td')
       
        #print tds
        if len(tds) > 3:
            tds = tds[1:] #chomp manufacturer if it's there 

        print "Result :"
        print "  Part: %s" % tds[0].a.get_text().strip()
        print "  Description: %s" % tds[2].string
        print "  Datasheet: %s" % tds[0].a['href']

    print "Search results from: www.alldatasheet.com"


def unit_convert(args):
    fromVal = args[0]
    fromUnit = fromVal[-1]
    toUnit = args[1]

    if not fromUnit.isdigit():
        fromUnitValue = dict(units)[fromUnit]
        fromVal = fromVal[:-1]
    else:
        fromUnitValue = 0

    print "Result : %s" % formatToUnit(float(fromVal) * (10 ** fromUnitValue), toUnit)


parts_sw = {
    'rsmd': smd_resistor,
    'res': resistor,
    'cap': capacitor,
    'part': part_search,
    'conv': unit_convert,
    'help': usage
}

def main():
    if len(sys.argv) < 2:
        print "Not enough arguments"
        usage()
        sys.exit(2)

    parts_sw.get(sys.argv[1], usage)(sys.argv[2:])

if __name__ == "__main__":
    main()
