import {
  Button,
  CheckboxInput,
  Input,
  Notification,
  Select,
  Textarea,
} from "@canonical/react-components";
import { ReactNode, useEffect, useMemo, useRef, useState } from "react";
import AddFieldDropdown from "./AddFieldDropdown";
import BlockCard from "./widgets/BlockCard";
import LinkEditor from "./widgets/LinkEditor";
import RadioGroupWidget from "./widgets/RadioGroupWidget";
import ResourceCardEditor from "./widgets/ResourceCardEditor";
import SegmentedControlWidget from "./widgets/SegmentedControlWidget";
import {
  buildInitialValues,
  getNestedValue,
  setNestedValue,
} from "../utils/buildInitialValues";
import {
  isBlockVisible,
  isRequired,
  isVisible,
} from "../utils/resolveConditions";
import { findBlockSchema, resolveRefs } from "../utils/resolveRefs";
import { JSONSchema, SchemaDefinition, UIFieldSchema } from "../types";

interface Props {
  schemaDefinition: SchemaDefinition;
  value: Record<string, unknown>;
  onChange: (value: Record<string, unknown>) => void;
}

// Return true when a value is considered "filled in" (used to hide addable
// fields once they've been cleared back to empty).
const hasValue = (value: unknown): boolean => {
  if (value === undefined || value === null) return false;
  if (typeof value === "string") return value.trim().length > 0;
  if (Array.isArray(value)) return value.length > 0;
  if (typeof value === "object")
    return Object.keys(value as Record<string, unknown>).length > 0;
  return true;
};

// Navigate a (fully-dereferenced) JSON Schema tree via a dot-separated property
// path.  Only traverses `.properties` — call resolveRefs first so there are no
// $ref indirections left.
const getSchemaAtPath = (
  rootSchema: JSONSchema | undefined,
  path: string,
): JSONSchema | undefined => {
  if (!rootSchema) return undefined;
  return path.split(".").reduce<JSONSchema | undefined>((current, segment) => {
    if (!current) return undefined;
    if (current.properties?.[segment]) return current.properties[segment];
    return undefined;
  }, rootSchema);
};

// Return the appropriate empty / default value for a newly-activated field.
const getDefaultByWidget = (
  field: UIFieldSchema,
  jsonSchema?: JSONSchema,
): unknown => {
  // Fields with sub-groups (e.g. title with text + link) are objects.
  if (field["ui:subfields"]) return {};
  if (field["ui:widget"] === "checkbox") return jsonSchema?.default ?? false;
  if (field["ui:widget"] === "link-editor") {
    return field["ui:multiplicity"] === "multiple"
      ? []
      : { content_html: "", attrs: { href: "" } };
  }
  if (field["ui:multiplicity"] === "multiple") return [];
  return "";
};

