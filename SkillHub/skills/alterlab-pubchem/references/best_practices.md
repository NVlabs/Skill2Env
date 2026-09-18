# PubChem — Rate Limits, Best Practices & Troubleshooting

## API Rate Limits

- Maximum 5 requests per second
- Maximum 400 requests per minute
- Maximum 300 seconds running time per minute

## Best Practices

1. **Use CIDs for repeated queries**: CIDs are more efficient than names or structures
2. **Cache results locally**: Store frequently accessed data
3. **Batch requests**: Combine multiple queries when possible
4. **Implement delays**: Add 0.2-0.3 second delays between requests
5. **Handle errors gracefully**: Check for HTTP errors and missing data
6. **Use PubChemPy**: Higher-level abstraction handles many edge cases
7. **Leverage asynchronous pattern**: For large similarity/substructure searches
8. **Specify MaxRecords**: Limit results to avoid timeouts

## Error Handling

```python
from pubchempy import BadRequestError, NotFoundError, TimeoutError

try:
    compound = pcp.get_compounds('query', 'name')[0]
except NotFoundError:
    print("Compound not found")
except BadRequestError:
    print("Invalid request format")
except TimeoutError:
    print("Request timed out - try reducing scope")
except IndexError:
    print("No results returned")
```

## Troubleshooting

**Compound Not Found**:
- Try alternative names or synonyms
- Use CID if known
- Check spelling and chemical name format

**Timeout Errors**:
- Reduce MaxRecords parameter
- Add delays between requests
- Use CIDs instead of names for faster queries

**Empty Property Values**:
- Not all properties are available for all compounds
- Check if property exists before accessing: `if compound.xlogp:`
- Some properties only available for certain compound types

**Rate Limit Exceeded**:
- Implement delays (0.2-0.3 seconds) between requests
- Use batch operations where possible
- Consider caching results locally

**Similarity/Substructure Search Hangs**:
- These are asynchronous operations that may take 15-30 seconds
- PubChemPy handles polling automatically
- Reduce MaxRecords if timing out

## Additional Resources

- PubChem Home: https://pubchem.ncbi.nlm.nih.gov/
- PUG-REST Documentation: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
- PUG-REST Tutorial: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest-tutorial
- PubChemPy Documentation: https://pubchempy.readthedocs.io/
- PubChemPy GitHub: https://github.com/mcs07/PubChemPy
