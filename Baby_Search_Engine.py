import string
def cleanToken(token):
    # Remove leading and trailing punctuation
    token = token.strip(string.punctuation)
    # Check if the token contains at least one letter
    if any(c.isalpha() for c in token):
        # Convert to lowercase
        return token.lower()
    else:
        return ""
def readDocs(database_file):
    forward_index = {}
    # Initialize an empty dictionary to store the forward index
    with open(database_file, 'r', encoding="utf-8") as file:
        current_url = None
        # Initialize the current URL
        unique_tokens = set()
        # Initialize a set to store unique tokens for each URL
        for line in file:
            line = line.strip()
            if line.startswith("https"):
                # Extract the URL from the line
                current_url = line[5:].strip()
            elif line.startswith("<endPageBody>"):
                # Process the tokens and add them to the forward index
                forward_index[current_url] = unique_tokens
                unique_tokens = set()
                # Reset the set for the next URL
            else:
                # Tokenize and clean each word in the line
                words = line.split()
                for word in words:
                    cleaned_word = cleanToken(word)
                    if cleaned_word:
                        unique_tokens.add(cleaned_word)
    return forward_index
def buildInvertedIndex(docs):
    inverted_index = {}
    for url, words in docs.items():
        for word in words:
            if word not in inverted_index:
                inverted_index[word] = set()
            inverted_index[word].add(url)
    return inverted_index
def findQueryMatches(index, query):
    query = query.lower()
    terms = query.split()
    # Initialize a set to store matching URLs
    result = set()
    for term in terms:
        modifier = None
        if term.startswith('+'):
            modifier = 'AND'
            term = term[1:]
        elif term.startswith('-'):
            modifier = 'NOT'
            term = term[1:]
        term = cleanToken(term)
        if term in index:
            term_results = index[term]
            if modifier == 'AND':
                result = result.intersection(term_results)
            elif modifier == 'NOT':
                result = result.difference(term_results)
            else:
                result = result.union(term_results)
    return result
def Baby_Search_Engine(dbfile):
    print("building index...")
    docs = readDocs(dbfile)
    print(f"Indexed {len(docs)} pages containing {sum(len(words) for words in docs.values())} unique terms.")
    while True:
        query = input("Enter query sentence (RETURN/ENTER to quit): ")
        if not query:
            break
        matches = findQueryMatches(buildInvertedIndex(docs), query)
        print(f"Found {len(matches)} matching pages {matches}")
# Example usage
if __name__ == "__main__":
    Baby_Search_Engine("/Users/agile/OneDrive/Desktop/sampleWebsiteData.txt")