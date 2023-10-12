import ironmill_oxide.registry as registry

def main(search_term: str):
    # Get all search results as rows
    results = registry.search(search_term)

    # Format and print result with a header
    print(registry.Row.get_header())
    for result in results:
        print(result)
