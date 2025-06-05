import { defineConfig, Schema } from "@julr/vite-plugin-validate-env";

export default defineConfig({
  VITE_AUTH_API_URL: Schema.string(),
  VITE_VISITS_API_URL: Schema.string(),
  VITE_PAYMENTS_API_URL: Schema.string(),
  VITE_AUTH_CLIENT_ID: Schema.string(),
  VITE_STRIPE_KEY: Schema.string(),
});
