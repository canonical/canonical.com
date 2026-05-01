import {
  Button,
  CheckboxInput,
  Input,
  Select,
  Textarea,
} from "@canonical/react-components";
import { JSONSchema, UIFieldSchema } from "../../types";
import { getNestedValue, setNestedValue } from "../../utils/buildInitialValues";
import BlockCard from "./BlockCard";

// Navigate a JSON Schema via a dot-separated path through .properties.
// Mirrors the same helper in SchemaForm but kept local to avoid circular deps.
const getSchemaAtPath = (
  schema: JSONSchema | undefined,
  path: string
): JSONSchema | undefined => {
  if (!schema) return undefined;
  return path.split(".").reduce<JSONSchema | undefined>((current, segment) => {
    if (!current?.properties?.[segment]) return undefined;
    return current.properties[segment];
  }, schema);
};

// Resolve a dot-path that may start with "../../" — those paths are relative to
// the containing block, not to the current item's own values.
const resolveConditionValue = (
  path: string,
  itemValues: Record<string, unknown>,
  contextValues: Record<string, unknown>
): unknown => {
  if (path.startsWith("../../")) {
    return getNestedValue(contextValues, path.slice(6));
  }
  return getNestedValue(itemValues, path);
};

const isItemFieldVisible = (
  field: UIFieldSchema,
  itemValues: Record<string, unknown>,
  contextValues: Record<string, unknown>
): boolean => {
  const conditions = field["ui:conditions"]?.visibleWhen;
  if (!conditions) return true;
  return Object.entries(conditions).every(([path, expected]) => {
    const actual = resolveConditionValue(path, itemValues, contextValues);
    return Array.isArray(expected)
      ? expected.includes(actual as string)
      : actual === expected;
  });
};

// Build a fresh item pre-populated with empty defaults for every field in the
// item schema.  We initialize ALL fields (not just "default" visibility) so
// that dot-path keys like "image.attrs.src" are always present in the object —
// if they were absent, the backend's JSON Schema validation would reject the
// payload even when the user fills in a sibling field (e.g. image.attrs.alt).
// Select widgets are skipped: submitting an empty string for an enum field
// would cause a schema validation error.
const buildDefaultItem = (
  itemSchema: Record<string, UIFieldSchema>
): Record<string, unknown> => {
  let item: Record<string, unknown> = {};
  for (const [key, field] of Object.entries(itemSchema)) {
    if (field["ui:widget"] === "select") continue;
    if (field["ui:widget"] === "checkbox") {
      item = setNestedValue(item, key, false);
    } else if (
      field["ui:multiplicity"] === "multiple" ||
      field["ui:widget"] === "resource-card-list"
    ) {
      item = setNestedValue(item, key, []);
    } else {
      item = setNestedValue(item, key, "");
    }
  }
  return item;
};

interface Props {
  label: string;
  value: Record<string, unknown>[];
  onChange: (items: Record<string, unknown>[]) => void;
  /** The UI schema for this list field (provides ui:itemSchema, ui:maxItems, etc.) */
  fieldDef: UIFieldSchema;
  /** JSON Schema for this array field — used to extract enum options for select widgets. */
  jsonSchema?: JSONSchema;
  /**
   * Values from the containing block (e.g. { render_images: true, ... }).
   * Needed to resolve "../../<field>" condition paths used in resource-card schemas.
   */
  contextValues?: Record<string, unknown>;
}

// Single item editor — renders one row of the list as a collapsible BlockCard.
interface ItemEditorProps {
  index: number;
  item: Record<string, unknown>;
  itemSchema: Record<string, UIFieldSchema>;
  jsonSchema?: JSONSchema;
  contextValues: Record<string, unknown>;
  parentLabel: string;
  onUpdate: (updated: Record<string, unknown>) => void;
  onRemove: () => void;
}

