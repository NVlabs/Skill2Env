# Author Schema Templates

Copy-paste JSON-LD templates for Person, Author, and Organization schemas. Use these as-is and fill in the placeholders. These are not advice. They're the actual blocks to drop into the `<head>` of a page.

A note before the templates: schema without substance is worse than no schema. Marking a page with Person + Author + Organization when the content shows no experience is a flag, not a fix. The content has to support the claims the schema makes. Add the schema after you've audited Experience and Trust, not instead.

## Person schema

The core entity. Describes the author as a real-world person with verifiable references. The `sameAs` array is the most important field. It's what lets Google's knowledge graph disambiguate this person from every other person with the same name.

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://example.com/authors/jane-doe#person",
  "name": "Jane Doe",
  "url": "https://example.com/authors/jane-doe",
  "image": "https://example.com/images/jane-doe.jpg",
  "jobTitle": "Senior Tax Advisor",
  "worksFor": {
    "@type": "Organization",
    "name": "Example Tax Advisory",
    "url": "https://example.com"
  },
  "alumniOf": {
    "@type": "EducationalOrganization",
    "name": "University of Amsterdam"
  },
  "knowsAbout": [
    "Dutch tax law",
    "International tax treaties",
    "Small business taxation"
  ],
  "sameAs": [
    "https://www.linkedin.com/in/janedoe",
    "https://twitter.com/janedoe",
    "https://github.com/janedoe",
    "https://orcid.org/0000-0000-0000-0000",
    "https://www.wikidata.org/wiki/Q0000000"
  ]
}
```

Fields to fill: `name`, `url`, `image`, `jobTitle`, `worksFor`, `alumniOf`, `knowsAbout` (the list of topics the author has demonstrated expertise in, kept narrow at 3 to 5 items), and the `sameAs` array.

## Author attached to an Article

The Person block above goes in the `author` field of the article. You can either inline the Person or reference it by `@id` if you've already declared it on the same page or in a site-wide JSON-LD block.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to File Dutch Taxes as a Freelancer",
  "datePublished": "2026-04-13",
  "dateModified": "2026-04-13",
  "author": {
    "@type": "Person",
    "@id": "https://example.com/authors/jane-doe#person",
    "name": "Jane Doe",
    "url": "https://example.com/authors/jane-doe",
    "sameAs": [
      "https://www.linkedin.com/in/janedoe",
      "https://orcid.org/0000-0000-0000-0000"
    ]
  },
  "publisher": {
    "@type": "Organization",
    "@id": "https://example.com#organization"
  }
}
```

`datePublished` and `dateModified` are not optional on YMYL content. Google's Quality Rater Guidelines explicitly treat update freshness as a trust signal for time-sensitive topics.

## Organization schema for the publishing site

Declare this once in a site-wide JSON-LD block. Other schemas on individual pages reference it by `@id`.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com#organization",
  "name": "Example Tax Advisory",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "description": "Dutch tax advisory for freelancers and small businesses.",
  "foundingDate": "2018-01-01",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Herengracht 1",
    "addressLocality": "Amsterdam",
    "postalCode": "1015BA",
    "addressCountry": "NL"
  },
  "sameAs": [
    "https://www.linkedin.com/company/example-tax-advisory",
    "https://www.wikidata.org/wiki/Q0000001"
  ]
}
```

## Worked example: all three nested for a single article

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com#organization",
      "name": "Example Tax Advisory",
      "url": "https://example.com",
      "logo": "https://example.com/logo.png",
      "sameAs": [
        "https://www.linkedin.com/company/example-tax-advisory"
      ]
    },
    {
      "@type": "Person",
      "@id": "https://example.com/authors/jane-doe#person",
      "name": "Jane Doe",
      "url": "https://example.com/authors/jane-doe",
      "jobTitle": "Senior Tax Advisor",
      "worksFor": { "@id": "https://example.com#organization" },
      "sameAs": [
        "https://www.linkedin.com/in/janedoe",
        "https://orcid.org/0000-0000-0000-0000"
      ]
    },
    {
      "@type": "Article",
      "headline": "How to File Dutch Taxes as a Freelancer",
      "datePublished": "2026-04-13",
      "dateModified": "2026-04-13",
      "author": { "@id": "https://example.com/authors/jane-doe#person" },
      "publisher": { "@id": "https://example.com#organization" }
    }
  ]
}
```

Using `@graph` with `@id` references keeps the blocks clean and lets Google resolve Person to Organization to Article as a single connected entity graph.

## Why sameAs is the most important field

The `sameAs` property on the Person entity is where you tell Google "this author is the same person as the LinkedIn profile at X, the ORCID at Y, the Wikidata entity at Z." Without it, the author is a name string in isolation. With it, the author is a node in the knowledge graph that Google can cross-reference against everything else it knows about that person.

Priority order for `sameAs` entries:

1. **Wikidata** if the author has an entry. This is the strongest entity anchor Google has.
2. **LinkedIn** verifies employment history and credentials.
3. **ORCID** for academic and research authors, verifies publications.
4. **GitHub** for technical authors, verifies code contributions.
5. **Institutional profile page** for university faculty, government agencies, professional registries.
6. **Twitter / X** is the weakest of the commonly-used options but still a recognised profile endpoint.

Include as many as you have real profiles for. Do not include profiles that don't exist or that don't actually belong to the author. Google cross-checks, and broken `sameAs` links are worse than no `sameAs` at all.

## Final warning

Schema is not a substitute for the content being real. A page with beautifully nested Person + Author + Organization schema but no actual experience signals in the prose reads, to a careful rater and to the algorithm, as someone trying to game the system. Build the content first, audit for Experience and Trust, fix the gaps, and then add the schema on top of the fix. Schema is the last step, not the first.
