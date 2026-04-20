interface Props {
  html: string;
}

const PreviewPane = ({ html }: Props) => {
  if (!html) {
    return <p>Generate a preview to inspect the rendered page.</p>;
  }

  return (
    <iframe
      title="Page preview"
      srcDoc={html}
      style={{ width: "100%", minHeight: "700px", border: "1px solid #d9d9d9" }}
    />
  );
};

export default PreviewPane;
