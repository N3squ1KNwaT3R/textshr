import type { Config } from "tailwindcss";

const config: Config = {
  plugins: [
    require("tailwindcss-animate"),
    require("@tailwindcss/typography"),
  ],
};
export default config;