const SchemaForm = ({ schemaDefinition, value, onChange }: Props) => {
  // Resolve all $ref pointers once so downstream schema lookups work without
  // any indirection.
  const resolvedSchema = useMemo(
    () => resolveRefs(schemaDefinition.schema),
    [schemaDefinition.schema],
  );
  const dataSchema = resolvedSchema.properties?.data;

  const initialValues = useMemo(
    () => (dataSchema ? buildInitialValues(dataSchema) : {}),
    [dataSchema],
  );

  // Initialise from parent value (preserving user edits across remounts),
  // falling back to schema defaults for new / empty sections.
  const [values, setValues] = useState<Record<string, unknown>>(() => {
    if (value && Object.keys(value).length > 0) {
      return { ...initialValues, ...value };
    }
    return initialValues;
  });
  // Tracks which "addable" top-level fields the user has explicitly added.
  const [activatedFields, setActivatedFields] = useState<Set<string>>(
    new Set(),
  );

  // Stable prefix for DOM IDs so multiple SchemaForm instances don't clash.
  const formId = useRef(`sf-${Math.random().toString(36).slice(2)}`);
  const [pendingScrollId, setPendingScrollId] = useState<string | null>(null);

  // Skip the first onChange call to avoid overwriting parent state on remount.
  const isMounted = useRef(false);

  useEffect(() => {
    if (!pendingScrollId) return;
    document
      .getElementById(pendingScrollId)
      ?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    setPendingScrollId(null);
  }, [pendingScrollId]);

  // Report every change upward to the parent (CreatePageApp).
  useEffect(() => {
    if (!isMounted.current) {
      isMounted.current = true;
      // For brand-new sections push schema defaults so the parent has
      // initial values, but don't overwrite existing data on remount.
      if (!value || Object.keys(value).length === 0) {
        onChange(values);
      }
      return;
    }
    onChange(values);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [values]);

  if (!dataSchema) {
    return (
      <Notification severity="negative" title="Invalid schema shape">
        Missing data schema for this section.
      </Notification>
    );
  }

  const getValueAt = (path: string): unknown => getNestedValue(values, path);
  const setValueAt = (path: string, val: unknown) =>
    setValues((prev) => setNestedValue(prev, path, val));

  const topFields = Object.entries(schemaDefinition.uiSchema.fields || {});

  // The data-model property that holds the repeatable blocks array.
  // Defaults to "blocks" but basic-section overrides it to "items".
  const blocksField = schemaDefinition.uiSchema["$blocksField"] || "blocks";
  const blocks = Array.isArray(values[blocksField])
    ? (values[blocksField] as Array<{
        type?: string;
        item?: Record<string, unknown>;
      }>)
    : [];

  // Addable top-level fields that haven't been activated or filled in yet.
  const topLevelAddable = topFields
    .filter(([, field]) => field["ui:visibility"] === "addable")
    .filter(
      ([fieldKey]) =>
        !activatedFields.has(fieldKey) && !hasValue(getValueAt(fieldKey)),
    )
    .map(([fieldKey, field]) => ({
      value: fieldKey,
      label: field["ui:label"],
    }));

  /**
   * Render a single form field given its UI schema descriptor, full dot-path
   * `name` into the form values, and optional JSON Schema for enum options.
   *
   * `contextValues` is only needed for resource-card-list fields: it provides
   * the containing block's top-level values so that "../../<field>" condition
   * paths (used in the resources pattern) can be resolved.
   */
  const renderField = (
    name: string,
    field: UIFieldSchema,
    fieldSchema?: JSONSchema,
    contextValues?: Record<string, unknown>,
  ): ReactNode => {
    if (!isVisible(field, values)) return null;

    const required = isRequired(field, values);
    const currentValue = getValueAt(name);

    if (field["ui:widget"] === "segmented-control") {
      const options = (fieldSchema?.enum ?? []).map((option) => ({
        label: String(option),
        value: String(option),
      }));
      return (
        <SegmentedControlWidget
          key={name}
          label={field["ui:label"]}
          options={options}
          required={required}
          value={String(currentValue ?? "")}
          onChange={(val) => setValueAt(name, val)}
        />
      );
    }

    if (field["ui:widget"] === "radio-group") {
      const options = (fieldSchema?.enum ?? []).map((option) => ({
        label: String(option),
        value: String(option),
      }));
      return (
        <RadioGroupWidget
          key={name}
          label={field["ui:label"]}
          name={`${formId.current}-${name}`}
          options={options}
          required={required}
          value={String(currentValue ?? "")}
          onChange={(val) => setValueAt(name, val)}
        />
      );
    }

    if (field["ui:widget"] === "textarea") {
      return (
        <Textarea
          key={name}
          id={name}
          label={field["ui:label"]}
          placeholder={field["ui:placeholder"]}
          rows={field["ui:rows"] || 3}
          required={required}
          value={String(currentValue ?? "")}
          onChange={(e) => setValueAt(name, e.target.value)}
        />
      );
    }

    if (field["ui:widget"] === "select") {
      const enumOptions = fieldSchema?.enum ?? [];
      // Coerce to number when the schema type is numeric OR when the enum
      // itself contains numbers (e.g. heading_level: [4, 5] has no explicit
      // type). The select widget always yields strings via e.target.value, so
      // without this the backend rejects "5" because it expects 5.
      const enumHasNumbers = fieldSchema?.enum?.some(
        (v) => typeof v === "number",
      );
      const coerce = (raw: string): string | number => {
        if (!raw) return raw;
        if (
          fieldSchema?.type === "integer" ||
          fieldSchema?.type === "number" ||
          enumHasNumbers
        ) {
          const n = Number(raw);
          return isNaN(n) ? raw : n;
        }
        return raw;
      };
      return (
        <Select
          key={name}
          id={name}
          label={field["ui:label"]}
          required={required}
          value={String(currentValue ?? "")}
          onChange={(e) => setValueAt(name, coerce(e.target.value))}
          options={[
            {
              label: `Choose ${field["ui:label"].toLowerCase()}`,
              value: "",
              disabled: true,
            },
            ...enumOptions.map((enumValue) => ({
              label: String(enumValue),
              value: String(enumValue),
            })),
          ]}
        />
      );
    }

    if (field["ui:widget"] === "checkbox") {
      return (
        <CheckboxInput
          key={name}
          id={name}
          label={field["ui:label"]}
          checked={Boolean(currentValue)}
          onChange={(e) =>
            setValueAt(name, (e.target as HTMLInputElement).checked)
          }
        />
      );
    }

    if (field["ui:widget"] === "link-editor") {
      if (field["ui:multiplicity"] === "multiple") {
        const items = (currentValue as Array<unknown>) || [];
        return (
          <div key={name} className="u-sv2">
            <p className="p-form__label">{field["ui:label"]}</p>
            {items.map((item, index) => (
              <div key={`${name}-${index}`} className="u-sv1">
                <LinkEditor
                  label={`${field["ui:label"]} ${index + 1}`}
                  value={
                    item as { content_html: string; attrs: { href: string } }
                  }
                  onChange={(val) => {
                    const next = [...items];
                    next[index] = val;
                    setValueAt(name, next);
                  }}
                />
                <Button
                  type="button"
                  appearance="negative"
                  onClick={() => {
                    const next = [...items];
                    next.splice(index, 1);
                    setValueAt(name, next);
                  }}
                >
                  Remove
                </Button>
              </div>
            ))}
            <Button
              type="button"
              appearance="base"
              onClick={() =>
                setValueAt(name, [
                  ...items,
                  { content_html: "", attrs: { href: "" } },
                ])
              }
            >
              Add another
            </Button>
          </div>
        );
      }

      return (
        <LinkEditor
          key={name}
          label={field["ui:label"]}
          required={required}
          value={
            currentValue as
              | { content_html: string; attrs: { href: string } }
              | undefined
          }
          onChange={(val) => setValueAt(name, val)}
        />
      );
    }

    if (field["ui:widget"] === "resource-card-list") {
      // Derive block-level context from the parent path so that nested item
      // fields can resolve "../../<field>" condition paths.
      const parts = name.split(".");
      const parentPath = parts.slice(0, -1).join(".");
      const blockData =
        contextValues ??
        (parentPath
          ? (getValueAt(parentPath) as Record<string, unknown>)
          : values);

      return (
        <ResourceCardEditor
          key={name}
          label={field["ui:label"]}
          value={(currentValue as Record<string, unknown>[]) || []}
          onChange={(val) => setValueAt(name, val)}
          fieldDef={field}
          jsonSchema={fieldSchema}
          contextValues={blockData || {}}
        />
      );
    }

    // Default: plain text input
    return (
      <Input
        key={name}
        id={name}
        type="text"
        label={field["ui:label"]}
        required={required}
        placeholder={field["ui:placeholder"]}
        value={String(currentValue ?? "")}
        onChange={(e) => setValueAt(name, e.target.value)}
      />
    );
  };

  const blockDefinitions = Object.entries(
    schemaDefinition.uiSchema.blocks || {},
  );

  // Blocks still available to add (respect maxItems, single-instance, and
  // block-level visibility conditions).
  const addableBlocks = blockDefinitions
    .filter(([, block]) => block["ui:visibility"] === "addable")
    .filter(([, block]) => isBlockVisible(block, values))
    .filter(([blockType, block]) => {
      const count = blocks.filter((b) => b.type === blockType).length;
      if (block["ui:multiplicity"] === "single" && count > 0) return false;
      if (block["ui:maxItems"] && count >= block["ui:maxItems"]) return false;
      return true;
    })
    .map(([blockType, block]) => ({
      value: blockType,
      label: block["ui:label"],
    }));

  const renderSubfields = (
    parentKey: string,
    subfields: Record<string, UIFieldSchema>,
    parentSchema: JSONSchema | undefined,
  ) => {
    const entries = Object.entries(subfields);
    // Default subfields first, then addable subfields that have a value.
    const defaultSubs = entries.filter(
      ([, sf]) => sf["ui:visibility"] !== "addable",
    );
    const activeSubs = entries.filter(
      ([subKey, sf]) =>
        sf["ui:visibility"] === "addable" &&
        hasValue(getValueAt(`${parentKey}.${subKey}`)),
    );
    return [...defaultSubs, ...activeSubs].map(([subKey, subField]) =>
      renderField(
        `${parentKey}.${subKey}`,
        subField,
        getSchemaAtPath(parentSchema, subKey),
      ),
    );
  };

  // Addable subfield options for a given parent field.
  const getAddableSubfieldOptions = (
    parentKey: string,
    subfields: Record<string, UIFieldSchema>,
  ) =>
    Object.entries(subfields)
      .filter(
        ([subKey, sf]) =>
          sf["ui:visibility"] === "addable" &&
          !hasValue(getValueAt(`${parentKey}.${subKey}`)),
      )
      .map(([subKey, sf]) => ({ value: subKey, label: sf["ui:label"] }));

  return (
    <div>
      {/* ── Top-level fields ─────────────────────────────────── */}
      {/* Default-visibility fields render first, in schema order. */}
      {topFields
        .filter(([, field]) => field["ui:visibility"] !== "addable")
        .map(([fieldKey, field]) => {
          const fieldSchema = getSchemaAtPath(dataSchema, fieldKey);
          const subfields = field["ui:subfields"];

          if (subfields) {
            const subfieldAddable = getAddableSubfieldOptions(
              fieldKey,
              subfields,
            );
            return (
              <div
                key={fieldKey}
                id={`${formId.current}-field-${fieldKey}`}
                className="u-sv2"
              >
                <h4 className="p-heading--5">{field["ui:label"]}</h4>
                {renderSubfields(fieldKey, subfields, fieldSchema)}
                {subfieldAddable.length > 0 ? (
                  <AddFieldDropdown
                    label={`Add ${field["ui:label"].toLowerCase()} field`}
                    options={subfieldAddable}
                    onAdd={(subKey) => {
                      const subDef = subfields[subKey];
                      if (!subDef) return;
                      const jsonSub = getSchemaAtPath(fieldSchema, subKey);
                      setValueAt(
                        `${fieldKey}.${subKey}`,
                        getDefaultByWidget(subDef, jsonSub),
                      );
                    }}
                  />
                ) : null}
              </div>
            );
          }

          return (
            <div key={fieldKey} id={`${formId.current}-field-${fieldKey}`}>
              {renderField(fieldKey, field, fieldSchema)}
            </div>
          );
        })}
      {/* Addable fields render after defaults, in activation order. */}
      {topFields
        .filter(
          ([fieldKey, field]) =>
            field["ui:visibility"] === "addable" &&
            (activatedFields.has(fieldKey) || hasValue(getValueAt(fieldKey))),
        )
        .map(([fieldKey, field]) => {
          const fieldSchema = getSchemaAtPath(dataSchema, fieldKey);
          const subfields = field["ui:subfields"];

          if (subfields) {
            const subfieldAddable = getAddableSubfieldOptions(
              fieldKey,
              subfields,
            );
            return (
              <div
                key={fieldKey}
                id={`${formId.current}-field-${fieldKey}`}
                className="u-sv2"
              >
                <h4 className="p-heading--5">{field["ui:label"]}</h4>
                {renderSubfields(fieldKey, subfields, fieldSchema)}
                {subfieldAddable.length > 0 ? (
                  <AddFieldDropdown
                    label={`Add ${field["ui:label"].toLowerCase()} field`}
                    options={subfieldAddable}
                    onAdd={(subKey) => {
                      const subDef = subfields[subKey];
                      if (!subDef) return;
                      const jsonSub = getSchemaAtPath(fieldSchema, subKey);
                      setValueAt(
                        `${fieldKey}.${subKey}`,
                        getDefaultByWidget(subDef, jsonSub),
                      );
                    }}
                  />
                ) : null}
              </div>
            );
          }

          return (
            <div key={fieldKey} id={`${formId.current}-field-${fieldKey}`}>
              {renderField(fieldKey, field, fieldSchema)}
            </div>
          );
        })}

      <div className="u-sv2">
        <AddFieldDropdown
          label="Add field"
          options={topLevelAddable}
          onAdd={(fieldName) => {
            const fieldDef = schemaDefinition.uiSchema.fields?.[fieldName];
            if (!fieldDef) return;
            setActivatedFields((prev) => new Set(prev).add(fieldName));
            const jsonFieldSchema = getSchemaAtPath(dataSchema, fieldName);
            setValueAt(
              fieldName,
              getDefaultByWidget(fieldDef, jsonFieldSchema),
            );
            setPendingScrollId(`${formId.current}-field-${fieldName}`);
          }}
        />
      </div>

      {/* ── Block list ───────────────────────────────────────── */}
      <div className="u-sv2">
        {blocks.map((block, blockIndex) => {
          const blockType = block.type || "unknown";
          const blockSchemaDef = schemaDefinition.uiSchema.blocks?.[blockType];

          if (!blockSchemaDef) {
            return (
              <Notification
                key={blockIndex}
                severity="information"
                title="Unsupported block"
              >
                Block type "{blockType}" is not mapped in the UI schema.
              </Notification>
            );
          }

          // Hide blocks whose visibility condition is not met.
          if (!isBlockVisible(blockSchemaDef, values)) return null;

          // Resolve the matching oneOf branch from the JSON Schema so we can
          // look up enum options and types for individual fields.
          const blocksItemsSchema = getSchemaAtPath(
            dataSchema,
            blocksField,
          )?.items;
          const matchedBlockSchema = findBlockSchema(
            blocksItemsSchema,
            blockType,
          );

          // The resources block stores its fields directly on the block object
          // (no `item` wrapper), unlike all other block types.
          const hasItemWrapper = Boolean(matchedBlockSchema?.properties?.item);

          // Block-level values (used as contextValues for resource-card-list
          // fields so that "../../<field>" conditions can be resolved).
          const blockData = getValueAt(`${blocksField}.${blockIndex}`) as
            | Record<string, unknown>
            | undefined;

          return (
            <div
              key={`${block.type}-${blockIndex}`}
              id={`${formId.current}-block-${blockIndex}`}
            >
              <BlockCard
                title={blockSchemaDef["ui:label"]}
                onRemove={() => {
                  const next = [...blocks];
                  next.splice(blockIndex, 1);
                  setValueAt(blocksField, next);
                }}
              >
                {Object.entries(blockSchemaDef.fields || {}).map(
                  ([fieldKey, field]) => {
                    // Choose whether the data lives at item.<field> or directly
                    // on the block object (resources block has no item wrapper).
                    const fieldPath = hasItemWrapper
                      ? `${blocksField}.${blockIndex}.item.${fieldKey}`
                      : `${blocksField}.${blockIndex}.${fieldKey}`;

                    const blockFieldSchema = hasItemWrapper
                      ? getSchemaAtPath(matchedBlockSchema, `item.${fieldKey}`)
                      : getSchemaAtPath(matchedBlockSchema, fieldKey);

                    return renderField(
                      fieldPath,
                      field,
                      blockFieldSchema,
                      blockData,
                    );
                  },
                )}
              </BlockCard>
            </div>
          );
        })}
      </div>

      <AddFieldDropdown
        label="Add block"
        options={addableBlocks}
        onAdd={(blockType) => {
          const blockDef = schemaDefinition.uiSchema.blocks?.[blockType];
          if (!blockDef) return;

          // Determine whether this block type uses an `item` wrapper.
          const blocksItemsSchema = getSchemaAtPath(
            dataSchema,
            blocksField,
          )?.items;
          const matchedBlockSchema = findBlockSchema(
            blocksItemsSchema,
            blockType,
          );
          const hasItemWrapper = Boolean(matchedBlockSchema?.properties?.item);

          // Build initial values for "default"-visibility fields and all
          // checkbox fields. Checkboxes must always be explicitly initialized
          // to false so the backend receives the correct value when the user
          // leaves them unchecked (absence of a boolean is treated as true
          // by the macro).
          const initialFields: Record<string, unknown> = {};
          Object.entries(blockDef.fields).forEach(([fieldKey, field]) => {
            if (
              field["ui:visibility"] === "default" ||
              field["ui:widget"] === "checkbox"
            ) {
              const jsonPath = hasItemWrapper ? `item.${fieldKey}` : fieldKey;
              const jsonFieldSchema = getSchemaAtPath(
                matchedBlockSchema,
                jsonPath,
              );
              initialFields[fieldKey] = getDefaultByWidget(
                field,
                jsonFieldSchema,
              );
            }
          });

          const newBlock = hasItemWrapper
            ? { type: blockType, item: initialFields }
            : { type: blockType, ...initialFields };

          setValueAt(blocksField, [...blocks, newBlock]);
          setPendingScrollId(`${formId.current}-block-${blocks.length}`);
        }}
      />
    </div>
  );
};

export default SchemaForm;
