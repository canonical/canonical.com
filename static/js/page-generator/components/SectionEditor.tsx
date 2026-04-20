import { Button, Col, Notification, Row } from "@canonical/react-components";
import PreviewPane from "./PreviewPane";
import SchemaForm from "./SchemaForm";
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
}: Props) => {
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

      <div className="grid-row">

        <div className="p-segmented-control">
          <ul className="p-segmented-control__list">
            <li className="p-segmented-control__item">
              <button
                type="button"
                className={`p-segmented-control__button ${viewMode === "edit" ? "is-active" : ""
                  }`}
                onClick={() => onViewModeChange("edit")}
              >
                Edit
              </button>
            </li>
            <li className="p-segmented-control__item">
              <button
                type="button"
                className={`p-segmented-control__button ${viewMode === "preview" ? "is-active" : ""
                  }`}
                onClick={() => onViewModeChange("preview")}
              >
                Preview
              </button>
            </li>
          </ul>
        </div>
      </div>

      {viewMode === "preview" ? (
        <PreviewPane html={previewHtml} />
      ) : (
        <>
          {sections.map((section, index) => {
            const schemaDefinition = schemas[section.patternName];
            const label =
              schemaDefinition?.label || section.patternName;

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
                      <Notification
                        severity="negative"
                        title="Missing schema"
                      >
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
              <div className="u-sv1">
                <Button
                  type="button"
                  appearance="positive"
                  onClick={onPreview}
                  disabled={isPreviewing || sections.length === 0}
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
        </>
      )}
    </>
  );
};

export default SectionEditor;
