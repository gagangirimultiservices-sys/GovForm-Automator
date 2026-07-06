"""
schemas.py
Pydantic models describing every field of Government PAN Form No. 93.
These models are used to validate incoming JSON from the React frontend
before the PDF generation engine fills the original government PDF.
"""

from __future__ import annotations

import re
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator


AADHAAR_RE = re.compile(r"^\d{12}$")
PIN_RE = re.compile(r"^\d{6}$")
MOBILE_RE = re.compile(r"^\d{10}$")
DATE_RE = re.compile(r"^\d{2}-\d{2}-\d{4}$")  # dd-mm-yyyy


class Address(BaseModel):
    flat: Optional[str] = ""
    road: Optional[str] = ""
    post_office: Optional[str] = ""
    area: Optional[str] = ""
    district: Optional[str] = ""
    state: Optional[str] = ""
    country: Optional[str] = ""
    pin: Optional[str] = ""

    @field_validator("pin")
    @classmethod
    def validate_pin(cls, v):
        if v and not PIN_RE.match(v):
            raise ValueError("PIN / ZIP code must be exactly 6 digits")
        return v


class ContactDetails(BaseModel):
    country_code: Optional[str] = "91"
    mobile: Optional[str] = ""
    email: Optional[str] = ""
    std_code: Optional[str] = ""
    landline: Optional[str] = ""

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v):
        if v and not MOBILE_RE.match(v):
            raise ValueError("Mobile number must be exactly 10 digits")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v:
            if "@" not in v or "." not in v.split("@")[-1]:
                raise ValueError("Invalid email address")
        return v


class AOCode(BaseModel):
    area_code: Optional[str] = ""
    ao_type: Optional[str] = ""
    range_code: Optional[str] = ""
    ao_number: Optional[str] = ""


class Form93Data(BaseModel):
    # ---- Part A : Personal Information ----
    first_name: str
    middle_name: Optional[str] = ""
    last_name: Optional[str] = ""

    aadhaar_first_name: Optional[str] = ""
    aadhaar_middle_name: Optional[str] = ""
    aadhaar_last_name: Optional[str] = ""

    gender: str  # "male" | "female" | "transgender"
    dob: str  # dd-mm-yyyy
    aadhaar_number: Optional[str] = ""

    residence_address: Address
    office_address: Optional[Address] = Address()

    residential_status: str  # "resident" | "non_resident" | "rnor"

    passport_number: Optional[str] = ""
    tin: Optional[str] = ""

    contact: ContactDetails

    # ---- Part B : Source of Income ----
    income_salary: bool = False
    income_business: bool = False
    income_house_property: bool = False
    income_capital_gains: bool = False
    income_other_sources: bool = False
    income_none: bool = False

    # ---- Part C : Parents ----
    single_parent: Optional[str] = ""  # "yes" | "no"

    father_first_name: Optional[str] = ""
    father_middle_name: Optional[str] = ""
    father_last_name: Optional[str] = ""

    mother_first_name: Optional[str] = ""
    mother_middle_name: Optional[str] = ""
    mother_last_name: Optional[str] = ""

    parent_to_print: Optional[str] = ""  # "father" | "mother"

    # ---- Part D : AO Code ----
    ao_code: AOCode = AOCode()

    # ---- Part E : Representative Assessee ----
    ra_first_name: Optional[str] = ""
    ra_middle_name: Optional[str] = ""
    ra_last_name: Optional[str] = ""
    ra_pan: Optional[str] = ""
    ra_aadhaar: Optional[str] = ""
    ra_address: Optional[Address] = Address()
    ra_contact: Optional[ContactDetails] = ContactDetails()

    # ---- Part F : Communication Address ----
    communication_address: str = "residence"  # residence | representative | office

    # ---- Part G : Declarations ----
    proof_identity: bool = False
    proof_address: bool = False
    proof_dob: bool = False

    ra_proof_identity: bool = False
    ra_proof_address: bool = False

    # ---- Verification ----
    declarant_name: Optional[str] = ""
    declarant_capacity: str = "self"  # "self" | "representative"
    place: Optional[str] = ""
    decl_date: Optional[str] = ""  # dd-mm-yyyy
    signatory_name: Optional[str] = ""
    designation: Optional[str] = ""

    @field_validator("dob", "decl_date")
    @classmethod
    def validate_dates(cls, v):
        if v and not DATE_RE.match(v):
            raise ValueError("Date must be in dd-mm-yyyy format")
        return v

    @field_validator("aadhaar_number", "ra_aadhaar")
    @classmethod
    def validate_aadhaar(cls, v):
        if v and not AADHAAR_RE.match(v):
            raise ValueError("Aadhaar number must be exactly 12 digits")
        return v

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v):
        if v not in ("male", "female", "transgender"):
            raise ValueError("gender must be one of male, female, transgender")
        return v

    @field_validator("residential_status")
    @classmethod
    def validate_residential_status(cls, v):
        if v not in ("resident", "non_resident", "rnor"):
            raise ValueError(
                "residential_status must be one of resident, non_resident, rnor"
            )
        return v

    @model_validator(mode="after")
    def validate_passport_for_non_resident(self):
        if self.residential_status in ("non_resident", "rnor") and not self.passport_number:
            raise ValueError(
                "Passport Number is mandatory for Non Resident / "
                "Resident but Not Ordinarily Resident applicants"
            )
        return self


class GenerateResponse(BaseModel):
    success: bool
    filename: Optional[str] = None
    download_url: Optional[str] = None
    message: str


class FormDescriptor(BaseModel):
    id: str
    name: str
    description: str
    pages: int
