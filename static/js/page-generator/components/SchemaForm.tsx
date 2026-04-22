import {
  Button,
  CheckboxInput,
  Input,
  Notification,
  Select,
  Textarea,
} from "@canonical/react-components";
import { ReactNode, useEffect, useMemo, useState } from "react";
import AddFieldDropdown from "./AddFieldDropdown";
import BlockCard from "./widgets/BlockCard";
import LinkEditor from "./widgets/LinkEditor";
import RadioGroupWidget from "./widgets/RadioGroupWidget";
import ResourceCardEditor from "./widgets/ResourceCardEditor";
import { buildInitialValues, getNestedValue, setNestedValue } from "../utils/buildInitialValues";
import { isRequired, isVisible } from "../utils/resolveConditions";
import { resolveRefs, findBlockSchema } from "../utils/resolveRefs";
import { JSONSchema, SchemaDefinition, UIFieldSchema } from "../types";

interface Props {
  schemaDefinition: SchemaDefinition;
  value: Record<string, unknown>;
  onChange: (value: Record<string, unknown>) => void;
}

const hasValue = (value: unknown): boolean => {
  if (value === undefined || value === null) {
    return false;
  }

  if (typeof value === "string") {
    return value.trim().length > 0;
  }

  if (Array.isArray(value)) {
    return value.length > 0;
  }

  if (typeof value === "object") {
    return Object.keys(value as Record<string, unknown>).length > 0;
  }

  return true;
};

const getSchemaAtPath = (
  rootSchema: JSONSchema | undefined,
  path: string
): JSONSchema | undefined => {
  if (!rootSchema) {
    return undefined;
  }

  return path.split(".").reduce<JSONSchema | undefined>((current, segment) => {
    if (!current) {
      return undefined;
    }

    if (current.properties && current.properties[segment]) {
      return current.properties[segment];
    }

    return undefined;
  }, rootSchema);
};

const getDefaultByWidget = (field: UIFieldSchema): unknown => {
  if (field["ui:widget"] === "checkbox") {
    return false;
  }

  if (field["ui:widget"] === "link-editor") {
    if (field["ui:multiplicity"] === "multiple") {
      return [];
    }

    return { content_html: "", attrs: { href: "" } };
  }

  if (field["ui:multiplicity"] === "multiple") {
    return [];
  }

  return "";
};

