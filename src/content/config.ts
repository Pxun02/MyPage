import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.date(),
    password: z.string().optional(),
  }),
});

export const collections = {
  'blog': blogCollection,
};