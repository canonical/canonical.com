import { Button, Icon } from "@canonical/react-components";
import { ReactNode } from "react";

interface Props {
  title: string;
  children: ReactNode;
  onRemove?: () => void;
}

const BlockCard = ({ title, children, onRemove }: Props) => {
  return (
    <div className="p-card u-no-margin--bottom">
      <div className="p-card__inner">
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            paddingBottom: "0.5rem",
          }}
        >
          <h5 className="p-heading--5 u-no-margin--bottom">{title}</h5>
          {onRemove ? (
            <Button
              type="button"
              appearance="base"
              hasIcon
              dense
              onClick={onRemove}
              aria-label={`Remove ${title}`}
              style={{ margin: 0 }}
            >
              <Icon name="delete" />
            </Button>
          ) : null}
        </div>
        <hr className="u-no-margin--top" />
        {children}
      </div>
    </div>
  );
};

export default BlockCard;
