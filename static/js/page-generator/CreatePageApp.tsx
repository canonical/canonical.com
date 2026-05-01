import { Notification, Spinner } from "@canonical/react-components";
import { useCallback, useMemo, useState } from "react";
import SectionEditor from "./components/SectionEditor";
import SectionSelector from "./components/SectionSelector";
import StepIndicator from "./components/StepIndicator";
import { usePreview } from "./hooks/usePreview";
import { useSave } from "./hooks/useSave";
import { useSchemas } from "./hooks/useSchemas";
import { SectionState } from "./types";
import { areSectionRequiredFieldsFilled } from "./utils/resolveConditions";

function splitPagePath(input: string) {
  const trimmed = input.replace(/^\/+|\/+$/g, "");
  const lastSlash = trimmed.lastIndexOf("/");
  if (lastSlash === -1) {
    return { name: trimmed, path: "/" };
  }
  return {
    name: trimmed.substring(lastSlash + 1),
    path: "/" + trimmed.substring(0, lastSlash),
  };
}

const CreatePageApp = () => {
  const { data: schemas = {}, isLoading, error } = useSchemas();
  const previewMutation = usePreview();
  const saveMutation = useSave();

  const [activeStep, setActiveStep] = useState<1 | 2>(1);
  const [viewMode, setViewMode] = useState<"edit" | "preview">("edit");
  const [sections, setSections] = useState<SectionState[]>([]);
  const [previewHtml, setPreviewHtml] = useState("");
  const [apiError, setApiError] = useState<string | null>(null);
  const [savedUrl, setSavedUrl] = useState<string | null>(null);
  const [pageName, setPageName] = useState("generated-page");
  const [isPreviewStale, setIsPreviewStale] = useState(false);

  const addSection = (patternName: string) => {
    setSections((current) => [
      ...current,
      {
        id: `${patternName}-${Date.now()}-${Math.round(Math.random() * 9999)}`,
        patternName,
        data: {},
      },
    ]);
    setIsPreviewStale(true);
  };

  const removeSection = (id: string) => {
    setSections((current) => current.filter((section) => section.id !== id));
    setIsPreviewStale(true);
  };

  const moveSection = (id: string, direction: "up" | "down") => {
    setSections((current) => {
      const currentIndex = current.findIndex((section) => section.id === id);

      if (currentIndex === -1) {
        return current;
      }

      const targetIndex =
        direction === "up" ? currentIndex - 1 : currentIndex + 1;

      if (targetIndex < 0 || targetIndex >= current.length) {
        return current;
      }

      const next = [...current];
      const [movedSection] = next.splice(currentIndex, 1);
      next.splice(targetIndex, 0, movedSection);
      return next;
    });
    setIsPreviewStale(true);
  };

  const updateSection = (id: string, data: Record<string, unknown>) => {
    setSections((current) =>
      current.map((section) => {
        if (section.id !== id) {
          return section;
        }

        return { ...section, data };
      }),
    );
    setIsPreviewStale(true);
  };

  const previewPage = useCallback(async () => {
    setApiError(null);

    try {
      const { name } = splitPagePath(pageName);
      const response = await previewMutation.mutateAsync({
        page_name: name,
        page_path: "/page-generator/preview",
        sections,
      });
      setPreviewHtml(response.html);
      setViewMode("preview");
      setIsPreviewStale(false);
    } catch (previewError) {
      setApiError(
        previewError instanceof Error
          ? previewError.message
          : "Failed to preview page",
      );
    }
  }, [previewMutation, sections, pageName]);

  const savePage = useCallback(async () => {
    setApiError(null);
    setSavedUrl(null);

    try {
      const { name, path } = splitPagePath(pageName);
      const response = await saveMutation.mutateAsync({
        page_name: name,
        page_path: path,
        sections,
      });
      setSavedUrl(response.url);
    } catch (saveError) {
      setApiError(
        saveError instanceof Error ? saveError.message : "Failed to save page",
      );
    }
  }, [saveMutation, sections, pageName]);

  const allRequiredFilled = useMemo(
    () =>
      sections.length > 0 &&
      sections.every((section) => {
        const def = schemas[section.patternName];
        return def ? areSectionRequiredFieldsFilled(def, section.data) : true;
      }),
    [sections, schemas],
  );

  return (
    <div>
      <h1 className="p-heading--2">Create page</h1>

      <StepIndicator
        activeStep={activeStep}
        onStepChange={setActiveStep}
        canAccessStepTwo={sections.length > 0}
      />

      {error ? (
        <Notification severity="negative" title="Unable to load schemas">
          {error instanceof Error ? error.message : "Failed to load schemas"}
        </Notification>
      ) : null}

      {isLoading ? <Spinner text="Loading schemas…" /> : null}

      {!isLoading && activeStep === 1 ? (
        <SectionSelector
          schemas={schemas}
          sections={sections}
          onAddSection={addSection}
          onMoveSection={moveSection}
          onRemoveSection={removeSection}
          onNext={() => setActiveStep(2)}
        />
      ) : null}

      {!isLoading && activeStep === 2 ? (
        <SectionEditor
          schemas={schemas}
          sections={sections}
          onUpdateSection={updateSection}
          onBack={() => setActiveStep(1)}
          onPreview={previewPage}
          onSave={savePage}
          isPreviewing={previewMutation.isPending}
          isSaving={saveMutation.isPending}
          previewHtml={previewHtml}
          error={apiError}
          savedUrl={savedUrl}
          viewMode={viewMode}
          onViewModeChange={setViewMode}
          pageName={pageName}
          onPageNameChange={setPageName}
          isPreviewStale={isPreviewStale}
          allRequiredFilled={allRequiredFilled}
        />
      ) : null}
    </div>
  );
};

export default CreatePageApp;
