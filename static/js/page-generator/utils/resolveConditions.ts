import { UICondition, UIFieldSchema } from "../types";

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

export const isRequired = (
  field: UIFieldSchema,
  values: Record<string, unknown>
): boolean => {
  if (field["ui:required"]) {
    return true;
  }

  return matchesCondition(values, field["ui:conditions"]?.requiredWhen);
};
