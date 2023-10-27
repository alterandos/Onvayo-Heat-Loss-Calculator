sample_json_data = {
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

from src import simplified_calculators as scalc

data = scalc.Building(
    sample_json_data
)

print ('build year  || ', data.build_year)
print ('delta__utb  || ', data.delta__utb)
print ('n__build    || ', data.n__build)
print ('theta__int  || ', data.theta__int_build)
x=0
for element in data.building_elements:
    x+=1
    print(f' ~b{x}~')
    print(f'  u__k      || ', element.u__k)
    print(f'  f__x      || ', element.f__x)
    print(f'  f__x      || ', element.design_transmission_loss)
print('--ventilation heat loss  || ', data.ventilation_heat_loss)
print('--transmission heat loss || ', data.building_design_transmission_heat_loss)
print('  ~--~ total heat load   || ', data.building_design_heat_load)
