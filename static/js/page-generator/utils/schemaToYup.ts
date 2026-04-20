import * as Yup from "yup";
import { JSONSchema } from "../types";

const inferYupType = (schema: JSONSchema): Yup.AnySchema => {
  if (schema.type === "boolean") {
    return Yup.boolean();
  }

  if (schema.type === "array") {
    return Yup.array();
  }

  if (schema.type === "object") {
    return Yup.object();
  }

  return Yup.string();
};

export const buildYupSchema = (dataSchema: JSONSchema): Yup.ObjectSchema<any> => {
  const shape: Record<string, Yup.AnySchema> = {};

  Object.entries(dataSchema.properties || {}).forEach(([key, fieldSchema]) => {
    let validator = inferYupType(fieldSchema);

    if (Array.isArray(dataSchema.required) && dataSchema.required.includes(key)) {
      validator = validator.required("Required");
    }

    if (fieldSchema.enum && fieldSchema.enum.length > 0) {
      validator = validator.oneOf(fieldSchema.enum);
    }

    shape[key] = validator;
  });

  return Yup.object().shape(shape);
};
