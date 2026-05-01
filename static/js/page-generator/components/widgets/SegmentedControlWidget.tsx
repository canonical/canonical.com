interface Option {
  label: string;
  value: string;
}

interface Props {
  label: string;
  options: Option[];
  required?: boolean;
  value: string;
  onChange: (value: string) => void;
}

const capitalize = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);

const SegmentedControlWidget = ({
  label,
  options,
  required,
  value,
  onChange,
}: Props) => {
  return (
    <div className="p-form__group">
      <span className={`p-form__label${required ? " is-required" : ""}`}>
        {label}
      </span>
      <div className="p-segmented-control" style={{ marginLeft: 0 }}>
        <ul
          className="p-segmented-control__list"
          style={{ marginLeft: 0, paddingLeft: 0 }}
        >
          {options.map((option) => (
            <li
              key={option.value}
              className="p-segmented-control__item"
              style={{ listStyleType: "none" }}
            >
              <button
                type="button"
                className={`p-segmented-control__button${
                  value === option.value ? " is-active" : ""
                }`}
                aria-pressed={value === option.value}
                onClick={() => onChange(option.value)}
              >
                {capitalize(option.label)}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default SegmentedControlWidget;
