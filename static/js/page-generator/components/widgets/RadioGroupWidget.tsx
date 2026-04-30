import { RadioInput } from "@canonical/react-components";

interface Option {
  label: string;
  value: string;
}

interface Props {
  label: string;
  name: string;
  options: Option[];
  required?: boolean;
  value: string;
  onChange: (value: string) => void;
}

const RadioGroupWidget = ({ label, name, options, required, value, onChange }: Props) => {
  return (
    <fieldset className="p-form__group">
      <legend className={`p-form__label${required ? " is-required" : ""}`}>
        {label}
      </legend>
      <div className="u-sv1">
        {options.map((option) => (
          <RadioInput
            key={option.value}
            label={option.label}
            name={name}
            checked={value === option.value}
            onChange={() => onChange(option.value)}
          />
        ))}
      </div>
    </fieldset>
  );
};

export default RadioGroupWidget;
