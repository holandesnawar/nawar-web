import { post } from './post'
import { homePage } from './homePage'
import { contactPage } from './contactPage'
import { waitlistPage } from './waitlistPage'
import { landingPage } from './landingPage'

export const schema = {
  types: [landingPage, post, homePage, contactPage, waitlistPage],
}
