import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import CreatePageApp from "./CreatePageApp";

const rootElement = document.getElementById("page-generator-root");
const queryClient = new QueryClient();

if (rootElement) {
  createRoot(rootElement).render(
    <QueryClientProvider client={queryClient}>
      <CreatePageApp />
    </QueryClientProvider>
  );
}