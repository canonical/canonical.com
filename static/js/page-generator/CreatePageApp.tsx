import { useEffect, useState } from "react";
import {
  Button,
  Card,
  Col,
  Notification,
  Row,
} from "@canonical/react-components";

type SelectedPattern = {
  id: string;
  patternName: string;
};

type SchemaDefinition = {
  label: string;
  description: string;
  schema: {
    properties?: {
      data?: {
        required?: string[];
      };
    };
  };
  uiSchema: {
    fields?: Record<string, { [key: string]: unknown }>;
    blocks?: Record<string, { [key: string]: unknown }>;
  };
};

type SchemasResponse = Record<string, SchemaDefinition>;

declare global {
  interface Window {
    PAGE_GENERATOR_CONFIG?: {
      schemasUrl: string;
      previewUrl?: string;
    };
  }
}

const SINGLE_INSTANCE_PATTERNS = new Set(["hero"]);

const CreatePageApp = () => {
  const [schemas, setSchemas] = useState<SchemasResponse>({});
  const [selectedPatterns, setSelectedPatterns] = useState<SelectedPattern[]>(
    []
  );
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadSchemas = async () => {
      try {
        const response = await fetch(
          window.PAGE_GENERATOR_CONFIG?.schemasUrl || "/create-page/schemas"
        );

        if (!response.ok) {
          throw new Error(`Failed to load schemas (${response.status})`);
        }

        const data = (await response.json()) as SchemasResponse;
        setSchemas(data);
      } catch (loadError) {
        setError(
          loadError instanceof Error
            ? loadError.message
            : "Failed to load schemas"
        );
      } finally {
        setIsLoading(false);
      }
    };

    void loadSchemas();
  }, []);

  const countSelectedPatterns = (patternName: string) => {
    return selectedPatterns.filter(
      (pattern) => pattern.patternName === patternName
    ).length;
  };

  const canAddPattern = (patternName: string) => {
    if (!SINGLE_INSTANCE_PATTERNS.has(patternName)) {
      return true;
    }

    return countSelectedPatterns(patternName) === 0;
  };

  const addPattern = (patternName: string) => {
    if (!canAddPattern(patternName)) {
      return;
    }

    setSelectedPatterns((current) => [
      ...current,
      {
        id: `${patternName}-${current.length + 1}-${Date.now()}`,
        patternName,
      },
    ]);
  };

  const removePattern = (patternId: string) => {
    setSelectedPatterns((current) =>
      current.filter((pattern) => pattern.id !== patternId)
    );
  };

  const movePattern = (patternId: string, direction: "up" | "down") => {
    setSelectedPatterns((current) => {
      const currentIndex = current.findIndex(
        (pattern) => pattern.id === patternId
      );

      if (currentIndex === -1) {
        return current;
      }

      const targetIndex =
        direction === "up" ? currentIndex - 1 : currentIndex + 1;

      if (targetIndex < 0 || targetIndex >= current.length) {
        return current;
      }

      const next = [...current];
      const [movedItem] = next.splice(currentIndex, 1);
      next.splice(targetIndex, 0, movedItem);
      return next;
    });
  };

  return (
    <div>
      {error ? (
        <Notification severity="negative" title="Unable to load schemas">
          {error}
        </Notification>
      ) : null}

      <section>
        <h2 className="p-heading--4">Step 1: Choose patterns</h2>
        <p>
          This scaffold already uses the real backend schema registry. The next
          step is wiring these definitions into the dynamic form engine.
        </p>
        {isLoading ? <p>Loading pattern definitions…</p> : null}
        <Row>
          {Object.entries(schemas).map(([patternName, definition]) => {
            const requiredFields =
              definition.schema.properties?.data?.required || [];
            const selectionCount = countSelectedPatterns(patternName);
            const isSingleInstance = SINGLE_INSTANCE_PATTERNS.has(patternName);
            const isAddDisabled = !canAddPattern(patternName);

            return (
              <Col size={4} key={patternName}>
                <Card title={definition.label}>
                  <p>{definition.description}</p>
                  <p>
                    <strong>Selected:</strong> {selectionCount}
                    {isSingleInstance ? " (single instance only)" : ""}
                  </p>
                  <p>
                    <strong>Required fields:</strong>{" "}
                    {requiredFields.length > 0
                      ? requiredFields.join(", ")
                      : "No top-level required fields"}
                  </p>
                  <p>
                    <strong>Configured fields:</strong>{" "}
                    {Object.keys(definition.uiSchema.fields || {}).length}
                  </p>
                  <p>
                    <strong>Configured blocks:</strong>{" "}
                    {Object.keys(definition.uiSchema.blocks || {}).length}
                  </p>
                  <Button
                    appearance={selectionCount > 0 ? "positive" : "base"}
                    disabled={isAddDisabled}
                    onClick={() => addPattern(patternName)}
                    type="button"
                  >
                    {isSingleInstance ? "Add pattern" : "Add another"}
                  </Button>
                </Card>
              </Col>
            );
          })}
        </Row>
      </section>

      <section className="u-sv3">
        <h2 className="p-heading--4">Current selection</h2>
        {selectedPatterns.length ? (
          <ul className="p-list--divided">
            {selectedPatterns.map((pattern, index) => (
              <li key={pattern.id}>
                <div className="row u-no-padding--top u-no-padding--bottom">
                  <div className="col-6">
                    {index + 1}. {schemas[pattern.patternName]?.label || pattern.patternName}
                  </div>
                  <div className="col-6">
                    <Button
                      appearance="base"
                      disabled={index === 0}
                      onClick={() => movePattern(pattern.id, "up")}
                      type="button"
                    >
                      Move up
                    </Button>{" "}
                    <Button
                      appearance="base"
                      disabled={index === selectedPatterns.length - 1}
                      onClick={() => movePattern(pattern.id, "down")}
                      type="button"
                    >
                      Move down
                    </Button>{" "}
                    <Button
                      appearance="negative"
                      onClick={() => removePattern(pattern.id)}
                      type="button"
                    >
                      Remove
                    </Button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>No patterns selected yet.</p>
        )}
      </section>
    </div>
  );
};

export default CreatePageApp;