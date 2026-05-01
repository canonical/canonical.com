import { endpoints } from "./endpoints";
import { PreviewResponse, SectionState } from "../types";

interface PreviewPayload {
  sections: Array<Pick<SectionState, "patternName" | "data">>;
  page_name?: string;
  page_path?: string;
}

export const previewPage = async (
  payload: PreviewPayload
): Promise<PreviewResponse> => {
  const response = await fetch(endpoints.previewUrl, {
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

  const body = (await response.json()) as PreviewResponse & {
    errors?: Array<{ message: string }>;
  };

  if (!response.ok) {
    throw new Error(body.errors?.[0]?.message || "Failed to preview page");
  }

  return body;
};
