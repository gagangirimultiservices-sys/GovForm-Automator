"""
pdf_generator.py  — v2 (precise coordinates)
==============================================
Uses field_mapper v2 calibrated coordinates.
Text is placed using:
    baseline_y = field.y_bot - 2.5
    center_x   = field.x_start + i * field.cell_w
                 + (field.cell_w - char_advance_width) / 2
"""
import io
import os
# import uuid
from typing import Optional

import fitz  # PyMuPDF

from field_mapper import COMB, TICK, LINE, CombField, TickField, LineField
from schemas import Form93Data

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
TEMPLATE   = os.path.join(BASE_DIR, "..", "templates", "Form93.pdf")
# OUTPUT_DIR = os.path.join(BASE_DIR, "..", "generated")

TEXT_COLOR  = (0.0, 0.0, 0.0)   # dark navy
TICK_COLOR  = (0.0,  0.0,  0.0)
FONT        = "helv"
FONT_SIZE   = 8.5   # default for comb boxes


class PDFGenerationError(Exception):
    pass

'''
def _ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
'''

# ---------------------------------------------------------------------------
# Core rendering helpers
# ---------------------------------------------------------------------------

def _write_comb(page: fitz.Page, field: CombField, value: str):
    """Write value into a comb (per-character box) field using precise centering."""
    if not value:
        return
    text = value.upper() if field.uppercase else value
    text = text[:field.count]

    # Font size: fit inside the box height leaving 1pt top+bottom margin
    box_h = field.y_bot - field.y_top
    fs = min(FONT_SIZE, box_h - 2.5, field.cell_w * 0.58)
    fs = max(fs, 5.0)

    baseline = field.baseline  # y_bot - 2.5

    for i, ch in enumerate(text):
        box_x0 = field.x_start + i * field.cell_w
        ch_w = fitz.get_text_length(ch, fontname=FONT, fontsize=fs)
        # center horizontally inside the cell
        cx = box_x0 + (field.cell_w - ch_w) / 2.0
        page.insert_text(
            fitz.Point(cx, baseline),
            ch,
            fontname=FONT,
            fontsize=fs,
            color=TEXT_COLOR,
        )


def _write_line(page: fitz.Page, field: LineField, value: str):
    """Write a plain line of text inside a non-comb line field."""
    if not value:
        return
    text = value.upper() if field.uppercase else value

    fs = field.font_size
    tw = fitz.get_text_length(text, fontname=FONT, fontsize=fs)
    while tw > field.max_w and fs > 5.0:
        fs -= 0.3
        tw = fitz.get_text_length(text, fontname=FONT, fontsize=fs)
    # Last-resort truncation
    while tw > field.max_w and len(text) > 1:
        text = text[:-1]
        tw = fitz.get_text_length(text, fontname=FONT, fontsize=fs)

    page.insert_text(
        fitz.Point(field.x, field.y),
        text,
        fontname=FONT,
        fontsize=fs,
        color=TEXT_COLOR,
    )


def _draw_tick(page: fitz.Page, field: TickField):
    """Draw a ✓ mark inside a printed tick-box placeholder."""
    x0, y0, x1, y1 = field.x0, field.y0, field.x1, field.y1
    w = x1 - x0
    h = y1 - y0
    # Two-stroke checkmark: bottom-left going to lower-center, then upper-right
    p1 = fitz.Point(x0 + w * 0.12, y0 + h * 0.55)
    p2 = fitz.Point(x0 + w * 0.42, y0 + h * 0.88)
    p3 = fitz.Point(x0 + w * 0.92, y0 + h * 0.15)
    page.draw_line(p1, p2, color=TICK_COLOR, width=1.2)
    page.draw_line(p2, p3, color=TICK_COLOR, width=1.2)


# ---------------------------------------------------------------------------
# Date helper
# ---------------------------------------------------------------------------

def _split_dob(dob: str):
    """dd-mm-yyyy -> (dd, mm, yyyy) or None."""
    parts = dob.split("-")
    if len(parts) != 3 or len(parts[0]) != 2 or len(parts[1]) != 2 or len(parts[2]) != 4:
        return None
    return parts[0], parts[1], parts[2]


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

