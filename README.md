# Onvayo Heat Loss Calculator

## Description
The Onvayo Heat Loss Calculator is designed to automatically calculate the heat loss of a heated space, a group of heated spaces, or an entire building. Inputs are sourced from German regulatory bodies or measurements from the buildings/rooms themselves, which are provided by customers. All calculations comply with German regulations.

The primary goal is to enable the advisory on heat pump installations for customers' homes or other buildings. It's important to note that this project will be integrated with a separate customer-facing frontend code.


## Usage
You can refer to the excel file located in the `/docs` folder for detailed information on the required inputs for the calculator. Particularly look at sheet "8" in column "Input Notes".

You can use _sample_usage.py_ to run the calculator and see how to access it.

Sample data is in the following structure:

```python
data = {
    'build_year': 2000,  # Year building was constructed, should result in n_build=0.25, build_year_range = '>=1995'
    'theta__e': -5,  # External design temperature in °C
    'v__build': 500,  # Internal volume of the considered heated building in m^3
    'theta__int_build': None,  # Internal design temperature of the considered heated building in °C. Must be included if there is no value for building_type
    'building_type': 'Residential', # should result in theta__int_build=20
    'delta__utb': None,  # Blanket additional thermal transmittance for thermal bridges in W/(m^2∙K)
    'delta__utb_selection_criteria': 'Buildings with mainly internal heat insulation broken by solid ceilings (e.g. reinforced concrete)',  # Used to determine delta__utb if no value supplied
    'n__build': None,  # Air change rate of the building in h^-1
    'air_tightness_level': None,  # Used to determine n__build if no value supplied. If not supplied, uses build_year instead
    'building_elements': [
        {
            'a__k': 100,
            'u__k': 1.5,
            'f__x': 0.5,
            'be_adjacent_to': None,
            'be_type': 'Doors',
            'be_sub_type': None
        },{
            'a__k': 130, 
            'u__k': None,
            'f__x': None,
            'be_adjacent_to': 'ground', # f__x=0.3
            'be_type': 'Doors',
            'be_sub_type': 'all', # u__k=3.5
        }
        # ... More building elements ...
    ]
}
```