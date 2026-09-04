import json



with open("text_segmentation_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)


# ============================================================
# 2. GET VOCABULARY
# ============================================================

word_counts = data["word_counts"]

vocabulary = set(word_counts.keys())

max_word_length = max(len(word) for word in vocabulary)

print("Vocabulary Size:", len(vocabulary))
print("Maximum Word Length:", max_word_length)



def greedy_segment(text, vocabulary, max_word_length):

    result = []

    i = 0

    while i < len(text):

        longest_word = None

        
        max_length = min(max_word_length, len(text) - i)

        # Try longest word first
        for length in range(max_length, 0, -1):

            candidate = text[i:i + length]

            if candidate in vocabulary:
                longest_word = candidate
                break

        # If a dictionary word was found
        if longest_word is not None:

            result.append(longest_word)

            # Move forward by length of selected word
            i += len(longest_word)

        else:

           
            result.append(text[i])

            i += 1

    return result




def calculate_accuracy(predicted, actual):

    correct = 0

    # Compare corresponding words
    for pred, true in zip(predicted, actual):

        if pred == true:
            correct += 1

    accuracy = correct / len(actual)

    return accuracy




def edit_distance(predicted, actual):

    m = len(predicted)
    n = len(actual)

    # dp[i][j] = edit distance between
    # first i predicted words and
    # first j actual words

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    # Fill DP table
    for i in range(1, m + 1):

        for j in range(1, n + 1):

            if predicted[i - 1] == actual[j - 1]:

                # No operation required
                dp[i][j] = dp[i - 1][j - 1]

            else:


                dp[i][j] = 1 + min(
                    dp[i - 1][j],       # deletion
                    dp[i][j - 1],       # insertion
                    dp[i - 1][j - 1]    # substitution
                )

    return dp[m][n]


# ============================================================
# 6. RUN GREEDY ON ALL TEST CASES
# ============================================================

test_cases = data["test_cases"]

total_accuracy = 0
total_edit_distance = 0


for case in test_cases:

    text = case["input"]

   
    ground_truth = case["ground_truth"]

    
    actual = ground_truth.split()

  
    predicted = greedy_segment(
        text,
        vocabulary,
        max_word_length
    )

    # Calculate accuracy
    accuracy = calculate_accuracy(
        predicted,
        actual
    )

    # Calculate edit distance
    distance = edit_distance(
        predicted,
        actual
    )

    total_accuracy += accuracy
    total_edit_distance += distance


# ============================================================
# 7. FINAL RESULTS
# ============================================================

number_of_cases = len(test_cases)

average_accuracy = total_accuracy / number_of_cases

average_edit_distance = total_edit_distance / number_of_cases


print("\n" + "=" * 60)
print("GREEDY ALGORITHM RESULTS")
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