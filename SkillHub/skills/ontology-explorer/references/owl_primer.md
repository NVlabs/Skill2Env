# OWL/RDF Primer for Materials Science Ontologies

## What Is an Ontology?

An ontology is a formal, machine-readable description of concepts in a domain and the relationships between them. In materials science, ontologies standardize how we describe materials, structures, properties, and simulations so that data can be shared and understood consistently.

## Core OWL Concepts

### Classes

A **class** represents a category of things. Examples: `Material`, `CrystalStructure`, `Atom`.

Classes form a **hierarchy** via `rdfs:subClassOf`:
- `CrystallineMaterial` is a subclass of `Material`
- Every crystalline material is a material, but not every material is crystalline

### Individuals (Instances)

An **individual** is a specific instance of a class. Example: a particular FCC copper sample is an individual of the class `AtomicScaleSample`.

### Object Properties

An **object property** links two individuals (or classes). It has a **domain** (source class) and a **range** (target class).

Example: `hasMaterial` has domain `ComputationalSample` and range `Material`.
This means: a computational sample *has a material*, and that material is an instance of the Material class.

### Data Properties

A **data property** links an individual to a literal value (string, float, integer).

Example: `hasSpaceGroupNumber` has domain `CrystalStructure` and range `xsd:integer`.
This means: a crystal structure has a space group number, which is an integer (1-230).

### Domain and Range

- **Domain**: the class that the property applies to (the subject)
- **Range**: the class or datatype of the value (the object)
- If a property has domain `UnitCell` and range `Basis`, it means: the property connects a unit cell to a basis

### Annotations

**Annotations** add human-readable metadata: labels (`rdfs:label`), descriptions (`rdfs:comment`, `skos:definition`), and definitions (IAO).

## Common OWL File Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| OWL/XML (RDF/XML) | `.owl` | Standard XML serialization; most common |
| Turtle | `.ttl` | Compact, human-readable RDF |
| JSON-LD | `.jsonld` | JSON-based linked data |
| N-Triples | `.nt` | One triple per line; simple |

## IRI (Internationalized Resource Identifier)

Every class, property, and individual has a unique **IRI** (like a URL). Example:
- `http://purls.helmholtz-metadaten.de/cmso/UnitCell` identifies the UnitCell class in CMSO

The **local name** is the part after the last `#` or `/`: `UnitCell`.

## Reading an Ontology

To understand an ontology, start with:
1. **Root classes** — the top-level concepts (no parent)
2. **Class hierarchy** — how classes specialize into subclasses
3. **Object properties** — how classes relate to each other
4. **Data properties** — what literal values each class carries

## Key Namespaces

| Prefix | URI | Used For |
|--------|-----|----------|
| `owl` | `http://www.w3.org/2002/07/owl#` | OWL language constructs |
| `rdfs` | `http://www.w3.org/2000/01/rdf-schema#` | Labels, comments, subClassOf |
| `rdf` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | RDF type, about, resource |
| `xsd` | `http://www.w3.org/2001/XMLSchema#` | Data types (string, float, integer) |
| `skos` | `http://www.w3.org/2004/02/skos/core#` | Preferred labels, definitions |
| `dc` | `http://purl.org/dc/elements/1.1/` | Dublin Core metadata |
