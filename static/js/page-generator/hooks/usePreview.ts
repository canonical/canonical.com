import { useMutation } from "@tanstack/react-query";
import { previewPage } from "../api/previewPage";

export const usePreview = () => {
  return useMutation({
    mutationFn: previewPage,
  });
};
