import { post } from './post'
import { homePage } from './homePage'
import { contactPage } from './contactPage'
import { waitlistPage } from './waitlistPage'

export const schema = {
  types: [post, homePage, contactPage, waitlistPage],
}
