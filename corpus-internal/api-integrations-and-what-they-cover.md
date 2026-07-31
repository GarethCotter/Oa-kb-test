---
title: "The API and the built-in integrations — read-only, and it needs two switches"
internal: true
last_reviewed: 2026-07-31
---

API access, GraphQL, connect to another system, EventsAir, Cvent, idloom, push data
into Oxford Abstracts, create submissions through the API, API key, API user, API
costs extra, submission ID in the API.

Distilled from around 15 support tickets in the year to July 2026, on top of the
public API article.

**The API is read-only.** It answers queries; it cannot create submissions, insert
submitters or write data back. Anyone wanting to bring data *into* Oxford Abstracts
has to use the admin interface — an organiser can create a submission on someone's
behalf there. There is **no extra charge** for API access.

**Two switches, not one.** Turning API access on for the event is not enough: the
third party's email address must also be added as an **API user** on the event's API
users page before any request returns data. This is the commonest reason a correctly
built integration sees nothing.

**Field names differ from the screen.** The submission number shown in the admin
interface is `serial_number` in GraphQL, not `id`. Matching on `id` produces numbers
that look wrong.

**There are limits on what is exposed** — email content, for example, is not
available. More complex pulls go through the GraphQL endpoint and its documentation.

**Built-in integrations** exist for **EventsAir**, **Cvent** and a beta **idloom**
integration, each configured on the event's integrations page with instructions on the
page itself. For anything else, the API is the route.

**Single sign-on** is separate from all of this: Google and LinkedIn are standard;
organisation-wide SSO is a paid one-off project covering a client's events, and
everyone reaching those events comes through the client's portal.