const ItemEditor = ({
  index,
  item,
  itemSchema,
  jsonSchema,
  contextValues,
  parentLabel,
  onUpdate,
  onRemove,
}: ItemEditorProps) => {
  const getVal = (path: string): unknown => getNestedValue(item, path);
  const setVal = (path: string, v: unknown) =>
    onUpdate(setNestedValue({ ...item }, path, v));

  return (
    <BlockCard title={`${parentLabel} ${index + 1}`} onRemove={onRemove}>
      {Object.entries(itemSchema).map(([fieldKey, field]) => {
        if (!isItemFieldVisible(field, item, contextValues)) return null;

        const currentVal = getVal(fieldKey);
        const inputId = `rce-${index}-${fieldKey.replace(/\./g, "-")}`;

        // Nested list — render recursively, passing the matching sub-schema.
        if (field["ui:widget"] === "resource-card-list") {
          const nestedJsonSchema = jsonSchema?.items
            ? getSchemaAtPath(jsonSchema.items, fieldKey)
            : undefined;
          return (
            <div key={fieldKey} className="u-sv2">
              <p className="p-form__label u-no-margin--bottom">
                {field["ui:label"]}
              </p>
              <ResourceCardEditor
                label={field["ui:label"]}
                value={(currentVal as Record<string, unknown>[]) || []}
                onChange={(val) => setVal(fieldKey, val)}
                fieldDef={field}
                jsonSchema={nestedJsonSchema}
                // Pass same contextValues so "../../" paths keep working at any depth.
                contextValues={contextValues}
              />
            </div>
          );
        }

        if (field["ui:widget"] === "textarea") {
          return (
            <Textarea
              key={fieldKey}
              id={inputId}
              label={field["ui:label"]}
              rows={field["ui:rows"] || 3}
              required={field["ui:required"]}
              value={String(currentVal ?? "")}
              onChange={(e) => setVal(fieldKey, e.target.value)}
            />
          );
        }

        if (field["ui:widget"] === "select") {
          // Look up the enum list from the JSON Schema for this specific field.
          const fieldJsonSchema = jsonSchema?.items
            ? getSchemaAtPath(jsonSchema.items, fieldKey)
            : undefined;
          const enumOptions = fieldJsonSchema?.enum ?? [];
          return (
            <Select
              key={fieldKey}
              id={inputId}
              label={field["ui:label"]}
              required={field["ui:required"]}
              value={String(currentVal ?? "")}
              onChange={(e) => setVal(fieldKey, e.target.value)}
              options={[
                {
                  label: `Choose ${field["ui:label"].toLowerCase()}`,
                  value: "",
                  disabled: true,
                },
                ...enumOptions.map((v) => ({
                  label: String(v),
                  value: String(v),
                })),
              ]}
            />
          );
        }

        if (field["ui:widget"] === "checkbox") {
          return (
            <CheckboxInput
              key={fieldKey}
              id={inputId}
              label={field["ui:label"]}
              checked={Boolean(currentVal)}
              onChange={(e) =>
                setVal(fieldKey, (e.target as HTMLInputElement).checked)
              }
            />
          );
        }

        // Default: text input (covers "text" and "link-editor" stubs at item level)
        return (
          <Input
            key={fieldKey}
            id={inputId}
            type="text"
            label={field["ui:label"]}
            required={field["ui:required"]}
            placeholder={field["ui:placeholder"]}
            value={String(currentVal ?? "")}
            onChange={(e) => setVal(fieldKey, e.target.value)}
          />
        );
      })}
    </BlockCard>
  );
};

/**
 * ResourceCardEditor — generic "list of structured items" widget.
 *
 * Used for:
 *  - resources pattern: `categories` (categories → items → title/description/image/metadata)
 *  - basic-section pattern: `list_items`, `logos`, `links` (flat lists)
 *
 * Each item's fields are driven by `fieldDef["ui:itemSchema"]`.
 * Nested resource-card-list fields are handled recursively.
 */
const ResourceCardEditor = ({
  label,
  value,
  onChange,
  fieldDef,
  jsonSchema,
  contextValues = {},
}: Props) => {
  const itemSchema = fieldDef["ui:itemSchema"] ?? {};
  const maxItems = fieldDef["ui:maxItems"];
  const canAdd = maxItems === undefined || value.length < maxItems;

  const addItem = () => {
    onChange([...value, buildDefaultItem(itemSchema)]);
  };

  const updateItem = (index: number, updated: Record<string, unknown>) => {
    const next = [...value];
    next[index] = updated;
    onChange(next);
  };

  const removeItem = (index: number) => {
    onChange(value.filter((_, i) => i !== index));
  };

  return (
    <div className="u-sv2">
      {value.map((item, index) => (
        <ItemEditor
          key={index}
          index={index}
          item={item}
          itemSchema={itemSchema}
          jsonSchema={jsonSchema}
          contextValues={contextValues}
          parentLabel={label}
          onUpdate={(updated) => updateItem(index, updated)}
          onRemove={() => removeItem(index)}
        />
      ))}
      {canAdd && (
        <Button type="button" appearance="base" onClick={addItem}>
          Add {label}
        </Button>
      )}
    </div>
  );
};

export default ResourceCardEditor;
