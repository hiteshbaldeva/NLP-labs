import json
import math




with open("text_segmentation_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)



# 2. GET WORD FREQUENCIES


word_counts = data["word_counts"]


vocabulary = set(word_counts.keys())

# Total frequency of all words
total_frequency = sum(word_counts.values())

# Maximum word length
max_word_length = max(len(word) for word in vocabulary)

print("Vocabulary Size:", len(vocabulary))
print("Total Frequency:", total_frequency)
print("Maximum Word Length:", max_word_length)


# ============================================================
# 3. CALCULATE LOG PROBABILITY
# ============================================================

def log_probability(word):

    frequency = word_counts[word]

    probability = frequency / total_frequency

    return math.log(probability)


# ============================================================
# 4. DYNAMIC PROGRAMMING SEGMENTATION
# ============================================================

def dp_segment(text, vocabulary, max_word_length):

    n = len(text)

    # --------------------------------------------------------
    # dp[i] = maximum log probability for first i characters
    # --------------------------------------------------------

    dp = [-float("inf")] * (n + 1)

    # Empty string has probability 1
    # log(1) = 0
    dp[0] = 0


    # --------------------------------------------------------
    # Store the word selected to reach each position
    # --------------------------------------------------------

    best_word = [None] * (n + 1)


    # --------------------------------------------------------
    # DP
    # --------------------------------------------------------

    for i in range(n):

        # If this position cannot be reached,
        # skip it
        if dp[i] == -float("inf"):
            continue

        # Try every possible word length
        max_length = min(
            max_word_length,
            n - i
        )

        for length in range(1, max_length + 1):

            candidate = text[i:i + length]

            # Check if candidate is a vocabulary word
            if candidate in vocabulary:

                # Calculate score
                score = dp[i] + log_probability(candidate)

                # If this segmentation is better
                if score > dp[i + length]:

                    dp[i + length] = score

                    best_word[i + length] = candidate


    # ========================================================
    # 5. RECONSTRUCT SEGMENTATION
    # ========================================================

    result = []

    position = n

    while position > 0:

        word = best_word[position]

        # No valid segmentation found
        if word is None:

            # Treat current character as unknown
            result.append(text[position - 1])

            position -= 1

        else:

            result.append(word)

            position -= len(word)


    
    result.reverse()

    return result


# ============================================================
# 6. TEST ON ONE EXAMPLE
# ============================================================

text = "likelywillthemillionissueearlierinthesessionashisfirst"

prediction = dp_segment(
    text,
    vocabulary,
    max_word_length
)

print("\nInput:")
print(text)

print("\nDP Segmentation:")
print(" ".join(prediction))


# ============================================================
# 7. ACCURACY
# ============================================================

def calculate_accuracy(predicted, actual):

    correct = 0

    for pred, true in zip(predicted, actual):

        if pred == true:
            correct += 1

    return correct / len(actual)


# ============================================================
# 8. EDIT DISTANCE
# ============================================================

def edit_distance(predicted, actual):

    m = len(predicted)
    n = len(actual)

    # DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j


    # Fill table
    for i in range(1, m + 1):

        for j in range(1, n + 1):

            if predicted[i - 1] == actual[j - 1]:

                dp[i][j] = dp[i - 1][j - 1]

            else:

                dp[i][j] = 1 + min(
                    dp[i - 1][j],       # deletion
                    dp[i][j - 1],       # insertion
                    dp[i - 1][j - 1]    # substitution
                )

    return dp[m][n]


# ============================================================
# 9. RUN DP ON ALL TEST CASES
# ============================================================

test_cases = data["test_cases"]

total_accuracy = 0
total_edit_distance = 0


for case in test_cases:

    # Unsegmented text
    text = case["input"]

    # Correct segmentation
    ground_truth = case["ground_truth"]

    # Convert ground truth to list
    actual = ground_truth.split()

    # DP prediction
    predicted = dp_segment(
        text,
        vocabulary,
        max_word_length
    )

    # Accuracy
    accuracy = calculate_accuracy(
        predicted,
        actual
    )

    # Edit distance
    distance = edit_distance(
        predicted,
        actual
    )

    total_accuracy += accuracy
    total_edit_distance += distance


# ============================================================
# 10. FINAL RESULTS
# ============================================================

number_of_cases = len(test_cases)

average_accuracy = (
    total_accuracy / number_of_cases
)

average_edit_distance = (
    total_edit_distance / number_of_cases
)


print("\n" + "=" * 60)
print("DYNAMIC PROGRAMMING RESULTS")
print("=" * 60)

print("Number of Test Cases :", number_of_cases)

print(
    "Average Accuracy     :",
    round(average_accuracy * 100, 2),
    "%"
)

print(
    "Average Edit Distance:",
    round(average_edit_distance, 2)
)