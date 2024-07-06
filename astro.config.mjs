import { defineConfig } from 'astro/config';

import react from "@astrojs/react";

// https://astro.build/config
export default defineConfig({
  site: 'https://Pxun02.github.io',
  base: '/MyPage',
  integrations: [react()]
});