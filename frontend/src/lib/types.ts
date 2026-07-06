const today = () => {
  const d = new Date();
  const day = String(d.getDate()).padStart(2, "0");
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const year = d.getFullYear();

  return `${day}-${month}-${year}`;
};
export interface Address {
  flat: string;
  road: string;
  post_office: string;
  area: string;
  district: string;
  state: string;
  country: string;
  pin: string;
}

export interface ContactDetails {
  country_code: string;
  mobile: string;
  email: string;
  std_code: string;
  landline: string;
}

export interface AOCode {
  area_code: string;
  ao_type: string;
  range_code: string;
  ao_number: string;
}

export interface Form93FormValues {
  first_name: string;
  middle_name: string;
  last_name: string;

  aadhaar_first_name: string;
  aadhaar_middle_name: string;
  aadhaar_last_name: string;

  gender: "male" | "female" | "transgender" | "";
  dob: string; // dd-mm-yyyy
  aadhaar_number: string;

  residence_address: Address;
  office_address: Address;

  residential_status: "resident" | "non_resident" | "rnor" | "";
  passport_number: string;
  tin: string;

  contact: ContactDetails;

  income_salary: boolean;
  income_business: boolean;
  income_house_property: boolean;
  income_capital_gains: boolean;
  income_other_sources: boolean;
  income_none: boolean;

  single_parent: "yes" | "no" | "";
  father_first_name: string;
  father_middle_name: string;
  father_last_name: string;
  mother_first_name: string;
  mother_middle_name: string;
  mother_last_name: string;
  parent_to_print: "father" | "mother" | "";

  ao_code: AOCode;

  ra_first_name: string;
  ra_middle_name: string;
  ra_last_name: string;
  ra_pan: string;
  ra_aadhaar: string;
  ra_address: Address;
  ra_contact: ContactDetails;

  communication_address: "residence" | "representative" | "office";

  proof_identity: boolean;
  proof_address: boolean;
  proof_dob: boolean;
  ra_proof_identity: boolean;
  ra_proof_address: boolean;

  declarant_name: string;
  declarant_capacity: "self" | "representative";
  place: string;
  decl_date: string;
  signatory_name: string;
  designation: string;
}

export const emptyAddress = (): Address => ({
  flat: "",
  road: "",
  post_office: "",
  area: "",
  district: "",
  state: "",
  country: "INDIA",
  pin: "",
});

export const emptyContact = (): ContactDetails => ({
  country_code: "91",
  mobile: "",
  email: "",
  std_code: "",
  landline: "",
});

export const defaultValues: Form93FormValues = {
  first_name: "",
  middle_name: "",
  last_name: "",
  aadhaar_first_name: "",
  aadhaar_middle_name: "",
  aadhaar_last_name: "",
  gender: "",
  dob: "",
  aadhaar_number: "",
  residence_address: emptyAddress(),
  office_address: emptyAddress(),
  residential_status: "",
  passport_number: "",
  tin: "",
  contact: emptyContact(),
  income_salary: false,
  income_business: false,
  income_house_property: false,
  income_capital_gains: false,
  income_other_sources: false,
  income_none: false,
  single_parent: "",
  father_first_name: "",
  father_middle_name: "",
  father_last_name: "",
  mother_first_name: "",
  mother_middle_name: "",
  mother_last_name: "",
  parent_to_print: "",
  ao_code: { area_code: "", ao_type: "", range_code: "", ao_number: "" },
  ra_first_name: "",
  ra_middle_name: "",
  ra_last_name: "",
  ra_pan: "",
  ra_aadhaar: "",
  ra_address: emptyAddress(),
  ra_contact: emptyContact(),
  communication_address: "residence",
  proof_identity: false,
  proof_address: false,
  proof_dob: false,
  ra_proof_identity: false,
  ra_proof_address: false,
  declarant_name: "",
  declarant_capacity: "self",
  place: "",
  decl_date: today(),
  signatory_name: "",
  designation: "",
};
