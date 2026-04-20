import { JSONSchema } from "../types";

/**
 * Recursively dereferences all local `$ref` pointers (e.g.
 * "#/definitions/descriptionBlock") in a JSON Schema tree, inlining the
 * referenced sub-schemas so that downstream code can navigate the schema
 * without worrying about indirection.
 *
 * Only handles document-local references (those starting with "#/").
 */
export const resolveRefs = (rootSchema: JSONSchema): JSONSchema => {
  // Keep a visited set to avoid infinite loops on circular refs
  const visiting = new WeakSet<object>();

  const resolveNode = (node: JSONSchema): JSONSchema => {
    if (!node || typeof node !== "object") return node;

    // Resolve $ref first — look up the target in the root schema
    if (node.$ref) {
      const refPath = node.$ref.replace(/^#\//, "").split("/");
      let target: unknown = rootSchema;

      for (const segment of refPath) {
        if (target && typeof target === "object") {
          target = (target as Record<string, unknown>)[segment];
        } else {
          target = undefined;
          break;
        }
      }

      if (target && typeof target === "object") {
        if (visiting.has(target as object)) {
          // Circular reference — return as-is to avoid infinite recursion
          return target as JSONSchema;
        }
        return resolveNode(target as JSONSchema);
      }

      // If the ref can't be resolved, return the node unchanged
      return node;
    }

    if (visiting.has(node)) return node;
    visiting.add(node);

    const resolved: JSONSchema = { ...node };

    if (resolved.properties) {
      resolved.properties = Object.fromEntries(
        Object.entries(resolved.properties).map(([key, value]) => [
          key,
          resolveNode(value),
        ])
      );
    }

    if (resolved.items) {
      resolved.items = resolveNode(resolved.items);
    }

    if (resolved.oneOf) {
      resolved.oneOf = resolved.oneOf.map((s) => resolveNode(s));
    }

    if (resolved.anyOf) {
      resolved.anyOf = resolved.anyOf.map((s) => resolveNode(s));
    }

    if (resolved.allOf) {
      resolved.allOf = resolved.allOf.map((s) => resolveNode(s));
    }

    if (resolved.definitions) {
      resolved.definitions = Object.fromEntries(
        Object.entries(resolved.definitions).map(([key, value]) => [
          key,
          resolveNode(value),
        ])
      );
    }

    visiting.delete(node);
    return resolved;
  };

  return resolveNode(rootSchema);
};

/**
 * Given the `items` schema of a blocks array (which typically contains a
 * `oneOf` with discriminated block types), find the branch that matches the
 * supplied `blockType` by checking `properties.type.const`.
 *
 * Falls back to returning the schema itself if there is no `oneOf`.
 */
export const findBlockSchema = (
  itemsSchema: JSONSchema | undefined,
  blockType: string
): JSONSchema | undefined => {
  if (!itemsSchema) return undefined;

  if (itemsSchema.oneOf) {
    return itemsSchema.oneOf.find(
      (branch) => branch.properties?.type?.const === blockType
    );
  }

  // No oneOf — return the schema directly (single-type items array)
  if (itemsSchema.properties) {
    return itemsSchema;
  }

  return undefined;
};
