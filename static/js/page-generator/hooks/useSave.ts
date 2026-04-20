import { useMutation } from "@tanstack/react-query";
import { savePage } from "../api/savePage";

export const useSave = () => {
  return useMutation({
    mutationFn: savePage,
  });
};
