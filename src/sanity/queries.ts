import { defineQuery } from 'groq'

export const LANDING_QUERY = defineQuery(`
  *[_type == "landingPage"][0]{
    hero,
    stats,
    marqueeItems,
    painPoints,
    features,
    steps,
    comparison,
    testimonials,
    doubts,
    about
  }
`)

export const HOME_QUERY = defineQuery(`
  *[_type == "homePage"][0]{
    hero,
    about,
    "featuredPosts": featuredPosts[]->{
      _id,
      title,
      "slug": slug.current,
      publishedAt,
      excerpt,
      mainImage
    },
    seo
  }
`)

export const POSTS_QUERY = defineQuery(`
  *[_type == "post" && defined(slug.current)] | order(publishedAt desc){
    _id,
    title,
    "slug": slug.current,
    publishedAt,
    excerpt,
    mainImage
  }
`)

export const POST_QUERY = defineQuery(`
  *[_type == "post" && slug.current == $slug][0]{
    _id,
    title,
    "slug": slug.current,
    publishedAt,
    excerpt,
    mainImage,
    body,
    seo
  }
`)

export const POST_SLUGS_QUERY = defineQuery(`
  *[_type == "post" && defined(slug.current)]{ "slug": slug.current }
`)

export const CONTACT_QUERY = defineQuery(`
  *[_type == "contactPage"][0]{ title, intro, email, formTitle, seo }
`)

export const WAITLIST_QUERY = defineQuery(`
  *[_type == "waitlistPage"][0]{
    title, headline, body, formTitle, formButtonText, successMessage, seo
  }
`)
