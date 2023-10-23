from dataclasses import dataclass
from res import din_12831_data


class Building:
    def __init__(self,
                 build_year: int,
                 v__build: float,
                 theta__e: float, 
                 theta__int_build: float = None, 
                 delta__utb: float = None, # used for building design transmission loss, but is constant through all BE's
                 n__build: float = None, # used for building ventilation loss
                 ):
        
        if v__build <= 0:
            raise ValueError('Volume of building element, a__k, cannot be zero or negative.')
        
        # Internal volume of the considered heated building in m^3
        self.v__build = v__build
        
        # Blanket additional thermal transmittance for thermal bridges in W/(m^2∙K)
        self.delta__utb = delta__utb if delta__utb is not None else get_simplified_additional_thermal_transmittance_for_thermal_bridges(delta__utb_selection_criteria)
        # Air change rate of the considered heated building in h^-1
        self.n__build = n__build if n__build is not None else get_simplified_air_change_rate(build_year, air_tightness_level)

        return


class BuildingElement:
    def __init__(self,
                 build_year: int,
                 a__k: float,
                #  v__build: float,
                 theta__e: float,
                 u__k: float = None,
                 delta__utb: float = None,
                 n__build: float = None,
                 theta__int_build: float = None,
                 f__x: float = None,
                 # must be included if there is no value for f__x
                #  space_type: str = None,
                #  space_sub_type: str = None,
                #  is_ceiling_less_than_4m: bool = True,
                 be_adjacent_to: str = None,
                 # must be included if there is no value for u__k
                 be_type: str = None,
                 be_sub_type: str = None,
                 # must be included if there is no value for theta__int_build
                 building_type: str = None,
                 # optional
                 delta__utb_selection_criteria: str = None, # used to determine delta__utb if no value supplied
                 air_tightness_level: str = None # used to determine n__build if no value supplied. If not supplied, uses build_year instead
                 ):
        
        # value checks
        if a__k <= 0:
            raise ValueError('Area of building element, a__k, cannot be zero or negative.')
        
        if u__k is None and (be_sub_type is None or be_type is None):
            raise ValueError('No value provided for u__k or building element type/sub-type. If no value is provided for u__k, values must be provided for building element type and sub-type.')
        
        if theta__int_build is None and building_type is None:
            raise ValueError('No value provided for theta__int_build or building type. If no value is provided for theta__int_build, value must be provided for building type.')
        
        if theta__e is None:
            raise ValueError('No value provided for theta__e, the external mean design temperature.')
        
        # if f__x is None and (space_type is None or space_sub_type is None):
            # raise ValueError('No value provided for f__x or space type. If no value is provided for f__x, values must be provided for space type and sub-type.')
        if f__x is None and be_adjacent_to is None:
            raise ValueError('No value provided for f__x or be_adjacent_to. If no value is provided for f__x, value must be provided for be_adjacent_to.')

        self.build_year = build_year
        self.be_adjacent_to = be_adjacent_to

        # Area of the building element (k) in m^2
        self.a__k = a__k


        # Thermal transmittance of the building element (k) in W/(m^2∙K)
        self.u__k = u__k if u__k is not None else get_simplified_thermal_transmittance_u(be_type, be_sub_type, build_year)
        # Blanket additional thermal transmittance for thermal bridges in W/(m^2∙K)
        self.delta__utb = delta__utb if delta__utb is not None else get_simplified_additional_thermal_transmittance_for_thermal_bridges(delta__utb_selection_criteria)
        # Air change rate of the considered heated building in h^-1
        self.n__build = n__build if n__build is not None else get_simplified_air_change_rate(build_year, air_tightness_level)
        # Internal design temperature of the considered heated building in °C
        self.theta__int_build = theta__int_build if theta__int_build is not None else get_simplified_internal_design_temperature(building_type)
        self.theta__e = theta__e  # External design temperature in °C
        self.f__x = f__x if f__x is not None else get_simplified_temperature_adjustment_term(be_adjacent_to) # Temperature correction factor

        self.design_transmission_loss = calculate_simplified_be_transmission_loss(self)


# In accordance with Annex A.4.3 and B.4.3 of DIN 12831
def get_simplified_thermal_transmittance_u(be_type:str, be_sub_type:str, build_year:int):
    u = a_4_3_simplified_u_value()
    if u is None:
        u = b_4_3_simplified_u_value(be_type, be_sub_type, build_year)
    return u


# In accordance with Annex A.3.2, alternatively A.2.1, and B.3.2, alternatively B.2.1, of DIN 12831, requires selection criteria
def get_simplified_additional_thermal_transmittance_for_thermal_bridges(delta__utb_selection_criteria:str=None):
    delta__utb = a_3_2_simplified_thermal_bridges()
    if delta__utb is None:
        delta__utb = b_3_2_simplified_thermal_bridges() if delta__utb_selection_criteria is None else b_2_1_simplified_thermal_bridges(delta__utb_selection_criteria)
    return delta__utb


# In accordance with annex A.3.4 and B.3.4 of DIN 12831; requires air tightness level or build year
def get_simplified_air_change_rate(build_year:int, air_tightness_level:str = None):
    n__build = a_3_4_simplified_air_change_rate()
    return n__build if n__build is not None else b_3_4_simplified_air_change_rate(build_year, air_tightness_level)


# In accordance with annex A.4.2 and B.4.2 of DIN 12831;
def get_simplified_internal_design_temperature(building_type:str):
    theta__int_build = a_4_2_internal_design_temperature()
    return theta__int_build if theta__int_build is not None else b_4_2_internal_design_temperature(building_type)


