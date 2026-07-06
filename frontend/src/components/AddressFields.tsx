import { UseFormRegister, FieldErrors } from "react-hook-form";
import { Form93FormValues } from "../lib/types";

interface Props {
  prefix:
    | "residence_address"
    | "office_address"
    | "ra_address";
  register: UseFormRegister<Form93FormValues>;
  errors: FieldErrors<Form93FormValues>;
  title: string;
}

export default function AddressFields({ prefix, register, errors, title }: Props) {
  const addressErrors = (errors as any)[prefix] || {};

  return (
    <div>
      <p className="text-xs font-semibold text-slate-500 mb-2">{title}</p>
      <div className="grid grid-cols-2 gap-3">
        <div className="col-span-2">
          <label className="field-label">Flat / Door / Building</label>
          <input className="field-input" {...register(`${prefix}.flat` as any)} />
        </div>
        <div className="col-span-2">
          <label className="field-label">Road / Street / Block / Sector</label>
          <input className="field-input" {...register(`${prefix}.road` as any)} />
        </div>
        <div>
          <label className="field-label">Post Office</label>
          <input className="field-input" {...register(`${prefix}.post_office` as any)} />
        </div>
        <div>
          <label className="field-label">Area / Locality / Town / City</label>
          <input className="field-input" {...register(`${prefix}.area` as any)} />
        </div>
        <div>
          <label className="field-label">District</label>
          <input className="field-input" {...register(`${prefix}.district` as any)} />
        </div>
        <div>
          <label className="field-label">State / Union Territory</label>
          <input className="field-input" {...register(`${prefix}.state` as any)} />
        </div>
        <div>
          <label className="field-label">Country / Region</label>
          <input className="field-input" {...register(`${prefix}.country` as any)} />
        </div>
        <div>
          <label className="field-label">PIN / ZIP Code</label>
          <input
            className={`field-input ${addressErrors.pin ? "field-input-error" : ""}`}
            maxLength={6}
            placeholder="6 digits"
            {...register(`${prefix}.pin` as any)}
          />
          {addressErrors.pin && (
            <p className="field-error-text">{addressErrors.pin.message}</p>
          )}
        </div>
      </div>
    </div>
  );
}
