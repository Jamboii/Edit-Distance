import sys


def edit_distance(X, Y, substitution_cost=2):
    m = len(X)
    n = len(Y)

    d = []
    ptr = []

    # Initialize data structures
    for i in range(m+1):
        d.append([])
        ptr.append([])
        for j in range(n+1):
            d[i].append(0)
            ptr[i].append(set())

    # Begin MED algorithm
    # Base conditions
    for i in range(m+1):
        d[i][0] = i
        ptr[i][0].add("DOWN")

    for j in range(n+1):
        d[0][j] = j
        ptr[0][j].add("LEFT")

    # Recurrence Relation
    for i in range(1, m+1):
        for j in range(1, n+1):
            deletion = d[i-1][j] + 1
            insertion = d[i][j-1] + 1
            # Change to index-1 due to zero-based indexing
            # Out of range IndexError otherwise
            if X[i - 1] != Y[j - 1]:
                substitution = d[i-1][j-1] + substitution_cost
            else:
                substitution = d[i - 1][j - 1]
            d[i][j] = min(deletion, insertion, substitution)
            if d[i][j] == deletion:
                ptr[i][j].add("DOWN")
            if d[i][j] == insertion:
                ptr[i][j].add("LEFT")
            if d[i][j] == substitution:
                ptr[i][j].add("DIAG")

    # Generate the backtrace
    backtrace = find_backtrace(ptr, m, n)
    # backtrace = 0
    # For words, edit distance cost is just d[m][n]
    # Sentence scores handled in translation_memory_retrieval.py
    cost = d[m][n]

    return cost, backtrace


def find_backtrace(ptr, m, n):

    i = m
    j = n

    # Initialize backtrace with last location in distance table
    backtrace = [(m, n, "INIT")]

    while True:
        # Substitution
        if "DIAG" in ptr[i][j]:
            i -= 1
            j -= 1
            backtrace.append((i, j, "DIAG"))
        # Insertion
        elif "LEFT" in ptr[i][j]:
            j -= 1
            backtrace.append((i, j, "LEFT"))
        # Deletion
        elif "DOWN" in ptr[i][j]:
            i -= 1
            backtrace.append((i, j, "DOWN"))
        else:
            raise ValueError(f"No ptr information found for i={i} and j={j}")
        # Once we reach the initial point, break out of the while loop
        if i == 0 and j == 0:
            break

    return backtrace


def print_alignment(backtrace, X, Y, outputFile, substitution_cost=2):
    i = 0
    j = 0
    outputFile.write("Alignment: (")
    # Reverse the backtrace to begin with the beginning of the words
    backtrace.reverse()
    for k, trace in enumerate(backtrace):

        # Print a comma only after the first trace and not after the last trace
        if k != 0 and trace[2] != "INIT":
            outputFile.write(", ")

        # Substitution
        if "DIAG" == trace[2]:
            outputFile.write(f"{X[i]}->{Y[j]} ")
            if X[i] == Y[j]:
                outputFile.write("0",)
            else:
                outputFile.write(str(substitution_cost))
            i += 1
            j += 1
        # Insertion
        elif "LEFT" == trace[2]:
            outputFile.write(f"*->{Y[j]} 1")
            j += 1
        # Deletion
        elif "DOWN" == trace[2]:
            outputFile.write(f"{X[i]}->* 1")
            i += 1
        # End of trace / beginning of backtrace (d[m][n])
        elif "INIT" == trace[2]:
            break
        else:
            raise ValueError(f"Improperly formatted backtrace")
    outputFile.write(")\n")


if __name__ == '__main__':

    # Try to assign word input arguments
    try:
        word1 = str(sys.argv[1])
        word2 = str(sys.argv[2])
    except IndexError:
        print("Not enough input arguments: python3 edit_distance.py <word1> <word2>")
        exit()

    # Make sure at least one word is populated
    if len(word1) == 0 and len(word2) == 0:
        raise ValueError("At least one word must be populated.")

    # Compute the edit distance and backtrace
    cost, backtrace = edit_distance(word1, word2)

    # Print out cost and alignment
    print(f"Cost of editing {word1} into {word2}: {cost}")
    print_alignment(backtrace, word1, word2, sys.stdout)
