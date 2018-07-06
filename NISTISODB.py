#!/usr/bin/env python 2

import json
import requests

#Defines an isotherm object class
#NOTE: This class definition must be rewritten after the 2017 isotherm standard (multicomponent-capable)
# has been implemented in the NIST ISODB API
class NIST_ISODB_isotherm:
    def __init__(self,filename):
        host='adsorption.nist.gov'
        URL = 'https://'+host+'/isodb/api/isotherm/'+filename
        isotherm_JSON = json.loads(requests.get(URL).content)
        #----------------------------------------------------------------
        #Essential Check: Confirm that input isotherm is single component
        n_adsorbates = len(isotherm_JSON["adsorbates"])
        if n_adsorbates > 1:
            raise Exception("ERROR: Filename "+filename+" has multiple adsorbates.\n Input isotherm must be single component.")
        #----------------------------------------------------------------
        self.filename = filename
        self.pressureUnits = isotherm_JSON["pressureUnits"]
        self.adsorptionUnits = isotherm_JSON["adsorptionUnits"]
        self.p_label = "Pressure ("+self.pressureUnits+")"
        self.ads_label = "Loading ("+self.adsorptionUnits+")"
        self.p_list = [ point["pressure"] for point in isotherm_JSON["isotherm_data"] ]
        # Uses the first entry (index 0) as the isotherm is single component, or would have failed earlier test
        self.ads_list = [ point["species_data"][0]["adsorption"] for point in isotherm_JSON["isotherm_data"] ]
        self.adsorbate = isotherm_JSON["adsorbates"][0]
        self.adsorbent = isotherm_JSON["adsorbent"]
        self.temperature = float(isotherm_JSON["temperature"])

def error_check_isotherms(isotherms):
    #Basic System Checks:
    print( 'ESSENTIAL SYSTEM CHECKS: ')
    # Confirm that pressure units are consistent
    pressure_units = [ isotherm.pressureUnits for isotherm in isotherms ]
    if len(set(pressure_units)) > 1:
        print('ERROR: Incompatible pressure units in isotherms')
        for (i,isotherm) in enumerate(isotherms):
            print( '  Isotherm '+str(i+1)+": "+isotherm.pressureUnits )
        raise ValueError("Incompatible pressure units in isotherms")
    else:
        print('Pressure units are compatible: '+list(set(pressure_units))[0] )
    # Confirm that adsorption units are consistent
    adsorption_units = [ isotherm.adsorptionUnits for isotherm in isotherms ]
    if len(set(adsorption_units)) > 1:
        print('ERROR: Incompatible adsorption units in isotherms')
        for (i,isotherm) in enumerate(isotherms):
            print( '  Isotherm '+str(i+1)+": "+isotherm.adsorptionUnits )
        raise ValueError("Incompatible adsorption units in isotherms")
    else:
        print('Adsorption units are compatible: '+list(set(adsorption_units))[0] )
    # Confirm that the material is the same across the isotherms
    material_hashes = [ isotherm.adsorbent["hashkey"] for isotherm in isotherms ]
    material_names = [ isotherm.adsorbent["name"] for isotherm in isotherms ]
    if len(set(material_hashes)) > 1:
        print( 'WARNING: Different Materials Specified' )
        for (i,isotherm) in enumerate(isotherms):
            print( '  Isotherm '+str(i+1)+": "+isotherm.adsorbent["name"] )
    else:
        print( 'Same material is specified: '+list(set(material_names))[0] )
    # Confirm that the temperature is consistent
    temperatures = [ isotherm.temperature for isotherm in isotherms ]
    if len(set(temperatures)) > 1:
        print('ERROR: Different temperatures in isotherms')
        for (i,isotherm) in enumerate(isotherms):
            print( '  Isotherm '+str(i+1)+": "+isotherm.temperatures )
        raise ValueError("Different temperatures in isotherms")
    else:
        print('Temperature is consistent: '+str(list(set(temperatures))[0]) )
    return None
