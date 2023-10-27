from dataclasses import dataclass
from data import din_12831_data


class BuildingElement:
    def __init__(self, data: dict):
        self.a__k = data.get('a__k')
        self.u__k = data.get('u__k')
        self.f__x = data.get('f__x')
        self.be_adjacent_to = data.get('be_adjacent_to')
        self.be_type = data.get('be_type')
        self.be_sub_type = data.get('be_sub_type')
        # building measurements
        self.build_year = data.get('build_year')
        self.delta__utb = data.get('delta__utb')
        self.theta__int_build = data.get('theta__int_build')
        self.theta__e = data.get('theta__e')

        # value checks
        if not isinstance(self.build_year, int):
            raise TypeError("build_year should be of type int")

        if self.a__k is None or self.a__k <= 0:
            raise ValueError('Area of building element, a__k, cannot be zero or negative.')
        
        if self.u__k is None and (self.be_sub_type is None or self.be_type is None):
            raise ValueError('No value provided for u__k or building element type/sub-type. If no value is provided for u__k, values must be provided for building element type and sub-type.')

        if self.f__x is None and self.be_adjacent_to is None:
            raise ValueError('No value provided for f__x or be_adjacent_to. If no value is provided for f__x, value must be provided for be_adjacent_to.')
        
        self.u__k = self.u__k if self.u__k is not None else self.get_simplified_thermal_transmittance_u() # Thermal transmittance of the building element (k) in W/(m^2∙K)
        self.f__x = self.f__x if self.f__x is not None else self.get_simplified_temperature_adjustment_term() # Temperature correction factor

        self.design_transmission_loss = self.calculate_simplified_be_design_transmission_loss()


    def calculate_simplified_be_design_transmission_loss(self) -> float:
        return BuildingElement.calculate_simplified_be_design_transmission_loss_static(
            self.a__k, self.u__k, self.delta__utb, self.f__x, self.theta__int_build, self.theta__e)


    @staticmethod
    def calculate_simplified_be_design_transmission_loss_static(
        a__k, u__k, delta__utb, f__x, theta__int_build, theta__e) -> float:
        return a__k * (u__k + delta__utb) * f__x * (theta__int_build - theta__e)
    

    # In accordance with Annex A.4.3 and B.4.3 of DIN 12831
    def get_simplified_thermal_transmittance_u(self):
        return BuildingElement.get_simplified_thermal_transmittance_u_static(self.be_type, self.be_sub_type, self.build_year)


    @staticmethod
    def get_simplified_thermal_transmittance_u_static(be_type:str, be_sub_type:str, build_year:int):
        u = din_12831_data.a_4_3_simplified_u_value()
        if u is None:
            u = din_12831_data.b_4_3_simplified_u_value(be_type, be_sub_type, build_year)
        return u
    
    
    # In accordance with annex A.4.2 and B.4.2 of DIN 12831; requires be_adjacent_to
    def get_simplified_temperature_adjustment_term(self):
        return BuildingElement.get_simplified_temperature_adjustment_term_static(self.be_adjacent_to)


    @staticmethod
    def get_simplified_temperature_adjustment_term_static(be_adjacent_to:str):
        f__x = din_12831_data.a_3_3_temperature_correction_factor()
        return f__x if f__x is not None else din_12831_data.b_3_3_temperature_correction_factor(be_adjacent_to)


