import { endpoints } from "./endpoints";
import { SchemasResponse } from "../types";

export const fetchSchemas = async (): Promise<SchemasResponse> => {
  const response = await fetch(endpoints.schemasUrl);

  if (!response.ok) {
    throw new Error(`Failed to load schemas (${response.status})`);
  }

  return (await response.json()) as SchemasResponse;
};
