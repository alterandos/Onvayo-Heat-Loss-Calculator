b_2_1_table_b_1_additional_thermal_transmittance_for_thermal_bridges = {
    "New buildings with a high level of heat insulation and attested minimization of thermal bridges that exceeds generally recognized rules of practice": 0.02,
    "New buildings in compliance with generally recognized rules of practice regarding the minimization of thermal bridges": 0.05,
    "Buildings with mainly internal heat insulation broken by solid ceilings (e.g. reinforced concrete)": 0.15,
    "All other buildings": 0.10
}

b_2_4_table_b_2_temperature_adjustment_term = {
    "Room or group of adjoining rooms/spaces": {
        "1 external wall": 0.4,
        "2 external walls without external doors": 0.5,
        "2 external walls with external doors": 0.6,
        "3 or more external walls": 0.8,
    },
    "Basement": { # A room can be considered as a basement if more than 70 % of the external wall area is in contact with the ground
        "without external doors/windows": 0.5,
        "with external doors/windows": 0.8,
    },
    "Roof space": {
        "high ventilation rate of the roof space": 1.0,
        "other non-insulated roofs": 0.9,
        "insulated roofs": 0.7,
    },
    "Circulation area": {
        "internal space (no external walls) with low ventilation (<=0.5 h-1)": 0.0,
        "freely ventilated": 1.0
    },
    "Floor": {
        "suspended (floor above crawl space)": 0.8
    }
}

b_3_3_table_b_11_temperature_correction_factor = {
    "external air": 1,
    "unheated spaces or another building entity (u)": 0.5,
    "ground": 0.3,
    "heated space": 0.3
}

b_3_4_table_b_12_air_change_rate = {
    ">=1995": 0.25,
    "<1995": 0.5,
    "<1977": 1,
    "buildings with tight windows": 0.25,
    "buildings with obvious leakages": 1,
    "heat load of single rooms": 0.5
}

b_4_2_table_b_14_building_temperature = {
    "Single office": 20,
    "Landscaped office": 20,
    "Conference room": 20,
    "Auditorium": 20,
    "Cafeteria/Restaurant": 20,
    "Classroom": 20,
    "Nursery": 20,
    "Department store": 16,
    "Residential": 20,
    "Bathroom": 24,
    "Church": 15,
    "Museum/Gallery": 16
}

b_4_3_table_b_15_u_values = {
    "Windows, French doors": {
        "Wooden frame, single glazing": {
            "<=1918": 5.0, "1919-48": 5.0, "1949-57": 5.0, "1958-68": 5.0, "1969-78": 5.0, "1979-83": 5.0, "1984-94": None, ">=1995": None
        },
        "Wooden frame, double glazing": {
            "<=1918": 2.7, "1919-48": 2.7, "1949-57": 2.7, "1958-68": 2.7, "1969-78": 2.7, "1979-83": 2.7, "1984-94": 2.7, ">=1995": None
        },
        "Wooden frame, insulation glazing": {
            ">=1995": 1.8
        },
        "Plastic frame, insulating glazing": {
            "1958-68": 3.0, "1969-78": 3.0, "1979-83": 3.0, "1984-94": 3.0, ">=1995": 1.8
        },
        "Metal frame, insulating glazing": {
            "1958-68": 4.3, "1969-78": 4.3, "1979-83": 4.3, "1984-94": 4.3, ">=1995": 1.8
        }
    },
    "Roller shutters": {
        "old, non-insulated": {
            "<=1918": 3.0, "1919-48": 3.0, "1949-57": 3.0, "1958-68": 3.0, "1969-78": 3.0, "1979-83": 3.0, "1984-94": 3.0, ">=1995": 3.0
        },
        "new, insulated": {
            "<=1918": 1.8, "1919-48": 1.8, "1949-57": 1.8, "1958-68": 1.8, "1969-78": 1.8, "1979-83": 1.8, "1984-94": 1.8, ">=1995": 1.8
        }
    },
    "Doors": {
        "all": {
            "<=1918": 3.5, "1919-48": 3.5, "1949-57": 3.5, "1958-68": 3.5, "1969-78": 3.5, "1979-83": 3.5, "1984-94": 3.5, ">=1995": 3.5
        }
    },
    "External walls, walls against ground, internal walls against unheated cellars": {
        "Solid construction (masonry, concrete or similar)": {
            "<=1918": 1.7, "1919-48": 1.7, "1949-57": 1.4, "1958-68": 1.4, "1969-78": 1.0, "1979-83": 0.8, "1984-94": 0.6, ">=1995": 0.5
        },
        "Wooden construction (timber frame construction, prefabricated house or similar)": {
            "<=1918": 2.0, "1919-48": 2.0, "1949-57": 1.4, "1958-68": 1.4, "1969-78": 0.6, "1979-83": 0.5, "1984-94": 0.4, ">=1995": 0.4
        }
    },
    "Ceilings against ground or unheated cellars": {
        "Solid construction (masonry, concrete or similar)": {
            "<=1918": 1.2, "1919-48": 1.2, "1949-57": 1.5, "1958-68": 1.0, "1969-78": 1.0, "1979-83": 0.8, "1984-94": 0.6, ">=1995": 0.6
        },
        "Wooden beam ceiling": {
            "<=1918": 1.0, "1919-48": 0.8, "1949-57": 0.8, "1958-68": 0.8, "1969-78": 0.6, "1979-83": 0.6, "1984-94": 0.4, ">=1995": 0.4
        }
    },
    "Roofs and walls between heated and unheated attics": {
        "Solid construction": {
            "<=1918": 2.1, "1919-48": 2.1, "1949-57": 2.1, "1958-68": 2.1, "1969-78": 0.6, "1979-83": 0.5, "1984-94": 0.4, ">=1995": 0.3
        },
        "Wooden construction": {
            "<=1918": 2.6, "1919-48": 1.4, "1949-57": 1.4, "1958-68": 1.4, "1969-78": 0.8, "1979-83": 0.5, "1984-94": 0.4, ">=1995": 0.3
        }
    },
    "Top storey ceilings and ceilings above ambient (passageways, etc.)": {
        "Solid": {
            "<=1918": 2.1, "1919-48": 2.1, "1949-57": 2.1, "1958-68": 2.1, "1969-78": 0.6, "1979-83": 0.5, "1984-94": 0.4, ">=1995": 0.3
        },
        "Wooden beam ceiling": {
            "<=1918": 1.0, "1919-48": 0.8, "1949-57": 0.8, "1958-68": 0.8, "1969-78": 0.6, "1979-83": 0.4, "1984-94": 0.3, ">=1995": 0.3
        }
    }
}
