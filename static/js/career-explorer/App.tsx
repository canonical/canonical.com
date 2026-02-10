import ReactDOM from "react-dom/client";
import Explorer from "./Explorer";

const domContainer = document.querySelector("#root");
const root = ReactDOM.createRoot(domContainer!);
root.render(<Explorer />);
