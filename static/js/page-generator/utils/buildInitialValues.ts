import { JSONSchema } from "../types";

/**
 * Deep-read a value at a dot-separated path inside a potentially nested
 * object/array structure.  Array segments are addressed by their numeric index.
 */
export const getNestedValue = (
  obj: Record<string, unknown>,
  path: string
): unknown => {
  return path
    .split(".")
    .reduce<unknown>((current, part) => {
      if (current === undefined || current === null) return undefined;
      if (typeof current === "object") {
        return (current as Record<string, unknown>)[part];
      }
      return undefined;
    }, obj);
};

/**
 * Return a new (shallow-cloned at each level) object with `value` set at the
 * dot-separated `path`, handling array segments by numeric index.
 */
export const setNestedValue = (
  obj: Record<string, unknown>,
  path: string,
  value: unknown
): Record<string, unknown> => {
  const parts = path.split(".");

  const setAt = (current: unknown, remaining: string[]): unknown => {
    if (remaining.length === 0) return value;

    const [head, ...rest] = remaining;
    const index = Number(head);

    if (!isNaN(index) && Array.isArray(current)) {
      const arr = [...current];
      arr[index] = setAt(arr[index], rest);
      return arr;
    }

    const currentObj =
      typeof current === "object" && current !== null
        ? { ...(current as Record<string, unknown>) }
        : ({} as Record<string, unknown>);

    return {
      ...currentObj,
      [head]: setAt((currentObj as Record<string, unknown>)[head], rest),
    };
  };

  return setAt(obj, parts) as Record<string, unknown>;
};

const buildBySchema = (schema?: JSONSchema): unknown => {
  if (!schema) {
    return undefined;
  }

  if (schema.default !== undefined) {
    return schema.default;
  }

  if (schema.type === "object" && schema.properties) {
    const result: Record<string, unknown> = {};

    Object.entries(schema.properties).forEach(([key, childSchema]) => {
      const childValue = buildBySchema(childSchema);

      if (childValue !== undefined) {
        result[key] = childValue;
      }
    });

    return result;
  }

  if (schema.type === "array") {
    return [];
  }

  if (schema.type === "boolean") {
    return false;
  }

  if (schema.type === "string") {
    return "";
  }

  return undefined;
};

export const buildInitialValues = (
  dataSchema: JSONSchema
): Record<string, unknown> => {
  const built = buildBySchema(dataSchema);

  if (typeof built === "object" && built !== null) {
    return built as Record<string, unknown>;
  }

  return {};
};
