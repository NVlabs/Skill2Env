# Selection Mapping Grammar

The mapping language uses Extended Backus-Naur Form (EBNF) to describe the complete JSONSelection grammar.

## Table of Contents

- [EBNF Grammar](#ebnf-grammar)
- [Valid Grammar Examples](#valid-grammar-examples)
- [Common Grammar Mistakes](#common-grammar-mistakes)

## EBNF Grammar

```ebnf
JSONSelection        ::= NamedSelection*
SubSelection         ::= "{" NamedSelection* "}"
NamedSelection       ::= (Alias | "...")? PathSelection | Alias SubSelection
Alias                ::= Key ":"
PathSelection        ::= Path SubSelection?
VarPath              ::= "$" (NO_SPACE Identifier)? PathTail
KeyPath              ::= Key PathTail
AtPath               ::= "@" PathTail
ExprPath             ::= "$(" LitExpr ")" PathTail
PathTail             ::= "?"? (PathStep "?"?)*
NonEmptyPathTail     ::= "?"? (PathStep "?"?)+ | "?"
PathStep             ::= "." Key | "->" Identifier MethodArgs?
Key                  ::= Identifier | LitString
Identifier           ::= [a-zA-Z_] NO_SPACE [0-9a-zA-Z_]*
MethodArgs           ::= "(" (LitExpr ("," LitExpr)* ","?)? ")"
LitExpr              ::= LitOpChain | LitPath | LitPrimitive | LitObject | LitArray | PathSelection
LitOpChain           ::= LitExpr (LitOp LitExpr)+
LitOp                ::= "??" | "?!"
LitPath              ::= (LitPrimitive | LitObject | LitArray) NonEmptyPathTail
LitPrimitive         ::= LitString | LitNumber | "true" | "false" | "null"
LitString            ::= "'" ("\\'" | [^'])* "'" | '"' ('\\"' | [^"])* '"'
LitNumber            ::= "-"? ([0-9]+ ("." [0-9]*)? | "." [0-9]+)
LitObject            ::= "{" (LitProperty ("," LitProperty)* ","?)? "}"
LitProperty          ::= Key ":" LitExpr
LitArray             ::= "[" (LitExpr ("," LitExpr)* ","?)? "]"
NO_SPACE             ::= !SpacesOrComments
SpacesOrComments     ::= (Spaces | Comment)+
Spaces               ::= (" " | "\t" | "\r" | "\n")+
Comment              ::= "#" [^\n]*
```

## Valid Grammar Examples

### Basic Field Selection

```
# Direct field selection
id
name
email

# Field aliasing (when renaming)
firstName: name.first
lastName: name.last
```

### Sub-selections

```
# Array sub-selection
$.results {
  id
  name
}

# Nested sub-selection
user {
  profile {
    avatar
  }
}

# First item from array
$.items->first {
  id
  title
}
```

### Method Chaining

```
# Chain methods with ->
name->slice(0, 10)
items->filter(@.active)->first
numbers->map(@->mul(2))
```

### Path Navigation

```
# Dot notation for nested fields
user.profile.name

# Optional chaining with ?
user?.profile?.name

# Variable paths
$args.id
$this.userId
$batch.id
```

### Literal Expressions

```
# Must use $() wrapper
$(1)
$(true)
$("hello")
$({"key": "value"})
$([1, 2, 3])

# Literal with method
$([a, b, c])->joinNotNull(',')
```

### Operators

```
# Null coalescing (fallback for null or undefined)
name ?? "Unknown"

# Undefined coalescing (fallback only for undefined, preserves null)
value ?! "default"
```

## Common Grammar Mistakes

### Wrong: Using `+` for Concatenation

```
# WRONG - No + operator
fullName: firstName + " " + lastName

# CORRECT - Use joinNotNull
fullName: $([firstName, lastName])->joinNotNull(' ')
```

### Wrong: Array Indexing with `[]`

```
# WRONG - No bracket indexing
firstItem: items[0]

# CORRECT - Use methods
firstItem: items->first
thirdItem: items->get(2)
slice: items->slice(0, 3)
```

### Wrong: Literal Without `$()`

```
# WRONG - Missing $() wrapper
body: "{ a: $args.a }"

# CORRECT - Use $() for literal objects
body: "$({ a: $args.a })"
```

### Wrong: Using `==` for Comparison

```
# WRONG - No == operator
isActive: status == "active"

# CORRECT - Use eq method
isActive: status->eq("active")
```

### Wrong: Ternary Operator

```
# WRONG - No ternary operator
result: condition ? a : b

# CORRECT - Use ?? or ?! operators
result: value ?? "default"
result: value ?! "fallback"
```

### Wrong: Unnecessary Root `$`

```
# WRONG - Unnecessary when selecting from root
$ {
  id
  name
}

# CORRECT - Direct field selection
id
name
```
