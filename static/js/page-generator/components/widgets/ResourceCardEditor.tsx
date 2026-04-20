import { Notification } from "@canonical/react-components";

interface Props {
  label: string;
}

const ResourceCardEditor = ({ label }: Props) => {
  return (
    <Notification severity="information" title={label}>
      Detailed resource card editing is scaffolded and will be expanded in the next Phase 3 slice.
    </Notification>
  );
};

export default ResourceCardEditor;