def generate_pdf(data: Form93Data) -> io.BytesIO: #str:
    if not os.path.exists(TEMPLATE):
        raise PDFGenerationError(
            "templates/Form93.pdf not found. Place the original government PDF there."
        )

    try:
        doc = fitz.open(TEMPLATE)
    except Exception as e:
        raise PDFGenerationError(f"Cannot open template: {e}") from e

    try:
        p0 = doc[0]
        p1 = doc[1] if doc.page_count > 1 else None

        def pg(field_page: int) -> fitz.Page:
            return p0 if field_page == 0 else p1

        def comb(name: str, value: str):
            if not value:
                return
            f = COMB[name]
            _write_comb(pg(f.page), f, value)

        def tick(name: str, condition: bool = True):
            if condition:
                f = TICK[name]
                _draw_tick(pg(f.page), f)

        def line(name: str, value: str):
            if not value:
                return
            f = LINE[name]
            _write_line(pg(f.page), f, value)

        # ----------------------------------------------------------------
        # PART A — Personal Information
        # ----------------------------------------------------------------
        comb("first_name",   data.first_name)
        comb("middle_name",  data.middle_name or "")
        comb("last_name",    data.last_name or "")

        # Name as per Aadhaar — write full name across row 1 only (25 chars),
        # spill to row 2 if name is longer, etc.
        aadhaar_full = " ".join(filter(None, [
            data.aadhaar_first_name or data.first_name,
            data.aadhaar_middle_name or data.middle_name or "",
            data.aadhaar_last_name or data.last_name or "",
        ])).upper().replace(" ", "")  # treat as continuous char stream in boxes
        # Actually the form splits it into rows; write each section separately
        # Row 1: first name chars
        fn = (data.aadhaar_first_name or data.first_name).upper()
        mn = (data.aadhaar_middle_name or data.middle_name or "").upper()
        ln = (data.aadhaar_last_name or data.last_name or "").upper()
        comb("aadhaar_name_r1", fn[:25])
        comb("aadhaar_name_r2", mn[:25])
        comb("aadhaar_name_r3", ln[:25])
        # row 4 left blank

        # ----------------------------------------------------------------
        # 2. Gender
        # ----------------------------------------------------------------
        tick("gender_male",        data.gender == "male")
        tick("gender_female",      data.gender == "female")
        tick("gender_transgender", data.gender == "transgender")

        # ----------------------------------------------------------------
        # 3. Date of Birth
        # ----------------------------------------------------------------
        dob = _split_dob(data.dob)
        if dob:
            dd, mm, yyyy = dob
            comb("dob_d1", dd[0])
            comb("dob_d2", dd[1])
            comb("dob_m1", mm[0])
            comb("dob_m2", mm[1])
            comb("dob_y1", yyyy[0])
            comb("dob_y2", yyyy[1])
            comb("dob_y3", yyyy[2])
            comb("dob_y4", yyyy[3])

        # ----------------------------------------------------------------
        # 4. Aadhaar Number
        # ----------------------------------------------------------------
        comb("aadhaar_number", data.aadhaar_number or "")

        # ----------------------------------------------------------------
        # 5. Residence Address
        # ----------------------------------------------------------------
        ra = data.residence_address
        comb("res_flat",         ra.flat or "")
        comb("res_road",         ra.road or "")
        comb("res_post_office",  ra.post_office or "")
        comb("res_area",         ra.area or "")
        comb("res_district",     ra.district or "")
        line("res_state",        ra.state or "")
        line("res_country",      ra.country or "")
        comb("res_pin",          (ra.pin or "")[:7])

        # ----------------------------------------------------------------
        # 6. Office Address
        # ----------------------------------------------------------------
        if data.office_address:
            oa = data.office_address
            comb("off_flat",        oa.flat or "")
            comb("off_road",        oa.road or "")
            comb("off_post_office", oa.post_office or "")
            comb("off_area",        oa.area or "")
            comb("off_district",    oa.district or "")
            line("off_state",       oa.state or "")
            line("off_country",     oa.country or "")
            comb("off_pin",         (oa.pin or "")[:7])

        # ----------------------------------------------------------------
        # 7. Residential Status
        # ----------------------------------------------------------------
        tick("status_resident",     data.residential_status == "resident")
        tick("status_non_resident", data.residential_status == "non_resident")
        tick("status_rnor",         data.residential_status == "rnor")

        # ----------------------------------------------------------------
        # 8. Passport Number
        # ----------------------------------------------------------------
        comb("passport_number", data.passport_number or "")

        # ----------------------------------------------------------------
        # 9. TIN
        # ----------------------------------------------------------------
        comb("tin", data.tin or "")

        # ----------------------------------------------------------------
        # 10. Contact Details
        # ----------------------------------------------------------------
        c = data.contact
        comb("mobile_country_code", c.country_code or "91")
        comb("mobile_number",       c.mobile or "")
        if c.email:
            line("email", c.email)
        comb("std_code",        c.std_code or "")
        comb("landline_number", c.landline or "")

        # ----------------------------------------------------------------
        # 11. Source of Income
        # ----------------------------------------------------------------
        tick("income_salary",         data.income_salary)
        tick("income_business",       data.income_business)
        tick("income_house_property", data.income_house_property)
        tick("income_capital_gains",  data.income_capital_gains)
        tick("income_other_sources",  data.income_other_sources)
        tick("income_none",           data.income_none)

        # ----------------------------------------------------------------
        # 12. Single Parent
        # ----------------------------------------------------------------
        tick("single_parent_yes", data.single_parent == "yes")
        tick("single_parent_no",  data.single_parent == "no")

        # ----------------------------------------------------------------
        # 13. Father's Name
        # ----------------------------------------------------------------
        comb("father_first_name",  data.father_first_name or "")
        comb("father_middle_name", data.father_middle_name or "")
        comb("father_last_name",   data.father_last_name or "")

        # ================================================================
        # PAGE 1
        # ================================================================
        if p1 is not None:

            # 14. Mother's Name
            comb("mother_first_name",  data.mother_first_name or "")
            comb("mother_middle_name", data.mother_middle_name or "")
            comb("mother_last_name",   data.mother_last_name or "")

            # 15. Parent to print
            tick("parent_print_father", data.parent_to_print == "father")
            tick("parent_print_mother", data.parent_to_print == "mother")

            # 16. AO Code
            ao = data.ao_code
            comb("ao_area_code",  ao.area_code or "")
            comb("ao_type",       ao.ao_type or "")
            comb("ao_range_code", ao.range_code or "")
            comb("ao_number",     ao.ao_number or "")

            # 17-21. Representative Assessee
            comb("ra_first_name",  data.ra_first_name or "")
            comb("ra_middle_name", data.ra_middle_name or "")
            comb("ra_last_name",   data.ra_last_name or "")
            comb("ra_pan",         data.ra_pan or "")
            comb("ra_aadhaar",     data.ra_aadhaar or "")

            if data.ra_address:
                raa = data.ra_address
                comb("ra_flat",        raa.flat or "")
                comb("ra_road",        raa.road or "")
                comb("ra_post_office", raa.post_office or "")
                comb("ra_area",        raa.area or "")
                comb("ra_district",    raa.district or "")
                line("ra_state",       raa.state or "")
                line("ra_country",     raa.country or "")
                comb("ra_pin",         (raa.pin or "")[:7])

            if data.ra_contact:
                rc = data.ra_contact
                comb("ra_mobile_country_code", rc.country_code or "")
                comb("ra_mobile_number",       rc.mobile or "")
                if rc.email:
                    line("ra_email", rc.email)
                comb("ra_std_code",       rc.std_code or "")
                comb("ra_landline_number", rc.landline or "")

            # 22. Communication Address
            tick("comm_residence",      data.communication_address == "residence")
            tick("comm_representative", data.communication_address == "representative")
            tick("comm_office",         data.communication_address == "office")

            # 23. Applicant Proofs
            tick("proof_identity", data.proof_identity)
            tick("proof_address",  data.proof_address)
            tick("proof_dob",      data.proof_dob)

            # 24. RA Proofs
            tick("ra_proof_identity", data.ra_proof_identity)
            tick("ra_proof_address",  data.ra_proof_address)

            # Verification
            declarant = (data.declarant_name or
                         " ".join(filter(None, [data.first_name, data.middle_name, data.last_name])))
            capacity = "Self" if data.declarant_capacity == "self" else "Representative Assessee"

            line("declarant_name",     declarant)
            line("declarant_capacity", capacity)
            line("place",              data.place or "")

            if data.decl_date:
                d_parts = data.decl_date.split("-")
                date_str = "/".join(d_parts) if len(d_parts) == 3 else data.decl_date
                line("decl_date", date_str)

            line("signatory_name", data.signatory_name or declarant)
            line("designation",    data.designation or capacity)

        # ----------------------------------------------------------------
        
        buffer = io.BytesIO()
        doc.save(buffer, deflate=True, garbage=3)
        buffer.seek(0)
        return buffer
        
    except PDFGenerationError:
        raise
    except Exception as e:
        raise PDFGenerationError(f"PDF generation failed: {e}") from e
    finally:
        doc.close()