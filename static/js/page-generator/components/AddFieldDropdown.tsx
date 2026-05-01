import { Button, ContextualMenu } from "@canonical/react-components";

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
  if (options.length === 0) {
    return (
      <Button type="button" disabled>
        {label}
      </Button>
    );
  }

  return (
    <ContextualMenu
      toggleLabel={label}
      toggleClassName="p-button"
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