# In accordance with annex A.4.2 and B.4.2 of DIN 12831; requires be_adjacent_to
def get_simplified_temperature_adjustment_term(be_adjacent_to:str):
    f__x = a_3_3_temperature_correction_factor()
    return f__x if f__x is not None else b_3_3_temperature_correction_factor(be_adjacent_to)


def calculate_simplified_be_transmission_loss(be: BuildingElement) -> float:
    """
    Calculate the design transmission heat loss of a building element.
    
    Args:
    - be (BuildingElement): Input data for the building element.
    
    Returns:
    - Building element design transmission heat loss in Watts.
    """
    return be.a__k * (be.u__k + be.delta__utb) * be.f__x * (be.theta__int_build - be.theta__e)


def calculate_simplified_building_ventilation_loss(b: Building) -> float:
    """
    Calculate the building design ventilation heat loss.
    
    Args:
    - b (Building): Input data for the building element.
    
    Returns:
    - Building design ventilation heat loss in Watts.
    """
    rho_cp = 0.34  # Fixed matter constant of air in Wh/(m^3∙K)
    return b.v__build * b.n__build * rho_cp * (data.theta__int_build - data.theta__e)


def get_build_year_range_for_air_change_rate(year):
    if year <= 1977:
        return "<1977"
    elif year < 1995:
        return "<1995"
    else:
        return ">=1995"

def get_build_year_range_for_u_values(year):
    if year <= 1918:
        return "<=1918"
    elif 1919 <= year <= 1948:
        return "1919-1948"
    elif 1949 <= year <= 1957:
        return "1949-1957"
    elif 1958 <= year <= 1968:
        return "1958-1968"
    elif 1969 <= year <= 1978:
        return "1969-1978"
    elif 1979 <= year <= 1983:
        return "1979-1983"
    elif 1984 <= year <= 1994:
        return "1984-1994"
    else:
        return ">=1995"
    

# Annex definitions
def a_3_2_simplified_thermal_bridges():
    # Placeholder in case we get national values for ΔUTB values
    return None


def a_3_3_temperature_correction_factor():
    # Placeholder in case we get national values for f__x values
    return None


def a_3_4_simplified_air_change_rate():
    # Placeholder in case we get national values for n values
    return None


def a_4_2_internal_design_temperature():
    # Placeholder in case we get national values for θint,build values
    return None

def a_4_3_simplified_u_value():
    # Placeholder in case we get national values for U values
    return None


def b_2_1_simplified_thermal_bridges(delta__utb_selection_criteria: str):
    # ΔUTB value  in accordance with Annex B.2.1 W/m2KW/(m2∙K)
    return din_12831_data.b_2_1_table_b_1_additional_thermal_transmittance_for_thermal_bridges[delta__utb_selection_criteria]


def b_3_2_simplified_thermal_bridges():
    # ΔUTB value in accordance with Annex B.3.2 W/m2KW/(m2∙K)
    return 0.1


def b_3_3_temperature_correction_factor(be_adjacent_to):
    # f__x value in accordance with Annex B.3.3
    return din_12831_data.b_3_3_table_b_11_temperature_correction_factor[be_adjacent_to]

def b_3_4_simplified_air_change_rate(build_year:int, air_tightness_level:str = None):
    build_year_range = get_build_year_range_for_air_change_rate(build_year)
    # Air change rate in accordance with Annex B.3.4 [h−1]
    return din_12831_data.b_3_4_table_b_12_air_change_rate[air_tightness_level] if air_tightness_level is not None else din_12831_data.b_3_4_table_b_12_air_change_rate[build_year_range]


def b_4_2_internal_design_temperature(building_type):
    # Internal design temperature in accordance with Annex B.4.2 [°C]
    return din_12831_data.b_4_2_table_b_14_building_temperature[building_type]


def b_4_3_simplified_u_value(be_type: str, be_sub_type: str, build_year: str):
    build_year_range = get_build_year_range_for_u_values(build_year)
    print('build_year_range', build_year_range)
    # U values in accordance with Annex B.4.3 [W/(m2∙K)]
    return din_12831_data.b_4_3_table_b_15_u_values[be_type][be_sub_type][build_year_range]


data = BuildingElement(
    build_year=2000, # n_build=0.25
    a__k=100,
    # v__build=500,
    # u__k=0.5,
    # delta__utb=0.1,
    # n__build=0.8,
    # theta__int_build=20,
    theta__e=-5,
    # f__x=1,
    be_type='Doors',
    be_sub_type='all', # u__k=3.5
    building_type='Residential', # theta__int_build=20,
    delta__utb_selection_criteria = 'Buildings with mainly internal heat insulation broken by solid ceilings (e.g. reinforced concrete)', # delta_utb=0.15
    # space_type='Room or group of adjoining rooms/spaces',
    # space_sub_type='2 external walls with external doors' # f__x=0.6
    be_adjacent_to = 'ground' # f__x=0.3
    )

print ('build year  || ', data.build_year)
print ('delta__utb  || ', data.delta__utb)
print ('u__k        || ', data.u__k)
print ('n__build    || ', data.n__build)
print ('theta__int  || ', data.theta__int_build)
print ('f__x        || ', data.f__x)



def calculate_design_heat_loss(transmission_loss: float, ventilation_loss: float) -> float:
    """
    Calculate the building design heat load.
    
    Args:
    - transmission_loss (W): Building design transmission heat loss.
    - ventilation_loss (W): Building design ventilation heat loss.
    
    Returns:
    - Building design heat load in Watts.
    """
    return transmission_loss + ventilation_loss
