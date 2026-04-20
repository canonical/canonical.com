import { useQuery } from "@tanstack/react-query";
import { fetchSchemas } from "../api/fetchSchemas";

export const useSchemas = () => {
  return useQuery({
    queryKey: ["page-generator", "schemas"],
    queryFn: fetchSchemas,
    staleTime: 5 * 60 * 1000,
  });
};
