import { Input, Col, Row } from "@canonical/react-components";

interface LinkValue {
  content_html: string;
  attrs: { href: string };
}

interface Props {
  label: string;
  required?: boolean;
  value?: LinkValue;
  onChange: (value: LinkValue) => void;
}

const LinkEditor = ({ label, required, value, onChange }: Props) => {
  const safeValue: LinkValue = value ?? { content_html: "", attrs: { href: "" } };

  return (
    <div className="u-sv2">
      <p className={`p-form__label${required ? " is-required" : ""}`}>{label}</p>
      <Row>
        <Col size={6}>
          <Input
            type="text"
            label="Label"
            required={required}
            value={safeValue.content_html}
            onChange={(e) =>
              onChange({ ...safeValue, content_html: e.target.value })
            }
          />
        </Col>
        <Col size={6}>
          <Input
            type="text"
            label="URL"
            value={safeValue.attrs.href}
            onChange={(e) =>
              onChange({ ...safeValue, attrs: { href: e.target.value } })
            }
          />
        </Col>
      </Row>
    </div>
  );
};

export default LinkEditor;
