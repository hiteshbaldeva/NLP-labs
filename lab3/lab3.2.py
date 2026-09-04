class MorphologicalFST:

    def __init__(self):
        self.lexicon = set()
        self.analysis = {}

        self.transition_table = {
            "NORMAL": {
                "s": ("PLURAL_S", "+PL"),
            },

            "ES": {
                "e": ("ES_E", "ε"),
                "s": ("PLURAL_ES", "+PL"),
            },

            "IES": {
                "i": ("IES_I", "y"),
                "e": ("IES_E", "ε"),
                "s": ("PLURAL_IES", "+PL"),
            }
        }

        self.final_states = {
            "SINGULAR",
            "PLURAL_S",
            "PLURAL_ES",
            "PLURAL_IES"
        }

    def build_lexicon(self, words):
        for word in words:
            word = word.strip().lower()

            if word.isalpha():
                self.lexicon.add(word)

    def is_consonant(self, ch):
        return ch.lower() not in "aeiou"

    def root_type(self, root):
        if root.endswith("sh"):
            return "ES"

        if root.endswith("ch"):
            return "ES"

        if root.endswith("s"):
            return "ES"

        if root.endswith("z"):
            return "ES"

        if root.endswith("x"):
            return "ES"

        if root.endswith("y"):
            if len(root) >= 2 and self.is_consonant(root[-2]):
                return "IES"

        return "NORMAL"

    def trace(self, word, root, rule):

        print("\n" + "-" * 75)
        print("FST TRACE")
        print("-" * 75)

        print(f"{'Step':<8}{'State':<18}{'Input':<10}{'Output':<12}{'Next State'}")
        print("-" * 75)

        state = "q0"
        step = 1

        for ch in root:

            next_state = "qROOT"

            print(
                f"{step:<8}{state:<18}{ch:<10}{ch:<12}{next_state}"
            )

            state = next_state
            step += 1

        if rule == "S":

            print(
                f"{step:<8}{'qROOT':<18}{'s':<10}{'+PL':<12}"
                f"{'qPL_S'}"
            )

            final_state = "qPL_S"

        elif rule == "ES":

            print(
                f"{step:<8}{'qROOT':<18}{'e':<10}{'ε':<12}"
                f"{'qE'}"
            )

            step += 1

            print(
                f"{step:<8}{'qE':<18}{'s':<10}{'+PL':<12}"
                f"{'qPL_ES'}"
            )

            final_state = "qPL_ES"

        elif rule == "IES":

            print(
                f"{step:<8}{'qROOT':<18}{'i':<10}{'y':<12}"
                f"{'qI'}"
            )

            step += 1

            print(
                f"{step:<8}{'qI':<18}{'e':<10}{'ε':<12}"
                f"{'qE'}"
            )

            step += 1

            print(
                f"{step:<8}{'qE':<18}{'s':<10}{'+PL':<12}"
                f"{'qPL_IES'}"
            )

            final_state = "qPL_IES"

        else:

            final_state = "qSINGULAR"

        print("-" * 75)

        return final_state

    def analyze(self, word, show_trace=False):

        word = word.strip().lower()

        if not word or not word.isalpha():
            return "Invalid Word"

        # ------------------------------------------------
        # CASE 1: Y -> IES
        # ------------------------------------------------

        if word.endswith("ies") and len(word) > 3:

            root = word[:-3] + "y"

            if root in self.lexicon:

                if (
                    len(root) >= 2
                    and self.is_consonant(root[-2])
                ):

                    if show_trace:
                        final_state = self.trace(
                            word,
                            root[:-1],
                            "IES"
                        )

                        print("Final State:", final_state)

                    return root + "+N+PL"

        # ------------------------------------------------
        # CASE 2: E INSERTION / ES
        # ------------------------------------------------

        if word.endswith("es") and len(word) > 2:

            root = word[:-2]

            if root in self.lexicon:

                if self.root_type(root) == "ES":

                    if show_trace:
                        final_state = self.trace(
                            word,
                            root,
                            "ES"
                        )

                        print("Final State:", final_state)

                    return root + "+N+PL"

        # ------------------------------------------------
        # CASE 3: NORMAL S ADDITION
        # ------------------------------------------------

        if word.endswith("s") and len(word) > 1:

            root = word[:-1]

            if root in self.lexicon:

                if self.root_type(root) == "NORMAL":

                    if show_trace:
                        final_state = self.trace(
                            word,
                            root,
                            "S"
                        )

                        print("Final State:", final_state)

                    return root + "+N+PL"

        # ------------------------------------------------
        # CASE 4: SINGULAR
        # ------------------------------------------------

        if word in self.lexicon:

            if show_trace:

                print("\n" + "-" * 75)
                print("FST TRACE")
                print("-" * 75)

                print(
                    f"{'Step':<8}{'State':<18}"
                    f"{'Input':<10}{'Output':<12}{'Next State'}"
                )

                print("-" * 75)

                state = "q0"

                for i, ch in enumerate(word, 1):

                    print(
                        f"{i:<8}{state:<18}"
                        f"{ch:<10}{ch:<12}qROOT"
                    )

                    state = "qROOT"

                print(
                    f"{len(word) + 1:<8}{'qROOT':<18}"
                    f"{'END':<10}{'ε':<12}qSINGULAR"
                )

                print("-" * 75)
                print("Final State: qSINGULAR")

            return word + "+N+SG"

        return "Invalid Word"

    def demonstrate(self):

        tests = [
            ("S ADDITION", "bags"),
            ("E INSERTION", "foxes"),
            ("Y REPLACEMENT", "tries"),
            ("INVALID WORD", "foxs")
        ]

        print("\n" + "=" * 80)
        print("                    FST DEMONSTRATION")
        print("=" * 80)

        for case, word in tests:

            print("\n" + "=" * 80)
            print(f"CASE: {case}")
            print(f"INPUT: {word}")
            print("=" * 80)

            result = self.analyze(
                word,
                show_trace=True
            )

            print("\nFINAL RESULT")
            print("-" * 40)

            if result == "Invalid Word":
                print("Output : Invalid Word")
                print("Status : REJECTED")
            else:
                print("Output :", result)
                print("Status : ACCEPTED")

    def print_test_cases(self):

        tests = [
            "fox",
            "foxes",
            "foxs",
            "box",
            "boxes",
            "boxs",
            "bag",
            "bags",
            "bagss",
            "watch",
            "watches",
            "watchs",
            "try",
            "tries",
            "trys",
            "baby",
            "babies"
        ]

        print("\n" + "=" * 80)
        print("                    FST TEST CASES")
        print("=" * 80)

        print(f"{'INPUT':<20}{'OUTPUT':<30}{'STATUS'}")
        print("-" * 80)

        for word in tests:

            result = self.analyze(word)

            if result == "Invalid Word":
                status = "REJECTED"
            else:
                status = "ACCEPTED"

            print(
                f"{word:<20}"
                f"{result:<30}"
                f"{status}"
            )

        print("-" * 80)

    def analyze_corpus(self, words):

        for word in words:

            result = self.analyze(word)

            self.analysis[word] = result

    def print_sample(self, words, count=50):

        print("\n" + "=" * 80)
        print("                CORPUS MORPHOLOGICAL ANALYSIS")
        print("=" * 80)

        print(f"{'WORD':<30}{'ANALYSIS'}")
        print("-" * 80)

        for word in words[:count]:

            print(
                f"{word:<30}"
                f"{self.analysis[word]}"
            )

        print("-" * 80)

    def print_statistics(self, words):

        singular = 0
        plural = 0
        invalid = 0

        for word in words:

            result = self.analysis[word]

            if result == "Invalid Word":

                invalid += 1

            elif result.endswith("+PL"):

                plural += 1

            elif result.endswith("+SG"):

                singular += 1

        print("\n" + "=" * 80)
        print("                       STATISTICS")
        print("=" * 80)

        print(f"Total corpus entries : {len(words)}")
        print(f"Unique lexicon words : {len(self.lexicon)}")
        print(f"Singular nouns       : {singular}")
        print(f"Plural nouns         : {plural}")
        print(f"Invalid words        : {invalid}")

        print("=" * 80)

    def write_output(
        self,
        words,
        filename="fst_output.txt"
    ):

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write("=" * 80 + "\n")
            file.write(
                "             FST MORPHOLOGICAL ANALYSIS\n"
            )
            file.write("=" * 80 + "\n\n")

            for word in words:

                file.write(
                    f"{word} = {self.analysis[word]}\n"
                )


def main():

    filename = "brown_nouns.txt"

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            words = [
                line.strip().lower()
                for line in file
                if line.strip()
            ]

    except FileNotFoundError:

        print("\nERROR")
        print("-" * 50)
        print("brown_nouns.txt was not found.")
        print(
            "Keep brown_nouns.txt in the same folder "
            "as this Python file."
        )
        return

    if not words:

        print("ERROR: brown_nouns.txt is empty.")
        return

    fst = MorphologicalFST()

    fst.build_lexicon(words)

    print("\nLexicon loaded successfully.")
    print(
        "Number of noun entries:",
        len(fst.lexicon)
    )

    fst.demonstrate()

    fst.print_test_cases()

    fst.analyze_corpus(words)

    fst.print_sample(
        words,
        count=50
    )

    fst.print_statistics(words)

    fst.write_output(words)

    print(
        "\nComplete output saved to: fst_output.txt"
    )


if __name__ == "__main__":
    main()