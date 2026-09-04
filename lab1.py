import os
import re



INPUT_FILE = "hi_1M_sentences.txt"
OUTPUT_FOLDER = "tokenized_output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


EMAIL_PATTERN = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'


URL_PATTERN = r'(?:https?://|www\.)[^\s]+'


DATE_PATTERN = r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b'

# Number / Decimal
NUMBER_PATTERN = r'\d+(?:\.\d+)?'






HINDI_WORD_PATTERN = r'[\u0900-\u0963\u0966-\u097F]+'

# English words
ENGLISH_WORD_PATTERN = r'[A-Za-z]+'

# Punctuation
PUNCT_PATTERN = r'[^\w\s]'



TOKEN_PATTERN = re.compile(
    f'{EMAIL_PATTERN}|'
    f'{URL_PATTERN}|'
    f'{DATE_PATTERN}|'
    f'{NUMBER_PATTERN}|'
    f'{HINDI_WORD_PATTERN}|'
    f'{ENGLISH_WORD_PATTERN}|'
    f'{PUNCT_PATTERN}',
    re.UNICODE
)



def sentence_tokenizer(text):

    
    text = text.replace("\n", " ")

    
    # . ! ? । ॥
    sentences = re.split(
        r'(?<=[.!?।॥])\s+',
        text
    )

    result = []

    for sentence in sentences:

        sentence = sentence.strip()

        if sentence != "":
            result.append(sentence)

    return result



def word_tokenizer(sentence):

    return TOKEN_PATTERN.findall(sentence)


# =====================================
# STATISTICS
# =====================================

total_sentences = 0
total_words = 0
total_characters = 0

unique_tokens = set()




if not os.path.exists(INPUT_FILE):

    print("Input file not found:")
    print(INPUT_FILE)

    exit()




with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    text = f.read()


# =====================================
# SENTENCE TOKENIZATION
# =====================================

sentences = sentence_tokenizer(text)


# =====================================
# OUTPUT FILE
# =====================================

output_file = os.path.join(
    OUTPUT_FOLDER,
    "hi_1M_sentences.txt"
)


# =====================================
# WORD TOKENIZATION
# =====================================

with open(
    output_file,
    "w",
    encoding="utf-8"
) as out:

    for sentence in sentences:

        tokens = word_tokenizer(sentence)

        if len(tokens) == 0:
            continue

        total_sentences += 1

        total_words += len(tokens)

        for token in tokens:

            total_characters += len(token)

            unique_tokens.add(token)

        # Write tokenized sentence
        out.write(" ".join(tokens))
        out.write("\n")


# =====================================
# CORPUS STATISTICS
# =====================================

if total_sentences > 0:

    avg_sentence_length = (
        total_words / total_sentences
    )

else:

    avg_sentence_length = 0


if total_words > 0:

    avg_word_length = (
        total_characters / total_words
    )

else:

    avg_word_length = 0


if total_words > 0:

    ttr = (
        len(unique_tokens) / total_words
    )

else:

    ttr = 0


# =====================================
# PRINT STATISTICS
# =====================================

print("=" * 60)
print("HINDI CORPUS STATISTICS")
print("=" * 60)

print("Total Sentences         :", total_sentences)
print("Total Tokens            :", total_words)
print("Total Characters        :", total_characters)

print(
    "Average Sentence Length :",
    round(avg_sentence_length, 2)
)

print(
    "Average Token Length    :",
    round(avg_word_length, 2)
)

print(
    "Unique Tokens           :",
    len(unique_tokens)
)

print(
    "Type Token Ratio (TTR)  :",
    round(ttr, 4)
)


# =====================================
# SAVE STATISTICS
# =====================================

stats_file = os.path.join(
    OUTPUT_FOLDER,
    "corpus_statistics.txt"
)

with open(
    stats_file,
    "w",
    encoding="utf-8"
) as f:

    f.write("Hindi Corpus Statistics\n")
    f.write("=" * 30 + "\n\n")

    f.write(
        f"Total Sentences : {total_sentences}\n"
    )

    f.write(
        f"Total Tokens : {total_words}\n"
    )

    f.write(
        f"Total Characters : {total_characters}\n"
    )

    f.write(
        f"Average Sentence Length : "
        f"{avg_sentence_length:.2f}\n"
    )

    f.write(
        f"Average Token Length : "
        f"{avg_word_length:.2f}\n"
    )

    f.write(
        f"Unique Tokens : "
        f"{len(unique_tokens)}\n"
    )

    f.write(
        f"Type Token Ratio (TTR) : "
        f"{ttr:.4f}\n"
    )


# =====================================
# SHOW TOKENIZATION
# =====================================

print("\n")
print("=" * 60)
print("TOKENIZATION DEMONSTRATION")
print("=" * 60)

for i, sentence in enumerate(sentences[:5], start=1):

    tokens = word_tokenizer(sentence)

    print(f"\nSentence {i}:")
    print(sentence)

    print("\nTokens:")
    print(tokens)

    print("\nTokens with position:")

    for j, token in enumerate(tokens, start=1):

        print(f"{j:2}. {token}")


# =====================================
# FINAL
# =====================================

print("\n")
print("Tokenized file saved at:")
print(output_file)

print("\nStatistics saved at:")
print(stats_file)