class Building:
    def __init__(self,
                #  build_year: int, # Year building was constructed
                #  v__build: float, # Internal volume of the considered heated building in m^3
                #  theta__e: float, # External design temperature in °C
                #  theta__int_build: float = None, # Internal design temperature of the considered heated building in °C
                #  building_type: str = None, # Must be included if there is no value for theta__int_build
                #  delta__utb: float = None, # Blanket additional thermal transmittance for thermal bridges in W/(m^2∙K)
                #  delta__utb_selection_criteria: str = None, # used to determine delta__utb if no value supplied
                #  n__build: float = None, # air change rate of the building in h^-1
                #  air_tightness_level: str = None, # used to determine n__build if no value supplied. If not supplied, uses build_year instead
                #  building_elements: list[dict] = None, # Building elements that make up the building facing either external air, unheated spaces, or ground
                 data: dict):
        
        self.build_year = data['build_year']
        self.v__build = data['v__build']
        self.theta__e = data['theta__e']
        self.theta__int_build = data.get('theta__int_build')
        self.building_type = data.get('building_type')
        self.delta__utb = data.get('delta__utb')
        self.delta__utb_selection_criteria = data.get('delta__utb_selection_criteria')
        self.n__build = data.get('n__build')
        self.air_tightness_level = data.get('air_tightness_level')
        self.building_elements = data.get('building_elements', [])

        if self.v__build is None or self.v__build <= 0:
            raise ValueError('Volume of building element, v__build, cannot be zero or negative.')
        
        if self.theta__e is None:
            raise ValueError('No value provided for theta__e, the external mean design temperature.')
        
        if self.theta__int_build is None and self.building_type is None:
            raise ValueError('No value provided for theta__int_build or building type. If no value is provided for theta__int_build, a value must be provided for building type.')
        
        if self.building_elements is None or len(self.building_elements) < 1:
            raise ValueError('No building elements provided.')
        
        if 'theta__int_build' not in data and 'building_type' not in data:
            raise ValueError("If theta__int_build is not provided in the data, building_type must be included.")

        if 'delta__utb' not in data and 'delta__utb_selection_criteria' not in data:
            raise ValueError("If delta__utb is not provided in the data, delta__utb_selection_criteria must be included.")

        if 'n__build' not in data and ('air_tightness_level' not in data and 'build_year' not in data):
            raise ValueError("If n__build is not provided, either air_tightness_level or build_year must be included.")
        
        # Blanket additional thermal transmittance for thermal bridges in W/(m^2∙K)
        self.get_simplified_additional_thermal_transmittance_for_thermal_bridges()
        # Air change rate in h-1, n__build
        self.get_simplified_air_change_rate()
        # Internal design temperature of the considered heated building in °C, theta__int_build
        self.get_simplified_internal_design_temperature()
        # External design temperature in °C
        # self.theta__e = self.theta__e

        self.building_elements = [BuildingElement({
                **element_data, 
                'build_year': self.build_year, 
                'delta__utb': self.delta__utb, 
                'theta__int_build': self.theta__int_build, 
                'theta__e': self.theta__e
            }) for element_data in data.get('building_elements', [])]

        return


    def get_simplified_additional_thermal_transmittance_for_thermal_bridges(self):
        self.delta__utb = self.delta__utb if self.delta__utb is not None else \
            Building.get_simplified_additional_thermal_transmittance_for_thermal_bridges_static(self.delta__utb_selection_criteria)


    # In accordance with Annex A.3.2, alternatively A.2.1, and B.3.2, alternatively B.2.1, of DIN 12831, requires selection criteria
    @staticmethod
    def get_simplified_additional_thermal_transmittance_for_thermal_bridges_static(selection_criteria:str=None):
        delta__utb = din_12831_data.a_3_2_simplified_thermal_bridges()
        if delta__utb is None:
            delta__utb = din_12831_data.b_3_2_simplified_thermal_bridges() if selection_criteria is None else din_12831_data.b_2_1_simplified_thermal_bridges(selection_criteria)
        return delta__utb


    def get_simplified_air_change_rate(self):
        self.n__build = self.n__build if self.n__build is not None \
            else Building.get_simplified_air_change_rate_static(self.build_year, self.air_tightness_level)


    # In accordance with annex A.3.4 and B.3.4 of DIN 12831; requires air tightness level or build year
    @staticmethod
    def get_simplified_air_change_rate_static(build_year:int, air_tightness_level:str = None):
        n__build = din_12831_data.a_3_4_simplified_air_change_rate()
        return n__build if n__build is not None else din_12831_data.b_3_4_simplified_air_change_rate(build_year, air_tightness_level)


    def get_simplified_internal_design_temperature(self):
        self.theta__int_build = self.theta__int_build if self.theta__int_build is not None \
            else Building.get_simplified_internal_design_temperature_static(self.building_type)
    

    # In accordance with annex A.4.2 and B.4.2 of DIN 12831;
    @staticmethod
    def get_simplified_internal_design_temperature_static(building_type:str):
        theta__int_build = din_12831_data.a_4_2_internal_design_temperature()
        return theta__int_build if theta__int_build is not None else din_12831_data.b_4_2_internal_design_temperature(building_type)


    def calculate_simplified_building_ventilation_loss(self):
        return Building.calculate_simplified_building_ventilation_loss_static(self)


    @staticmethod
    def calculate_simplified_building_ventilation_loss_static(b: 'Building') -> float:
        """
        Calculate the building design ventilation heat loss.
        
        Args:
        - b (Building): Input data for the building element.
        
        Returns:
        - Building design ventilation heat loss in Watts.
        """
        rho_cp = 0.34  # Fixed matter constant of air in Wh/(m^3∙K)
        return b.v__build * b.n__build * rho_cp * (data.theta__int_build - data.theta__e)






data = Building(
        data = {
        'build_year': 2000, # n_build=0.25, build_year_range = '>=1995'
        'theta__e': -5,
        'v__build': 500,
        'theta__int_build': None,
        'building_type': 'Residential', # theta__int_build=20
        'delta__utb': None,
        'delta__utb_selection_criteria': 'Buildings with mainly internal heat insulation broken by solid ceilings (e.g. reinforced concrete)', # delta_utb=0.15
        'n__build': None,
        'air_tightness_level': None,
        'building_elements': [
            {
                'a__k': 100,
                'u__k': 1.5,
                'f__x': 0.5,
                'be_adjacent_to': None,
                'be_type': 'Doors',
                'be_sub_type': None
            },
            {
                'a__k': 130, 
                'u__k': None,
                'f__x': None,
                'be_adjacent_to': 'ground', # f__x=0.3
                'be_type': 'Doors',
                'be_sub_type': 'all', # u__k=3.5
            }
        ]
    }
)

print ('build year  || ', data.build_year)
print ('delta__utb  || ', data.delta__utb)
print ('n__build    || ', data.n__build)
print ('theta__int  || ', data.theta__int_build)
for element in data.building_elements:
    print('u__k        || ', element.u__k)
    print('f__x        || ', element.f__x)
    print('f__x        || ', element.design_transmission_loss)



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
