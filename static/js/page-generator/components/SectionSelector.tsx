import {
  Badge,
  Button,
  Card,
  Col,
  Icon,
  Row,
} from "@canonical/react-components";
import { SchemaDefinition, SectionState } from "../types";

interface Props {
  schemas: Record<string, SchemaDefinition>;
  sections: SectionState[];
  onAddSection: (patternName: string) => void;
  onMoveSection: (id: string, direction: "up" | "down") => void;
  onRemoveSection: (id: string) => void;
  onNext: () => void;
}

const SINGLE_INSTANCE_PATTERNS = new Set(["hero"]);

const SectionSelector = ({
  schemas,
  sections,
  onAddSection,
  onMoveSection,
  onRemoveSection,
  onNext,
}: Props) => {
  const countSelected = (patternName: string) =>
    sections.filter((item) => item.patternName === patternName).length;

  return (
    <>
      <Row>
        {/* Left column: available pattern cards */}
        <Col size={6}>
          <h3 className="p-heading--5">Available sections</h3>
          <Row>
            {Object.entries(schemas).map(([patternName, definition]) => {
              const count = countSelected(patternName);
              const isSingle = SINGLE_INSTANCE_PATTERNS.has(patternName);
              const disabled = isSingle && count > 0;

              return (
                <Col size={6} key={patternName}>
                  <Card>
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        marginBottom: "0.5rem",
                      }}
                    >
                      <h4 className="p-heading--5 u-no-margin--bottom">
                        {definition.label}
                      </h4>
                      {count > 0 ? (
                        <Badge value={count} />
                      ) : null}
                    </div>
                    <p className="u-text--muted">{definition.description}</p>
                    <Button
                      type="button"
                      appearance="base"
                      disabled={disabled}
                      onClick={() => onAddSection(patternName)}
                      dense
                    >
                      {disabled ? "Added" : isSingle ? "Add section" : "Add"}
                    </Button>
                  </Card>
                </Col>
              );
            })}
          </Row>
        </Col>

        {/* Right column: selected sections ordered list */}
        <Col size={6}>
          <h3 className="p-heading--5">Selected sections</h3>
          {sections.length === 0 ? (
            <p className="u-text--muted">
              No sections selected yet. Add sections from the left.
            </p>
          ) : (
            <ul className="p-list--divided u-no-margin--bottom">
              {sections.map((section, index) => (
                <li key={section.id} className="p-list__item">
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                    }}
                  >
                    <span>
                      {index + 1}.{" "}
                      {schemas[section.patternName]?.label ||
                        section.patternName}
                    </span>
                    <span style={{ display: "flex", gap: "0.25rem" }}>
                      <Button
                        type="button"
                        appearance="base"
                        hasIcon
                        dense
                        disabled={index === 0}
                        onClick={() => onMoveSection(section.id, "up")}
                        aria-label="Move up"
                        style={{ margin: 0 }}
                      >
                        <Icon name="chevron-up" />
                      </Button>
                      <Button
                        type="button"
                        appearance="base"
                        hasIcon
                        dense
                        disabled={index === sections.length - 1}
                        onClick={() => onMoveSection(section.id, "down")}
                        aria-label="Move down"
                        style={{ margin: 0 }}
                      >
                        <Icon name="chevron-down" />
                      </Button>
                      <Button
                        type="button"
                        appearance="base"
                        hasIcon
                        dense
                        onClick={() => onRemoveSection(section.id)}
                        aria-label="Remove section"
                        style={{ margin: 0 }}
                      >
                        <Icon name="close" />
                      </Button>
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </Col>
      </Row>

      <Row>
        <Col size={12}>
          <div className="u-sv2">
            <Button
              type="button"
              appearance="positive"
              disabled={sections.length === 0}
              onClick={onNext}
            >
              Next: Add content
            </Button>
          </div>
        </Col>
      </Row>
    </>
  );
};

export default SectionSelector;
