# Auto-event triggers, forms, and SPA navigation

Use this reference when the producer cannot push a business event and GTM would infer it from the
DOM, or when navigation in a single-page application (SPA) is measured.

## Prefer the producer; use auto-events only for interaction facts

A click, scroll, element-visibility, or form-submit trigger records that an interaction happened.
It does not record that the business outcome happened. Treat them as interaction events and keep
the outcome event (lead accepted, trial activated, order placed) on a producer or backend fact.
See [event contracts](event-contracts-architecture.md).

## Click and link triggers

- Scope each trigger with explicit conditions (page path, element selector, or an attribute the
  team controls). `Click Text` and generic classes change with copy and redesigns.
- Check which click variable describes the element you need: the click target can be a child of
  the element that carries the attribute, so test with `Click Element` alternatives.
- A trigger that waits for tags or validation changes timing; navigation can cancel pending
  requests. Verify the request completes on outbound or same-tab links.

## Form triggers

- A form-submit trigger fires on the browser event, including submissions that fail validation or
  that the application handles with JavaScript and a request. Distinguish submitted from accepted
  from qualified. Prefer the application's success event.
- Forms inside iframes, shadow DOM, and widgets often do not expose the submit event to the host
  page; confirm in Preview rather than assuming.
- Never copy field values (name, email, message) into event parameters or logs.

## Scroll, visibility, timer, and video

- Define the threshold and the unit (percent or pixels) and fire once per page or per element as
  the contract states. Test short pages and dynamic content that changes page height.
- Visibility triggers can fire repeatedly for the same element; set the firing limit and verify it.
- Native or third-party video events depend on the player API being enabled; verify the player
  actually emits the events before building tags.

## Enhanced measurement overlap

If the destination offers automatic interaction collection (outbound clicks, scrolls, site search,
file downloads, form interactions, video), an equivalent GTM tag can double-count. Record which
mechanism owns each event and disable or exclude the other before release. Configuration overlap
is a finding; counted duplicates need destination evidence.

## SPA navigation

- Initial load, framework route changes, and `history` updates are different signals. Confirm
  which one the producer emits and whether the title and URL are updated before the signal fires.
- A History Change trigger can fire for hash and state changes that are not page views, and may
  fire more than once per navigation. Filter by the fields that change and test back/forward.
- Prefer a producer-pushed virtual page view event with the final URL and title. If you must use
  History Change, read the new URL from the event, not from a variable that may still hold the old
  page.
- Send a page view for a route once; confirm that the automatic page view and any manual or
  server-originated page view do not both fire (see [Web workflow](workflow-web.md)).

## Evidence

For each event: producer or DOM signal, trigger fired with its conditions, tag executed once,
request parameters, and the repeated and negative cases (see [QA matrix](../assets/qa-matrix.template.md)).
