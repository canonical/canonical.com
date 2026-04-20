import { ContextualMenu } from "@canonical/react-components";

interface AddOption {
  label: string;
  value: string;
}

interface Props {
  label: string;
  options: AddOption[];
  onAdd: (value: string) => void;
}

const AddFieldDropdown = ({ label, options, onAdd }: Props) => {
  return (
    <ContextualMenu
      toggleLabel={label}
      toggleAppearance="base"
      toggleDisabled={options.length === 0}
      links={options.map((option) => ({
        children: option.label,
        onClick: () => {
          onAdd(option.value);
        },
      }))}
    />
  );
};

export default AddFieldDropdown;
