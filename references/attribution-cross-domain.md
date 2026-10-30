# Attribution, cross-domain, and cookies

Use this reference when sessions break across domains, traffic is mis-attributed, click IDs are
lost, or cookie lifetime affects conversion matching. Verify every platform rule against the
current [official references](official-references.md); this file lists what to inspect, not
vendor constants.

## Cross-domain and subdomains

- Inventory every hostname in the journey: marketing site, app, checkout, payment gateway, help
  center, and embedded widgets. Subdomains of one registrable domain usually share first-party
  cookies; separate registrable domains need linker configuration.
- Confirm the domain list is configured where the Google tag reads it, and that links and forms
  to those domains actually carry the linker parameter. A configured list does not prove the
  parameter reached the destination page.
- Test the full path in Preview and in the request: the client ID or session identifiers must be
  identical before and after the hop. Redirects, payment gateways, and `target=_blank` popups are
  the usual breakpoints.
- If the hop crosses a domain you do not control (a hosted payment page), record the limitation
  and move the conversion fact to a server-side or backend source instead of assuming continuity.

## Referral and campaign integrity

- Payment gateways and identity providers can appear as referrers and replace the real source.
  Check the property's unwanted-referral configuration and whether the redirect strips query
  parameters.
- Campaign parameters (`utm_*`) and click identifiers (`gclid`, `wbraid`, `gbraid`, and others)
  can be dropped by redirects, URL shorteners, link-in-bio tools, or consent-dependent storage.
  Compare the landing URL, the first hit's parameters, and the stored cookie values.
- Do not rewrite or normalize `utm_*` values in GTM unless the attribution owner specified the
  rule; silent case or whitespace changes split reports.
- Self-referrals in reports are a symptom, not a diagnosis: locate the hop that creates a new
  session before changing exclusions.

## Cookies and identifiers

- Identify the writer of each identifier (Google tag, a template, application code, a server
  response) and its `SameSite`, `Secure`, domain, and lifetime. Browser storage limits can shorten
  JavaScript-set cookies; a server-set first-party cookie behaves differently. Verify the current
  browser behavior before promising a lifetime.
- Conversion matching windows depend on the identifier surviving until conversion. Test a delayed
  conversion, not only the landing session.
- Consent affects whether identifiers are stored or read; test granted and denied paths and record
  which identifiers exist in each. A cookie existing does not prove it is used by a destination.

## Evidence

Cross-domain: same client/session identifier on both sides, with the hop's URL parameters redacted
in notes. Attribution: first-hit parameters, stored values, and a destination view of the source,
labeled by the layer reached (see [audit evidence](audit-evidence.md)).
