# Available Methods

Methods are invoked using the `->` operator. You MUST NOT make up method names - only use methods listed here.

## Table of Contents

- [String Methods](#string-methods)
- [Object Methods](#object-methods)
- [Array Methods](#array-methods)
- [Logical Methods](#logical-methods)
- [Math Methods](#math-methods)
- [Type Coercion](#type-coercion)
- [Other Methods](#other-methods)

## String Methods

| Method | Description | Example |
|--------|-------------|---------|
| `slice` | Returns a slice of a string | `firstTwo: countryCode->slice(0, 2)` |
| `size` | Returns the length of a string | `length: word->size` |

## Object Methods

| Method | Description | Example |
|--------|-------------|---------|
| `entries` | Returns a list of key-value pairs | `pairs: object->entries` |
| `size` | Returns the number of properties | `count: object->size` |

## Array Methods

| Method | Description | Example |
|--------|-------------|---------|
| `filter` | Returns items matching criteria | `even: numbers->filter(@->mod(2)->eq(0))` |
| `find` | Returns first matching item | `first: items->find(@.active)` |
| `first` | Returns the first item | `first: colors->first` |
| `get` | Returns item at index or key | `third: items->get(2)` |
| `joinNotNull` | Joins strings, ignoring nulls | `full: $([a, b])->joinNotNull(' ')` |
| `last` | Returns the last item | `last: colors->last` |
| `map` | Transforms each item | `wrapped: items->map({ name: @ })` |
| `slice` | Returns a slice of the array | `firstTwo: items->slice(0, 2)` |
| `size` | Returns the array length | `count: items->size` |

### Array Method Examples

**filter** - Filter items by condition:
```
# Keep items where active is true
$.items->filter(@.active)

# Keep even numbers
$.numbers->filter(@->mod(2)->eq(0))

# Chain filters instead of using ->and
$.items->filter(@.active)->filter(@.price->gt(10))
```

**find** - Find first matching item:
```
# Find first active item
$.items->find(@.active)

# Find item with specific id
$.items->find(@.id->eq($args.id))
```

**map** - Transform items:
```
# Wrap each item
$.items->map({ value: @ })

# Extract nested field
$.users->map(@.profile.name)
```

**joinNotNull** - Concatenate strings:
```
# Join name parts with space
fullName: $([firstName, middleName, lastName])->joinNotNull(' ')

# Join address parts with comma
address: $([street, city, state])->joinNotNull(', ')
```

## Logical Methods

| Method | Description | Example |
|--------|-------------|---------|
| `and` | True if all values are true | `both: a->and(b, c)` |
| `contains` | True if array contains value | `hasRed: colors->contains("red")` |
| `eq` | True if equal to argument | `isActive: status->eq("active")` |
| `gt` | True if greater than | `large: size->gt(100)` |
| `gte` | True if greater than or equal | `atLeast: count->gte(10)` |
| `in` | True if value is in list | `valid: status->in("a", "b", "c")` |
| `lt` | True if less than | `small: size->lt(50)` |
| `lte` | True if less than or equal | `within: count->lte(100)` |
| `ne` | True if not equal | `notEmpty: value->ne("")` |
| `not` | Inverts boolean | `inactive: isActive->not` |
| `or` | True if any value is true | `either: a->or(b)` |

### Logical Method Examples

**Comparisons:**
```
# Check equality
isAdmin: role->eq("admin")

# Check inequality
notEmpty: value->ne("")

# Numeric comparisons
expensive: price->gt(100)
affordable: price->lte(50)
```

**Boolean logic:**
```
# AND - all must be true
valid: a->and(b, c)

# OR - any can be true
hasAccess: isAdmin->or(isOwner)

# NOT - invert
hidden: visible->not
```

**Membership:**
```
# Check if value is in list
validStatus: status->in("pending", "active", "complete")

# Check if array contains value
hasPremium: features->contains("premium")
```

## Math Methods

| Method | Description | Example |
|--------|-------------|---------|
| `add` | Addition | `total: price->add(tax)` |
| `div` | Division | `avg: sum->div(count)` |
| `mod` | Modulo (remainder) | `rem: num->mod(5)` |
| `mul` | Multiplication | `area: width->mul(height)` |
| `sub` | Subtraction | `diff: total->sub(discount)` |

### Math Method Examples

```
# Calculate total with tax
totalWithTax: subtotal->mul(1.08)

# Calculate average
average: total->div(count)

# Check if even
isEven: number->mod(2)->eq(0)

# Apply discount
finalPrice: price->sub(discount)
```

## Type Coercion

| Method | Description | Example |
|--------|-------------|---------|
| `parseInt` | Convert to Int | `count: strCount->parseInt` |
| `toString` | Convert to String | `id: numId->toString` |

### Type Coercion Examples

```
# String to integer
count: "42"->parseInt

# Integer to string for ID field
id: numericId->toString

# Parse and calculate
total: strPrice->parseInt->add(tax->parseInt)
```

## Other Methods

| Method | Description | Example |
|--------|-------------|---------|
| `echo` | Returns its argument | `wrapped: value->echo({ data: @ })` |
| `jsonStringify` | Convert to JSON string | `json: obj->jsonStringify` |
| `match` | Replace value based on matches | `status: code->match([1, "one"], [2, "two"], [@, "other"])` |

### Other Method Examples

**echo** - Useful for wrapping values:
```
# Wrap a value in an object
wrapped: items->echo({ data: @ })

# Use with transformations
result: value->echo({ original: @, doubled: @->mul(2) })
```

**match** - Map values to new values:
```
# Map status codes to strings
statusText: status->match(
  [1, "pending"],
  [2, "active"],
  [3, "complete"],
  [@, "unknown"]
)

# Map boolean to text
activeText: isActive->match(
  [true, "Yes"],
  [false, "No"]
)
```

**jsonStringify** - Convert to JSON:
```
# Serialize object for logging
serialized: data->jsonStringify
```
