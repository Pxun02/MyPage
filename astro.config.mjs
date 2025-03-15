import { defineConfig } from 'astro/config';
import expressiveCode from 'astro-expressive-code';

import react from "@astrojs/react";
import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
  site: 'https://Pxun02.github.io',
  base: "/MyPage",
  integrations: [react(), expressiveCode(), mdx()]
});