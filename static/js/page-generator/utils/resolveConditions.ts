import {
  SchemaDefinition,
  UIBlockSchema,
  UICondition,
  UIFieldSchema,
} from "../types";

const getValueByPath = (
  values: Record<string, unknown>,
  path: string
): unknown => {
  const pathParts = path.split(".").filter(Boolean);
  let current: unknown = values;

  for (const part of pathParts) {
    if (typeof current !== "object" || current === null) {
      return undefined;
    }

    current = (current as Record<string, unknown>)[part];
  }

  return current;
};

const matchesCondition = (
  values: Record<string, unknown>,
  condition?: UICondition
): boolean => {
  if (!condition) {
    return true;
  }

  return Object.entries(condition).every(([path, expected]) => {
    const actual = getValueByPath(values, path);

    if (Array.isArray(expected)) {
      return expected.includes(String(actual));
    }

    return actual === expected;
  });
};

export const isVisible = (
  field: UIFieldSchema,
  values: Record<string, unknown>
): boolean => {
  return matchesCondition(values, field["ui:conditions"]?.visibleWhen);
};

export const isBlockVisible = (
  block: UIBlockSchema,
  values: Record<string, unknown>
): boolean => {
  return matchesCondition(values, block["ui:conditions"]?.visibleWhen);
};

export const isRequired = (
  field: UIFieldSchema,
  values: Record<string, unknown>
): boolean => {
  if (field["ui:required"]) {
    return true;
  }

  const condition = field["ui:conditions"]?.requiredWhen;
  if (!condition) return false;
  return matchesCondition(values, condition);
};

const isFilled = (value: unknown): boolean => {
  if (value === undefined || value === null) return false;
  if (typeof value === "string") return value.trim().length > 0;
  if (Array.isArray(value)) return value.length > 0;
  if (typeof value === "object")
    return Object.keys(value as Record<string, unknown>).length > 0;
  return true;
};

/**
 * Returns true when every required top-level field in the section
 * has a non-empty value.
 */
export const areSectionRequiredFieldsFilled = (
  definition: SchemaDefinition,
  data: Record<string, unknown>
): boolean => {
  const fields = definition.uiSchema.fields || {};
  for (const [key, field] of Object.entries(fields)) {
    if (!isVisible(field, data)) continue;
    if (!isRequired(field, data)) continue;
    if (!isFilled(getValueByPath(data, key))) return false;
  }
  return true;
};
