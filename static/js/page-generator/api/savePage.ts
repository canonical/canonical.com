import { endpoints } from "./endpoints";
import { SaveResponse, SectionState } from "../types";

interface SavePayload {
  sections: Array<Pick<SectionState, "patternName" | "data">>;
  page_name?: string;
  page_path?: string;
}

export const savePage = async (payload: SavePayload): Promise<SaveResponse> => {
  const response = await fetch(endpoints.saveUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      page_name: payload.page_name,
      page_path: payload.page_path,
      sections: payload.sections.map((section) => ({
        name: section.patternName,
        data: section.data,
      })),
    }),
  });

  const body = (await response.json()) as SaveResponse & {
    errors?: Array<{ message: string }>;
  };

  if (!response.ok) {
    throw new Error(body.errors?.[0]?.message || "Failed to save page");
  }

  return body;
};
