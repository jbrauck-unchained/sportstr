from similarity_check import deduplicate_articles

# Test case 1: Duplicate headlines
headline1 = "Scientists discover new species of butterfly in the Amazon rainforest."
headline2 = "Researchers find a previously unknown type of moth in the Amazon jungle."
headline3 = "Researchers find a previously unknown species of butterfly in the Amazon rainforest."

# Test case 2: Non-duplicate headlines
headline4 = "Apple announces new iPhone model"
headline5 = "Microsoft unveils new software update for Windows 10"

# Previous notes (simulate previously seen headlines)
prev_notes = [headline1, headline2]

# Test deduplication function
print("Test case 1:")
print("Expecting: True")
print("Result:", deduplicate_articles(headline3, prev_notes))

print("\nTest case 2:")
print("Expecting: False")
print("Result:", deduplicate_articles(headline4, prev_notes))
print("Expecting: False")
print("Result:", deduplicate_articles(headline5, prev_notes))
