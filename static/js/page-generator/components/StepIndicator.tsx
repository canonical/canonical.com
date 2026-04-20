interface Props {
  activeStep: 1 | 2;
  onStepChange: (step: 1 | 2) => void;
  canAccessStepTwo: boolean;
}

const StepIndicator = ({ activeStep, onStepChange, canAccessStepTwo }: Props) => {
  const step1Complete = activeStep === 2;

  return (
    <nav aria-label="Page creation steps">
      <ul className="p-tabs__list" role="tablist">
        <li className="p-tabs__item" role="presentation">
          <button
            type="button"
            role="tab"
            className={`p-tabs__link${activeStep === 1 ? " is-active" : ""}`}
            aria-selected={activeStep === 1}
            onClick={() => onStepChange(1)}
            style={{ display: "inline-flex", alignItems: "center", gap: "0.5rem" }}
          >
            {step1Complete ? (
              <i className="p-icon--success" aria-hidden="true" />
            ) : (
              <span
                aria-hidden="true"
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  justifyContent: "center",
                  width: "1rem",
                  height: "1rem",
                  borderRadius: "50%",
                  border: "1.5px solid currentColor",
                  fontSize: "0.75rem",
                  lineHeight: 1,
                  flexShrink: 0,
                }}
              >
                1
              </span>
            )}
            Choose your sections
          </button>
        </li>
        <li className="p-tabs__item" role="presentation">
          <button
            type="button"
            role="tab"
            className={`p-tabs__link${activeStep === 2 ? " is-active" : ""}${!canAccessStepTwo ? " is-disabled" : ""}`}
            aria-selected={activeStep === 2}
            aria-disabled={!canAccessStepTwo}
            onClick={() => {
              if (canAccessStepTwo) {
                onStepChange(2);
              }
            }}
            style={{ display: "inline-flex", alignItems: "center", gap: "0.5rem" }}
          >
            <span
              aria-hidden="true"
              style={{
                display: "inline-flex",
                alignItems: "center",
                justifyContent: "center",
                width: "1rem",
                height: "1rem",
                borderRadius: "50%",
                border: "1.5px solid currentColor",
                fontSize: "0.75rem",
                lineHeight: 1,
                flexShrink: 0,
              }}
            >
              2
            </span>
            Add your content
          </button>
        </li>
      </ul>
    </nav>
  );
};

export default StepIndicator;
