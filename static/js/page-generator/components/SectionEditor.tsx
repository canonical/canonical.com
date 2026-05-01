import { Button, Input, Notification } from "@canonical/react-components";
import { useEffect } from "react";
import PreviewPane from "./PreviewPane";
import SchemaForm from "./SchemaForm";
import SegmentedControlWidget from "./widgets/SegmentedControlWidget";
import { SchemaDefinition, SectionState } from "../types";

interface Props {
  schemas: Record<string, SchemaDefinition>;
  sections: SectionState[];
  onUpdateSection: (id: string, data: Record<string, unknown>) => void;
  onBack: () => void;
  onPreview: () => void;
  onSave: () => void;
  isPreviewing: boolean;
  isSaving: boolean;
  previewHtml: string;
  error: string | null;
  savedUrl: string | null;
  viewMode: "edit" | "preview";
  onViewModeChange: (mode: "edit" | "preview") => void;
  pageName: string;
  onPageNameChange: (name: string) => void;
  isPreviewStale: boolean;
  allRequiredFilled: boolean;
}

const SectionEditor = ({
  schemas,
  sections,
  onUpdateSection,
  onBack,
  onPreview,
  onSave,
  isPreviewing,
  isSaving,
  previewHtml,
  error,
  savedUrl,
  viewMode,
  onViewModeChange,
  pageName,
  onPageNameChange,
  isPreviewStale,
  allRequiredFilled,
}: Props) => {
  useEffect(() => {
    if (error || savedUrl) {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }, [error, savedUrl]);

  return (
    <>
      {error ? (
        <Notification severity="negative" title="Page generator error">
          {error}
        </Notification>
      ) : null}

      {savedUrl ? (
        <Notification severity="positive" title="Page saved">
          Saved successfully: <a href={savedUrl}>{savedUrl}</a>
        </Notification>
      ) : null}

      <SegmentedControlWidget
        label=""
        options={[
          { label: "Edit", value: "edit" },
          { label: "Preview", value: "preview" },
        ]}
        value={viewMode}
        onChange={(val) => onViewModeChange(val as "edit" | "preview")}
      />

      {viewMode === "preview" ? (
        <>
          {isPreviewStale && previewHtml ? (
            <Notification severity="caution" title="Preview may be outdated">
              Content has changed since the last preview. Generate a new preview
              to see the latest changes.
            </Notification>
          ) : null}
          <PreviewPane html={previewHtml} />
        </>
      ) : null}

      <div style={{ display: viewMode !== "edit" ? "none" : undefined }}>
        {sections.map((section, index) => {
          const schemaDefinition = schemas[section.patternName];
          const label = schemaDefinition?.label || section.patternName;

          return (
            <div key={section.id}>
              {index > 0 ? <hr /> : null}
              <div className="grid-row">
                <div className="grid-col-2">
                  <p
                    className="p-text--small-caps"
                    style={{ paddingTop: "0.5rem" }}
                  >
                    {label}
                  </p>
                </div>
                <div className="grid-col-6">
                  {schemaDefinition ? (
                    <SchemaForm
                      schemaDefinition={schemaDefinition}
                      value={section.data}
                      onChange={(nextData) => {
                        onUpdateSection(section.id, nextData);
                      }}
                    />
                  ) : (
                    <Notification severity="negative" title="Missing schema">
                      Could not load schema for {section.patternName}.
                    </Notification>
                  )}
                </div>
              </div>
            </div>
          );
        })}

        <hr />

        <div className="grid-row">
          <div className="grid-col-2" />
          <div className="grid-col-6">
            <div className="u-sv2">
              <Input
                type="text"
                label="Page path"
                placeholder="e.g. academy/my-new-page"
                help="Path relative to templates/, e.g. academy/my-new-page"
                required
                value={pageName}
                onChange={(e) => onPageNameChange(e.target.value)}
              />
            </div>
            <div className="u-sv1">
              <Button
                type="button"
                appearance="positive"
                onClick={onPreview}
                disabled={
                  isPreviewing || sections.length === 0 || !allRequiredFilled
                }
              >
                {isPreviewing ? "Generating preview…" : "Generate preview"}
              </Button>{" "}
              <Button
                type="button"
                appearance="brand"
                onClick={onSave}
                disabled={isSaving || sections.length === 0}
              >
                {isSaving ? "Saving…" : "Save page"}
              </Button>{" "}
              <Button type="button" appearance="base" onClick={onBack}>
                Back
              </Button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default SectionEditor;