const SchemaForm = ({ schemaDefinition, value: _value, onChange }: Props) => {
  // Resolve all $ref pointers once so downstream lookups work without indirection.
  const resolvedSchema = useMemo(
    () => resolveRefs(schemaDefinition.schema),
    [schemaDefinition.schema]
  );
  const dataSchema = resolvedSchema.properties?.data;

  const initialValues = useMemo(() => {
    if (!dataSchema) return {};
    return buildInitialValues(dataSchema);
  }, [dataSchema]);

  const [values, setValues] = useState<Record<string, unknown>>(initialValues);
  const [activatedFields, setActivatedFields] = useState<Set<string>>(new Set());

  // Report changes to parent whenever internal state updates.
  useEffect(() => {
    onChange(values);
  }, [values]);

  if (!dataSchema) {
    return (
      <Notification severity="negative" title="Invalid schema shape">
        Missing data schema for this section.
      </Notification>
    );
  }

  const getValueAt = (path: string): unknown => getNestedValue(values, path);

  const setValueAt = (path: string, val: unknown) => {
    setValues((prev) => setNestedValue(prev, path, val));
  };

  const topFields = Object.entries(schemaDefinition.uiSchema.fields || {});
  // The data-model property holding the repeatable blocks array.
  // Defaults to "blocks" but can be overridden per-pattern (e.g. basic-section uses "items").
  const blocksField = schemaDefinition.uiSchema["$blocksField"] || "blocks";
  const blocks = Array.isArray(values[blocksField])
    ? (values[blocksField] as Array<{ type?: string; item?: Record<string, unknown> }>)
    : [];

  const topLevelAddable = topFields
    .filter(([, field]) => field["ui:visibility"] === "addable")
    .filter(([fieldKey]) => !hasValue(getValueAt(fieldKey)))
    .map(([fieldKey, field]) => ({ value: fieldKey, label: field["ui:label"] }));

  const renderField = (
    name: string,
    field: UIFieldSchema,
    fieldSchema?: JSONSchema
  ): ReactNode => {
    if (!isVisible(field, values)) return null;

    const required = isRequired(field, values);
    const currentValue = getValueAt(name);

    if (field["ui:widget"] === "radio-group") {
      const options = (fieldSchema?.enum || []).map((option) => ({
        label: option,
        value: option,
      }));
      return (
        <RadioGroupWidget
          key={name}
          label={field["ui:label"]}
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
      return (
        <Select
          key={name}
          id={name}
          label={field["ui:label"]}
          required={required}
          value={String(currentValue ?? "")}
          onChange={(e) => setValueAt(name, e.target.value)}
          options={[
            { label: `Choose ${field["ui:label"].toLowerCase()}`, value: "", disabled: true },
            ...(fieldSchema?.enum || []).map((enumValue) => ({
              label: enumValue,
              value: enumValue,
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
          onChange={(e) => setValueAt(name, (e.target as HTMLInputElement).checked)}
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
                  value={item as { content_html: string; attrs: { href: string } }}
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
              onClick={() => setValueAt(name, [...items, { content_html: "", attrs: { href: "" } }])}
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
          value={currentValue as { content_html: string; attrs: { href: string } } | undefined}
          onChange={(val) => setValueAt(name, val)}
        />
      );
    }

    if (field["ui:widget"] === "resource-card-list") {
      return <ResourceCardEditor key={name} label={field["ui:label"]} />;
    }

    // Default: text input
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

  const blockDefinitions = Object.entries(schemaDefinition.uiSchema.blocks || {});

  const addableBlocks = blockDefinitions
    .filter(([, block]) => block["ui:visibility"] === "addable")
    .filter(([blockType, block]) => {
      const count = blocks.filter((item) => item.type === blockType).length;
      if (block["ui:multiplicity"] === "single" && count > 0) return false;
      if (block["ui:maxItems"] && count >= block["ui:maxItems"]) return false;
      return true;
    })
    .map(([blockType, block]) => ({ value: blockType, label: block["ui:label"] }));

  return (
    <div>
      {topFields.map(([fieldKey, field]) => {
        const visibility = field["ui:visibility"];
        if (visibility === "addable" && !activatedFields.has(fieldKey) && !hasValue(getValueAt(fieldKey))) return null;

        const fieldSchema = getSchemaAtPath(dataSchema, fieldKey);
        const subfields = field["ui:subfields"];

        if (subfields) {
          return (
            <div key={fieldKey} className="u-sv2">
              <h4 className="p-heading--5">{field["ui:label"]}</h4>
              {Object.entries(subfields).map(([subKey, subField]) =>
                renderField(
                  `${fieldKey}.${subKey}`,
                  subField,
                  getSchemaAtPath(fieldSchema, subKey)
                )
              )}
            </div>
          );
        }

        return renderField(fieldKey, field, fieldSchema);
      })}

      <div className="u-sv2">
        <AddFieldDropdown
          label="Add field"
          options={topLevelAddable}
          onAdd={(fieldName) => {
            const fieldDef = schemaDefinition.uiSchema.fields?.[fieldName];
            if (!fieldDef) return;
            setActivatedFields((prev) => new Set(prev).add(fieldName));
            setValueAt(fieldName, getDefaultByWidget(fieldDef));
          }}
        />
      </div>

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
                This block type is not yet mapped in the UI schema renderer.
              </Notification>
            );
          }

          return (
            <BlockCard
              key={`${block.type}-${blockIndex}`}
              title={blockSchemaDef["ui:label"]}
              onRemove={() => {
                const next = [...blocks];
                next.splice(blockIndex, 1);
                setValueAt(blocksField, next);
              }}
            >
              {Object.entries(blockSchemaDef.fields || {}).map(([fieldKey, field]) => {
                // Resolve the correct oneOf branch for this block type,
                // then navigate into item.<fieldKey> to get the field-level schema.
                const blocksItemsSchema = getSchemaAtPath(dataSchema, blocksField)?.items;
                const matchedBlockSchema = findBlockSchema(blocksItemsSchema, blockType);
                const blockFieldSchema = getSchemaAtPath(matchedBlockSchema, `item.${fieldKey}`);
                return renderField(
                  `${blocksField}.${blockIndex}.item.${fieldKey}`,
                  field,
                  blockFieldSchema
                );
              })}
            </BlockCard>
          );
        })}
      </div>

      <AddFieldDropdown
        label="Add block"
        options={addableBlocks}
        onAdd={(blockType) => {
          const blockDef = schemaDefinition.uiSchema.blocks?.[blockType];
          if (!blockDef) return;

          const initialItem: Record<string, unknown> = {};
          Object.entries(blockDef.fields).forEach(([fieldKey, field]) => {
            if (field["ui:visibility"] === "default") {
              initialItem[fieldKey] = getDefaultByWidget(field);
            }
          });

          setValueAt(blocksField, [...blocks, { type: blockType, item: initialItem }]);
        }}
      />
    </div>
  );
};

export default SchemaForm;
