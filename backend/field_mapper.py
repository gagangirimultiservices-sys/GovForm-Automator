"""
field_mapper.py  — CALIBRATED v2
==================================
"""
 
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
 
 
@dataclass
class CombField:
    x_start: float
    y_top: float
    y_bot: float
    cell_w: float
    count: int
    page: int
    uppercase: bool = True
 
    @property
    def baseline(self) -> float:
        return round(self.y_bot - 2.5, 2)
 
 
@dataclass
class TickField:
    x0: float
    y0: float
    x1: float
    y1: float
    page: int
 
 
@dataclass
class LineField:
    x: float
    y: float
    max_w: float
    page: int
    font_size: float = 8.0
    uppercase: bool = False
 
 
COMB: Dict[str, CombField] = {
    "first_name":          CombField(x_start=180.36, y_top=195.01, y_bot=206.50, cell_w=15.35, count=25, page=0),
    "middle_name":         CombField(x_start=180.48, y_top=208.42, y_bot=219.92, cell_w=15.35, count=25, page=0),
    "last_name":           CombField(x_start=180.48, y_top=221.83, y_bot=233.86, cell_w=15.35, count=25, page=0),
    "aadhaar_name_r1":     CombField(x_start=180.48, y_top=252.87, y_bot=264.37, cell_w=15.35, count=25, page=0),
    "aadhaar_name_r2":     CombField(x_start=180.31, y_top=266.28, y_bot=277.78, cell_w=15.35, count=25, page=0),
    "aadhaar_name_r3":     CombField(x_start=180.59, y_top=279.69, y_bot=291.19, cell_w=15.35, count=25, page=0),
    "aadhaar_name_r4":     CombField(x_start=180.36, y_top=293.10, y_bot=304.60, cell_w=15.35, count=25, page=0),
    "dob_d1":  CombField(x_start=180.53, y_top=306.52, y_bot=318.01, cell_w=15.16, count=1, page=0),
    "dob_d2":  CombField(x_start=195.69, y_top=306.52, y_bot=318.01, cell_w=16.53, count=1, page=0),
    "dob_m1":  CombField(x_start=226.38, y_top=306.52, y_bot=318.01, cell_w=16.52, count=1, page=0),
    "dob_m2":  CombField(x_start=242.90, y_top=306.52, y_bot=318.01, cell_w=15.16, count=1, page=0),
    "dob_y1":  CombField(x_start=272.47, y_top=306.52, y_bot=318.01, cell_w=15.16, count=1, page=0),
    "dob_y2":  CombField(x_start=287.63, y_top=306.52, y_bot=318.01, cell_w=14.91, count=1, page=0),
    "dob_y3":  CombField(x_start=302.53, y_top=306.52, y_bot=318.01, cell_w=14.91, count=1, page=0),
    "dob_y4":  CombField(x_start=317.44, y_top=306.52, y_bot=318.01, cell_w=15.16, count=1, page=0),
    "aadhaar_number":      CombField(x_start=180.34, y_top=319.93, y_bot=331.43, cell_w=15.17, count=12, page=0),
    "res_flat":            CombField(x_start=180.34, y_top=350.44, y_bot=361.93, cell_w=15.35, count=25, page=0),
    "res_road":            CombField(x_start=180.49, y_top=363.85, y_bot=375.35, cell_w=15.35, count=25, page=0),
    "res_post_office":     CombField(x_start=180.56, y_top=377.26, y_bot=388.76, cell_w=15.35, count=25, page=0),
    "res_area":            CombField(x_start=180.70, y_top=390.67, y_bot=402.17, cell_w=15.35, count=25, page=0),
    "res_district":        CombField(x_start=180.77, y_top=404.09, y_bot=415.58, cell_w=15.35, count=25, page=0),
    "res_pin":             CombField(x_start=457.07, y_top=417.50, y_bot=428.99, cell_w=15.43, count=7, page=0),
    #OFFICE ADRESS
    "off_flat":            CombField(x_start=180.77, y_top=448.01, y_bot=459.50, cell_w=15.35, count=25, page=0),
    "off_road":            CombField(x_start=180.65, y_top=461.42, y_bot=472.91, cell_w=15.35, count=25, page=0),
    "off_post_office":     CombField(x_start=180.65, y_top=474.83, y_bot=486.32, cell_w=15.35, count=25, page=0),
    "off_area":            CombField(x_start=180.48, y_top=488.24, y_bot=499.74, cell_w=15.35, count=25, page=0),
    "off_district":        CombField(x_start=180.36, y_top=501.65, y_bot=513.15, cell_w=15.35, count=25, page=0),

    "off_pin":             CombField(x_start=457.07, y_top=515.07, y_bot=526.56, cell_w=15.43, count=7, page=0),
    "passport_number":     CombField(x_start=328.57, y_top=551.77, y_bot=563.27, cell_w=15.00, count=12, page=0),
    "tin":                 CombField(x_start=269.77, y_top=571.84, y_bot=583.33, cell_w=15.18, count=20, page=0),
    "mobile_country_code": CombField(x_start=240.06, y_top=602.34, y_bot=613.84, cell_w=14.99, count=3, page=0),
    "mobile_number":       CombField(x_start=376.92, y_top=602.34, y_bot=613.84, cell_w=14.74, count=10, page=0),
    "std_code":            CombField(x_start=240.11, y_top=629.17, y_bot=640.66, cell_w=14.99, count=4, page=0),
    "landline_number":     CombField(x_start=377.49, y_top=629.17, y_bot=640.66, cell_w=15.05, count=8, page=0),
    "father_first_name":   CombField(x_start=179.42, y_top=739.00, y_bot=750.49, cell_w=15.35, count=25, page=0),
    "father_middle_name":  CombField(x_start=179.56, y_top=752.41, y_bot=763.90, cell_w=15.35, count=25, page=0),
    "father_last_name":    CombField(x_start=179.42, y_top=765.82, y_bot=777.32, cell_w=15.35, count=25, page=0),
    "mother_first_name":   CombField(x_start=179.42, y_top=21.85,  y_bot=33.34,  cell_w=15.34, count=25, page=1),
    "mother_middle_name":  CombField(x_start=179.70, y_top=35.26,  y_bot=46.76,  cell_w=15.34, count=25, page=1),
    "mother_last_name":    CombField(x_start=179.28, y_top=48.67,  y_bot=60.17,  cell_w=15.34, count=25, page=1),
    "ao_area_code":        CombField(x_start=237.33, y_top=106.24, y_bot=117.73, cell_w=15.53, count=3, page=1),
    "ao_type":             CombField(x_start=397.20, y_top=106.24, y_bot=117.73, cell_w=15.59, count=2, page=1),
    "ao_range_code":       CombField(x_start=237.75, y_top=119.65, y_bot=131.15, cell_w=15.53, count=3, page=1),
    "ao_number":           CombField(x_start=397.17, y_top=119.65, y_bot=131.15, cell_w=15.59, count=2, page=1),
    "ra_first_name":       CombField(x_start=177.38, y_top=163.62, y_bot=175.12, cell_w=15.34, count=25, page=1),
    "ra_middle_name":      CombField(x_start=177.38, y_top=177.03, y_bot=188.53, cell_w=15.34, count=25, page=1),
    "ra_last_name":        CombField(x_start=177.38, y_top=190.44, y_bot=201.94, cell_w=15.34, count=25, page=1),
    "ra_pan":              CombField(x_start=178.14, y_top=205.75, y_bot=217.24, cell_w=15.39, count=10, page=1),
    "ra_aadhaar":          CombField(x_start=281.09, y_top=222.12, y_bot=233.62, cell_w=15.39, count=12, page=1),
    "ra_flat":             CombField(x_start=177.76, y_top=253.70, y_bot=265.20, cell_w=15.34, count=25, page=1),
    "ra_road":             CombField(x_start=177.91, y_top=267.12, y_bot=278.61, cell_w=15.34, count=25, page=1),
    "ra_post_office":      CombField(x_start=178.13, y_top=280.53, y_bot=292.02, cell_w=15.34, count=25, page=1),
    "ra_area":             CombField(x_start=177.91, y_top=293.94, y_bot=305.43, cell_w=15.34, count=25, page=1),
    "ra_district":         CombField(x_start=178.23, y_top=307.35, y_bot=318.85, cell_w=15.34, count=25, page=1),
    "ra_pin":              CombField(x_start=454.14, y_top=320.76, y_bot=332.26, cell_w=15.43, count=7, page=1),
    "ra_mobile_country_code": CombField(x_start=236.96, y_top=351.84, y_bot=363.33, cell_w=15.53, count=3, page=1),
    "ra_mobile_number":       CombField(x_start=357.38, y_top=351.84, y_bot=363.33, cell_w=15.34, count=10, page=1),
    "ra_std_code":            CombField(x_start=237.62, y_top=379.80, y_bot=391.29, cell_w=15.46, count=4, page=1),
    "ra_landline_number":     CombField(x_start=358.83, y_top=379.80, y_bot=391.29, cell_w=15.00, count=8, page=1),
}
 
 
TICK: Dict[str, TickField] = {
    "gender_male":           TickField(x0=180.36, y0=293.11, x1=196.64, y1=304.60, page=0),
    "gender_female":         TickField(x0=226.52, y0=293.11, x1=242.80, y1=304.60, page=0),
    "gender_transgender":    TickField(x0=287.61, y0=293.11, x1=303.88, y1=304.60, page=0),
    "status_resident":       TickField(x0=210.65, y0=531.91, x1=225.97, y1=543.40, page=0),
    "status_non_resident":   TickField(x0=272.73, y0=531.91, x1=288.05, y1=543.40, page=0),
    "status_rnor":           TickField(x0=349.97, y0=531.91, x1=365.30, y1=543.40, page=0),
    "income_salary":         TickField(x0=179.15, y0=668.95, x1=194.47, y1=680.44, page=0),
    "income_business":       TickField(x0=256.00, y0=668.95, x1=271.33, y1=680.44, page=0),
    "income_house_property": TickField(x0=394.47, y0=668.95, x1=409.80, y1=680.44, page=0),
    "income_capital_gains":  TickField(x0=179.15, y0=685.19, x1=194.47, y1=696.69, page=0),
    "income_other_sources":  TickField(x0=255.86, y0=685.19, x1=271.70, y1=696.69, page=0),
    "income_none":           TickField(x0=394.62, y0=685.19, x1=410.71, y1=696.69, page=0),
    "single_parent_yes":     TickField(x0=240.41, y0=724.15, x1=255.78, y1=735.64, page=0),
    "single_parent_no":      TickField(x0=301.92, y0=724.15, x1=317.29, y1=735.64, page=0),
    "parent_print_father":   TickField(x0=332.82, y0=64.67, x1=349.19, y1=77.77, page=1),
    "parent_print_mother":   TickField(x0=394.33, y0=64.67, x1=410.42, y1=77.77, page=1),
    "comm_residence":        TickField(x0=213.56, y0=415.53, x1=228.92, y1=427.03, page=1),
    "comm_representative":   TickField(x0=299.55, y0=415.53, x1=315.08, y1=427.03, page=1),
    "comm_office":           TickField(x0=445.55, y0=415.53, x1=460.91, y1=427.03, page=1),
    "proof_identity":        TickField(x0=68.20, y0=472.64, x1=83.57, y1=484.13, page=1),
    "proof_address":         TickField(x0=166.83, y0=472.64, x1=182.19, y1=484.13, page=1),
    "proof_dob":             TickField(x0=267.74, y0=472.64, x1=283.11, y1=484.13, page=1),
    "ra_proof_identity":     TickField(x0=68.20, y0=509.73, x1=83.57, y1=521.22, page=1),
    "ra_proof_address":      TickField(x0=166.83, y0=509.73, x1=182.19, y1=521.22, page=1),
}
 
 
LINE: Dict[str, LineField] = {
    "res_state":          LineField(x=134.0,  y=426.5,  max_w=79.0,  page=0, uppercase=True, font_size=7.5),
    "res_country":        LineField(x=291.0,  y=426.5,  max_w=94.0,  page=0, uppercase=True, font_size=7.5),
    "off_state":          LineField(x=134.0,  y=524.1,  max_w=79.0,  page=0, uppercase=True, font_size=7.5),
    "off_country":        LineField(x=291.0,  y=524.1,  max_w=94.0,  page=0, uppercase=True, font_size=7.5),

    "email":              LineField(x=253.47,  y=623.50,  max_w=340.0, page=0, font_size=8.0),

    "ra_state":           LineField(x=129.5,  y=329.8,  max_w=79.0,  page=1, uppercase=True, font_size=7.5),
    "ra_country":         LineField(x=286.5,  y=329.8,  max_w=91.0,  page=1, uppercase=True, font_size=7.5),

    "ra_email":           LineField(x=250.0,  y=374.3,  max_w=340.0, page=1, font_size=8.0),

    "declarant_name":     LineField(x=75.0,   y=569.0,  max_w=145.0, page=1, font_size=8.5),
    "declarant_capacity": LineField(x=282.0,  y=569.0,  max_w=85.0,  page=1, font_size=8.5),
    "place":              LineField(x=95.0,   y=629.7,  max_w=150.0, page=1, font_size=8.5),
    "decl_date":          LineField(x=95.0,   y=645.0,  max_w=150.0, page=1, font_size=8.5),
    "signatory_name":     LineField(x=395.0,  y=774.5,  max_w=105.0, page=1, font_size=8.5),
    "designation":        LineField(x=412.0,  y=801.5,  max_w=95.0,  page=1, font_size=8.5),
}
 
 
def get_comb(name: str) -> CombField:
    if name not in COMB:
        raise KeyError(f"Unknown comb field: {name!r}")
    return COMB[name]
 
 
def get_tick(name: str) -> TickField:
    if name not in TICK:
        raise KeyError(f"Unknown tick field: {name!r}")
    return TICK[name]
 
 
def get_line(name: str) -> LineField:
    if name not in LINE:
        raise KeyError(f"Unknown line field: {name!r}")
    return LINE[name]