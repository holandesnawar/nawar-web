import { defineCollection, z } from 'astro:content'

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    publishedAt: z.coerce.date(),
    excerpt: z.string().optional(),
    category: z.enum(['inburgering', 'cultura', 'vocabulario', 'pronunciacion']).optional(),
    mainImage: z
      .object({
        src: z.string(),
        alt: z.string().optional(),
      })
      .optional(),
    readingMinutes: z.number().optional(),
    seo: z
      .object({
        title: z.string().optional(),
        description: z.string().optional(),
      })
      .optional(),
  }),
})

export const collections = { blog }
