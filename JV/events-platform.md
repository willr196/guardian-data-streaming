# Events Platform

## Project Overview

A small community business has reached out to you to create a platform where they can create and share events with members of the community.

You have been tasked with building and a mobile app that allows community members to view, sign up for, and add events to their own personal calendars. Staff members should have additional functionality to create and manage events.

## Minimum Viable Product (MVP)

Your platform must fulfill the following functionality:

1. Display a list of events for users to browse.
2. Allow users to sign up for an event.
3. Allow users to add events to their Google Calendar after signing up.
4. Enable staff members to sign-in to create and manage events.

See [Completion and Submission Requirements](#completion-and-submission-requirements) for more details.

## Tech Choices:

- The platform should be built using **Java** or **Kotlin**.
- **Event Data**: You can use either a freely available API for event data or create your own event data. Research and decide on which API to use prior to starting. The focus is on building the platform, not on data generation.
- **Calendar API**: You'll need to sign up for the Google Calendar API (or an equivalent) using a free developer account. This will allow users to add events to their calendars.
- Implement security best practices for **user authentication and authorisation** (e.g., OAuth login flow, username and password, web tokens)

The following technologies and tools are **suggestions**, not requirements:

- **Android** for the frontend.
- **Kotlin** for a new challenge.
- **Google Calendar API** for calendar integration.
- **Spring Security** for authentication.

## UI Requirements

- Design should be **responsive** and adapt well across various mobile device screen sizes.
- Ensure **accessibility** for users with disabilities (e.g., support screen readers, voice navigation).
- The UI should clearly display **errors** (e.g., failed requests or missing fields) and show loading states when content is being fetched.
- The user interface should be intuitive, making it easy to find, sign up for, and create events.

## Completion and Submission Requirements

The due date will be advised, but it will be no later than four weeks after the project commencement.

Your project must meet the following criteria to be considered complete:

1. The project should feature a fully documented backend API application and an Android Studio project for the frontend app.
2. **README Documentation** should include:
   - A summary of the project
     - (you may consider recording a **video walkthrough** of your platform, highlighting key features. Host this video on a free platform (e.g., YouTube) and include a link in your README.)
   - Clear instructions on how to run the project locally, including setup steps (e.g., installing dependencies, any necessary API keys, database setup, configuring application properties and environment variables).
3. Meet the [MVP requirements](#minimum-viable-product-mvp) outlined above.

Failure to do this may result in the project being rejected.

## _Optional_ Extensions

If you have time once you have completed the MVP requirements, consider adding the following features:

1. **Payment platform integration**: Implement payments via Stripe, Google Pay, etc.
2. **Confirmation emails**: Automatically send confirmation emails to users who sign up for an event.
3. **Social media integration**: Allow users to share events on social platforms.
4. **Cross-platform**: Build both a mobile app and website.
5. **Google/Social login**: Allow users to sign up using their Google or social media accounts.
