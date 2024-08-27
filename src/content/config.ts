// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    description: z.string().optional(),
    slug: z.string(),
  }),
});

export const collections = {
  'blog': blogCollection,
};
