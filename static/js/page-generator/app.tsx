import { createRoot } from "react-dom/client";
import CreatePageApp from "./CreatePageApp";

const rootElement = document.getElementById("page-generator-root");

if (rootElement) {
  createRoot(rootElement).render(<CreatePageApp />);
}