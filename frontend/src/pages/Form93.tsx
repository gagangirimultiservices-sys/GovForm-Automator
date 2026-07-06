import { useState } from "react";
import { useForm } from "react-hook-form";
import AddressFields from "../components/AddressFields";
import Loader from "../components/Loader";
import Dialog from "../components/Dialog";
import { defaultValues, Form93FormValues } from "../lib/types";
import { generateForm93 } from "../lib/api";
//import { generateForm93, downloadUrlFor } from "../lib/api";

const AADHAAR_RE = /^\d{12}$/;
const PIN_RE = /^\d{6}$/;
const MOBILE_RE = /^\d{10}$/;
const DATE_RE = /^\d{2}-\d{2}-\d{4}$/;

export default function Form93Page() {
  const {
    register,
    handleSubmit,
    watch,
    reset,
    formState: { errors },
  } = useForm<Form93FormValues>({ defaultValues, mode: "onBlur" });

  const [loading, setLoading] = useState(false);
  //const [successUrl, setSuccessUrl] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const residentialStatus = watch("residential_status");

  const onSubmit = async (values: Form93FormValues) => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const payload = {
        ...values,
        office_address:
          values.office_address.flat ||
          values.office_address.road ||
          values.office_address.pin
            ? values.office_address
            : undefined,
      };
      /*
      const res = await generateForm93(payload);
      if (res.success && res.download_url) {
        setSuccessUrl(res.download_url);
      } else {
        setErrorMsg(res.message || "Something went wrong while generating the PDF.");
      }*/
     await generateForm93(payload);
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      if (Array.isArray(detail)) {
        setErrorMsg(detail.map((d: any) => d.msg).join(", "));
      } else if (typeof detail === "string") {
        setErrorMsg(detail);
      } else {
        setErrorMsg("Could not reach the backend. Is it running on port 8000?");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    reset(defaultValues);
    setErrorMsg(null);
    //setSuccessUrl(null);
    setErrorMsg(null);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6">
      <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* LEFT: Digital Form */}
        <div>
          <div className="section-card">
            <h2 className="section-title">1. Personal Information</h2>
            <div className="grid grid-cols-3 gap-3 mb-3">
              <div>
                <label className="field-label">First Name *</label>
                <input
                  className={`field-input ${errors.first_name ? "field-input-error" : ""}`}
                  {...register("first_name", { required: "First name is required" })}
                />
                {errors.first_name && <p className="field-error-text">{errors.first_name.message}</p>}
              </div>
              <div>
                <label className="field-label">Middle Name</label>
                <input className="field-input" {...register("middle_name")} />
              </div>
              <div>
                <label className="field-label">Last Name</label>
                <input className="field-input" {...register("last_name")} />
              </div>
            </div>

            <p className="text-xs font-semibold text-slate-500 mt-4 mb-2">Name (as per Aadhaar)</p>
            <div className="grid grid-cols-3 gap-3 mb-4">
              <input className="field-input" placeholder="First name" {...register("aadhaar_first_name")} />
              <input className="field-input" placeholder="Middle name" {...register("aadhaar_middle_name")} />
              <input className="field-input" placeholder="Last name" {...register("aadhaar_last_name")} />
            </div>

            <div className="grid grid-cols-3 gap-3 mb-4">
              <div>
                <label className="field-label">Gender *</label>
                <div className="flex gap-2">
                  {(["male", "female", "transgender"] as const).map((g) => (
                    <label key={g} className="radio-pill flex-1 justify-center capitalize">
                      <input type="radio" value={g} {...register("gender", { required: true })} />
                      {g}
                    </label>
                  ))}
                </div>
                {errors.gender && <p className="field-error-text">Gender is required</p>}
              </div>
              <div>
                <label className="field-label">Date of Birth (dd-mm-yyyy) *</label>
                <input
                  className={`field-input ${errors.dob ? "field-input-error" : ""}`}
                  placeholder="15-08-1995"
                  {...register("dob", {
                    required: "Date of birth is required",
                    pattern: { value: DATE_RE, message: "Use dd-mm-yyyy format" },
                  })}
                />
                {errors.dob && <p className="field-error-text">{errors.dob.message}</p>}
              </div>
              <div>
                <label className="field-label">Aadhaar Number</label>
                <input
                  className={`field-input ${errors.aadhaar_number ? "field-input-error" : ""}`}
                  placeholder="12 digits"
                  maxLength={12}
                  {...register("aadhaar_number", {
                    pattern: { value: AADHAAR_RE, message: "Must be 12 digits" },
                  })}
                />
                {errors.aadhaar_number && (
                  <p className="field-error-text">{errors.aadhaar_number.message}</p>
                )}
              </div>
            </div>

            <AddressFields
              prefix="residence_address"
              register={register}
              errors={errors}
              title="5. Residence Address"
            />
          </div>

          <div className="section-card">
            <h2 className="section-title">6. Office Address (optional)</h2>
            <AddressFields
              prefix="office_address"
              register={register}
              errors={errors}
              title=""
            />
          </div>

          <div className="section-card">
            <h2 className="section-title">7-10. Status & Contact</h2>
            <div className="grid grid-cols-3 gap-2 mb-4">
              {[
                { v: "resident", l: "Resident" },
                { v: "non_resident", l: "Non Resident" },
                { v: "rnor", l: "Resident but Not Ordinarily Resident" },
              ].map((opt) => (
                <label key={opt.v} className="radio-pill justify-center text-center">
                  <input type="radio" value={opt.v} {...register("residential_status", { required: true })} />
                  {opt.l}
                </label>
              ))}
            </div>
            {errors.residential_status && (
              <p className="field-error-text -mt-3 mb-3">Residential status is required</p>
            )}

            <div className="grid grid-cols-2 gap-3 mb-3">
              <div>
                <label className="field-label">
                  Passport Number{" "}
                  {(residentialStatus === "non_resident" || residentialStatus === "rnor") && "*"}
                </label>
                <input
                  className={`field-input ${errors.passport_number ? "field-input-error" : ""}`}
                  {...register("passport_number", {
                    required:
                      residentialStatus === "non_resident" || residentialStatus === "rnor"
                        ? "Passport number is mandatory for this residential status"
                        : false,
                  })}
                />
                {errors.passport_number && (
                  <p className="field-error-text">{errors.passport_number.message}</p>
                )}
              </div>
              <div>
                <label className="field-label">TIN (Country of Residence)</label>
                <input className="field-input" {...register("tin")} />
              </div>
            </div>

            <div className="grid grid-cols-4 gap-3">
              <div>
                <label className="field-label">Country Code</label>
                <input className="field-input" {...register("contact.country_code")} />
              </div>
              <div className="col-span-2">
                <label className="field-label">Mobile Number *</label>
                <input
                  className={`field-input ${(errors.contact as any)?.mobile ? "field-input-error" : ""}`}
                  maxLength={10}
                  {...register("contact.mobile", {
                    required: "Mobile number is required",
                    pattern: { value: MOBILE_RE, message: "Must be 10 digits" },
                  })}
                />
                {(errors.contact as any)?.mobile && (
                  <p className="field-error-text">{(errors.contact as any).mobile.message}</p>
                )}
              </div>
              <div>
                <label className="field-label">STD Code</label>
                <input className="field-input" {...register("contact.std_code")} />
              </div>
              <div className="col-span-3">
                <label className="field-label">Email ID *</label>
                <input
                  type="email"
                  className={`field-input ${(errors.contact as any)?.email ? "field-input-error" : ""}`}
                  {...register("contact.email", { required: "Email is required" })}
                />
                {(errors.contact as any)?.email && (
                  <p className="field-error-text">{(errors.contact as any).email.message}</p>
                )}
              </div>
              <div>
                <label className="field-label">Landline Number</label>
                <input className="field-input" {...register("contact.landline")} />
              </div>
            </div>
          </div>

          <div className="section-card">
            <h2 className="section-title">11. Source of Income</h2>
            <div className="grid grid-cols-3 gap-2">
              {[
                { k: "income_salary", l: "Salary" },
                { k: "income_business", l: "Business / Profession" },
                { k: "income_house_property", l: "House Property" },
                { k: "income_capital_gains", l: "Capital Gains" },
                { k: "income_other_sources", l: "Other Sources" },
                { k: "income_none", l: "No Income" },
              ].map((opt) => (
                <label key={opt.k} className="radio-pill text-center justify-center">
                  <input type="checkbox" {...register(opt.k as any)} />
                  {opt.l}
                </label>
              ))}
            </div>
          </div>

          <div className="section-card">
            <h2 className="section-title">12-15. Details of Parents</h2>
            <div className="mb-3">
              <label className="field-label">Single Parent?</label>
              <div className="flex gap-2">
                {(["yes", "no"] as const).map((v) => (
                  <label key={v} className="radio-pill flex-1 justify-center capitalize">
                    <input type="radio" value={v} {...register("single_parent")} />
                    {v}
                  </label>
                ))}
              </div>
            </div>
            <p className="text-xs font-semibold text-slate-500 mb-2">Father's Name</p>
            <div className="grid grid-cols-3 gap-3 mb-3">
              <input className="field-input" placeholder="First" {...register("father_first_name")} />
              <input className="field-input" placeholder="Middle" {...register("father_middle_name")} />
              <input className="field-input" placeholder="Last" {...register("father_last_name")} />
            </div>
            <p className="text-xs font-semibold text-slate-500 mb-2">Mother's Name</p>
            <div className="grid grid-cols-3 gap-3 mb-3">
              <input className="field-input" placeholder="First" {...register("mother_first_name")} />
              <input className="field-input" placeholder="Middle" {...register("mother_middle_name")} />
              <input className="field-input" placeholder="Last" {...register("mother_last_name")} />
            </div>
            <div>
              <label className="field-label">Parent name to print on PAN card</label>
              <div className="flex gap-2">
                {(["father", "mother"] as const).map((v) => (
                  <label key={v} className="radio-pill flex-1 justify-center capitalize">
                    <input type="radio" value={v} {...register("parent_to_print")} />
                    {v}
                  </label>
                ))}
              </div>
            </div>
          </div>

          <div className="section-card">
            <h2 className="section-title">16. Assessing Officer (AO Code)</h2>
            <div className="grid grid-cols-4 gap-3">
              <div>
                <label className="field-label">Area Code</label>
                <input className="field-input" {...register("ao_code.area_code")} />
              </div>
              <div>
                <label className="field-label">AO Type</label>
                <input className="field-input" {...register("ao_code.ao_type")} />
              </div>
              <div>
                <label className="field-label">Range Code</label>
                <input className="field-input" {...register("ao_code.range_code")} />
              </div>
              <div>
                <label className="field-label">AO Number</label>
                <input className="field-input" {...register("ao_code.ao_number")} />
              </div>
            </div>
          </div>

          <div className="section-card">
            <h2 className="section-title">17-21. Representative Assessee (if applicable)</h2>
            <div className="grid grid-cols-3 gap-3 mb-3">
              <input className="field-input" placeholder="First name" {...register("ra_first_name")} />
              <input className="field-input" placeholder="Middle name" {...register("ra_middle_name")} />
              <input className="field-input" placeholder="Last name" {...register("ra_last_name")} />
            </div>
            <div className="grid grid-cols-2 gap-3 mb-4">
              <div>
                <label className="field-label">PAN (if any)</label>
                <input className="field-input" {...register("ra_pan")} />
              </div>
              <div>
                <label className="field-label">Aadhaar (if PAN not available)</label>
                <input className="field-input" maxLength={12} {...register("ra_aadhaar")} />
              </div>
            </div>
            <AddressFields prefix="ra_address" register={register} errors={errors} title="Representative Assessee Address" />
            <div className="grid grid-cols-4 gap-3 mt-3">
              <input className="field-input" placeholder="Country Code" {...register("ra_contact.country_code")} />
              <input className="field-input col-span-2" placeholder="Mobile Number" {...register("ra_contact.mobile")} />
              <input className="field-input" placeholder="STD Code" {...register("ra_contact.std_code")} />
              <input className="field-input col-span-3" placeholder="Email ID" {...register("ra_contact.email")} />
              <input className="field-input" placeholder="Landline" {...register("ra_contact.landline")} />
            </div>
          </div>

          <div className="section-card">
            <h2 className="section-title">22. Communication Address</h2>
            <div className="grid grid-cols-3 gap-2">
              {[
                { v: "residence", l: "Residence Address" },
                { v: "representative", l: "Representative Assessee Address" },
                { v: "office", l: "Office Address" },
              ].map((opt) => (
                <label key={opt.v} className="radio-pill text-center justify-center">
                  <input type="radio" value={opt.v} {...register("communication_address")} />
                  {opt.l}
                </label>
              ))}
            </div>
          </div>

          <div className="section-card">
            <h2 className="section-title">23-24. Document Proof Checkboxes</h2>
            <p className="text-xs font-semibold text-slate-500 mb-2">Applicant Proofs</p>
            <div className="grid grid-cols-3 gap-2 mb-4">
              <label className="radio-pill justify-center"><input type="checkbox" {...register("proof_identity")} /> Proof of Identity</label>
              <label className="radio-pill justify-center"><input type="checkbox" {...register("proof_address")} /> Proof of Address</label>
              <label className="radio-pill justify-center"><input type="checkbox" {...register("proof_dob")} /> Proof of DOB</label>
            </div>
            <p className="text-xs font-semibold text-slate-500 mb-2">Representative Assessee Proofs</p>
            <div className="grid grid-cols-2 gap-2">
              <label className="radio-pill justify-center"><input type="checkbox" {...register("ra_proof_identity")} /> Proof of Identity</label>
              <label className="radio-pill justify-center"><input type="checkbox" {...register("ra_proof_address")} /> Proof of Address</label>
            </div>
          </div>

          <div className="section-card">
            <h2 className="section-title">Verification &amp; Declaration</h2>
            <div className="grid grid-cols-2 gap-3 mb-3">
              <div>
                <label className="field-label">Declarant Name</label>
                <input className="field-input" {...register("declarant_name")} />
              </div>
              <div>
                <label className="field-label">Capacity</label>
                <div className="flex gap-2">
                  {(["self", "representative"] as const).map((v) => (
                    <label key={v} className="radio-pill flex-1 justify-center capitalize">
                      <input type="radio" value={v} {...register("declarant_capacity")} />
                      {v}
                    </label>
                  ))}
                </div>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3 mb-3">
              <div>
                <label className="field-label">Place</label>
                <input className="field-input" {...register("place")} />
              </div>
              <div>
                <label className="field-label">Date (dd-mm-yyyy)</label>
                <input
                  className={`field-input ${errors.decl_date ? "field-input-error" : ""}`}
                  placeholder="30-06-2026"
                  {...register("decl_date", {
                    pattern: { value: DATE_RE, message: "Use dd-mm-yyyy format" },
                  })}
                />
                {errors.decl_date && <p className="field-error-text">{errors.decl_date.message}</p>}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="field-label">Name (printed under signature)</label>
                <input className="field-input" {...register("signatory_name")} />
              </div>
              <div>
                <label className="field-label">Designation</label>
                <input className="field-input" {...register("designation")} />
              </div>
            </div>
          </div>
        </div>

       {/* RIGHT: Info / Preview panel */}
<div className="lg:sticky lg:top-6 lg:self-start">
  <div className="section-card">
    <h2 className="section-title">Instructions to Complete PAN Application</h2>

    <ol className="text-sm text-slate-700 list-decimal pl-5 space-y-2">
      <li>Fill in all the required details carefully and verify the information before proceeding.</li>

      <li>Click <strong>Generate PDF</strong> to create your filled PAN application form.</li>

      <li>Click <strong>Download PDF</strong> and save the generated file to your device.</li>

      <li>Take a clear printout of the downloaded PDF on A4-size paper.</li>

      <li>Paste one recent passport-size photograph in the photograph box provided on the first page.</li>

      <li>
        Sign the application using a <strong>black ink pen</strong>:
        <ul className="list-disc pl-5 mt-2 space-y-1">
          <li>On the first page, sign across the photograph from shoulder to shoulder.</li>
          <li>On the second page, sign inside the signature box provided at the bottom of the form.</li>
          <li><strong>Do not allow your signature to touch or cross the borders of the signature box.</strong></li>
          <li>Ensure the signature is clear, complete, and remains entirely within the box.</li>
        </ul>
      </li>
    </ol>
  </div>
          {/*successUrl && (
            <div className="section-card border-emerald-300">
              <h2 className="section-title text-emerald-700 border-emerald-200">PDF Ready</h2>
              <p className="text-sm text-slate-600 mb-3">
                Your filled Form 93 has been generated successfully.
              </p>
              <a
                href={downloadUrlFor(successUrl)}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center justify-center w-full px-4 py-2.5 rounded-md bg-emerald-600 text-white text-sm font-semibold hover:bg-emerald-700 transition"
              >
                Download Filled PDF
              </a>
            </div>
          )*/}

          <div className="section-card">
            <h2 className="section-title">Action Bar</h2>
            <div className="flex flex-col gap-3">
              <button
                type="submit"
                disabled={loading}
                className="w-full px-4 py-3 rounded-md bg-govblue-700 text-white font-semibold hover:bg-govblue-800 transition disabled:opacity-60"
              >
                {loading ? <Loader label="Generating PDF..." /> : "Generate PDF"}
              </button>
              {/*successUrl && (
                <a
                  href={downloadUrlFor(successUrl)}
                  target="_blank"
                  rel="noreferrer"
                  className="w-full text-center px-4 py-3 rounded-md border border-govblue-300 text-govblue-800 font-semibold hover:bg-govblue-50 transition"
                >
                  Download PDF
                </a>
              )*/}
              <button
                type="button"
                onClick={handleReset}
                className="w-full px-4 py-3 rounded-md border border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 transition"
              >
                Reset Form
              </button>
            </div>
          </div>
        </div>
      </form>

      <Dialog open={!!errorMsg} onClose={() => setErrorMsg(null)} title="Could not generate PDF" tone="error">
        {errorMsg}
      </Dialog>
    </div>
  );
}
