export type UIWidget =
  | "text"
  | "textarea"
  | "select"
  | "radio-group"
  | "segmented-control"
  | "checkbox"
  | "link-editor"
  | "block-list"
  | "resource-card-list";

export type UICondition = Record<string, string | string[] | boolean>;

export interface UIFieldSchema {
  "ui:widget": UIWidget;
  "ui:label": string;
  "ui:placeholder"?: string;
  "ui:help"?: string;
  "ui:rows"?: number;
  "ui:required"?: boolean;
  "ui:visibility": "default" | "addable";
  "ui:multiplicity": "single" | "multiple";
  "ui:maxItems"?: number;
  "ui:subfields"?: Record<string, UIFieldSchema>;
  "ui:itemSchema"?: Record<string, UIFieldSchema>;
  "ui:conditions"?: {
    visibleWhen?: UICondition;
    requiredWhen?: UICondition;
  };
}

export interface UIBlockSchema {
  "ui:label": string;
  "ui:visibility": "default" | "addable";
  "ui:multiplicity": "single" | "multiple";
  "ui:maxItems"?: number;
  "ui:conditions"?: {
    visibleWhen?: UICondition;
    requiredWhen?: UICondition;
  };
  fields: Record<string, UIFieldSchema>;
}

export interface UISchema {
  "$pattern": string;
  "$blocksField"?: string;
  "ui:label": string;
  "ui:description"?: string;
  fields?: Record<string, UIFieldSchema>;
  blocks?: Record<string, UIBlockSchema>;
}

export interface JSONSchema {
  type?: string;
  enum?: (string | number | boolean)[];
  default?: unknown;
  required?: string[];
  properties?: Record<string, JSONSchema>;
  items?: JSONSchema;
  const?: unknown;
  $ref?: string;
  oneOf?: JSONSchema[];
  anyOf?: JSONSchema[];
  allOf?: JSONSchema[];
  definitions?: Record<string, JSONSchema>;
}

export interface SchemaDefinition {
  schema: JSONSchema;
  uiSchema: UISchema;
  label: string;
  description: string;
}

export type SchemasResponse = Record<string, SchemaDefinition>;

export interface SectionState {
  id: string;
  patternName: string;
  data: Record<string, unknown>;
}

export interface PreviewResponse {
  preview_url: string;
  page_path: string;
  html: string;
}

export interface SaveResponse {
  url: string;
  page_path: string;
}

export interface PageGeneratorConfig {
  schemasUrl: string;
  previewUrl: string;
  saveUrl: string;
}

declare global {
  interface Window {
    __PAGE_GENERATOR__?: Partial<PageGeneratorConfig>;
    PAGE_GENERATOR_CONFIG?: Partial<PageGeneratorConfig>;
  }
}
