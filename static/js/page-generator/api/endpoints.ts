import { PageGeneratorConfig } from "../types";

const FALLBACK_ENDPOINTS: PageGeneratorConfig = {
  schemasUrl: "/create-page/schemas",
  previewUrl: "/create-page/preview",
  saveUrl: "/create-page/save",
};

const config = {
  ...FALLBACK_ENDPOINTS,
  ...(window.__PAGE_GENERATOR__ || {}),
  ...(window.PAGE_GENERATOR_CONFIG || {}),
};

export const endpoints: PageGeneratorConfig = {
  schemasUrl: config.schemasUrl,
  previewUrl: config.previewUrl,
  saveUrl: config.saveUrl,
};
