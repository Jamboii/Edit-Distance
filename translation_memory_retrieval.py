from edit_distance import edit_distance, print_alignment
import random
import string

def percent_match(M, C):
    # M and C are the list of words in the sentence
    m_unigrams = set(M.split())
    c_unigrams = set(C.split())
    intersection = 0
    for unigram in m_unigrams:
        if unigram in c_unigrams:
            intersection += 1

    return intersection / len(m_unigrams)


def sentence_edit_distance_score(M, C):
    # M and C are the list of words in the sentence
    cost, backtrace = edit_distance(M.split(), C.split(), substitution_cost=1)

    ed_score = max(1.0 - (cost / len(set(M.split()))), 0)

    return ed_score, backtrace

def translation_memory_retrieval(retrieval):
    # Open english and french translation files
    eng = open("en-fr/EMEA.en-fr.en")
    fre = open("en-fr/EMEA.en-fr.fr")
    # Load lines of translation files
    linesEng = eng.readlines()
    linesFre = fre.readlines()
    # set random seed
    random.seed(42)
    # Load 10000 random lines for TMB
    TMB = {}
    # countTMB = {}
    while len(TMB) < 10000:
        idx = random.randint(0,len(linesEng))
        lineEng = linesEng[idx].translate(str.maketrans('','',string.punctuation))
        lineFre = linesFre[idx].translate(str.maketrans('','',string.punctuation))
        if lineEng not in TMB:
            # countTMB[idx] = 1
            TMB[lineEng] = lineFre
    # Write TMB to file
    fileTMB = open("TMB.txt",'w')
    fileTMB.writelines(TMB.keys())
    fileTMB.close()
    # Load 5 random lines for MTBT
    MTBT = {}
    # countMTBT = {}
    while len(MTBT) < 5:
        idx = random.randint(0,len(linesEng))
        lineEng = linesEng[idx].translate(str.maketrans('','',string.punctuation))
        lineFre = linesFre[idx].translate(str.maketrans('','',string.punctuation))
        if lineEng not in TMB and lineEng not in MTBT:
            # countMTBT[idx] = 1
            MTBT[lineEng] = lineFre
    # Write MTBT to file
    fileMTBT = open("MTBT.txt","w")
    fileMTBT.writelines(MTBT.keys())
    fileMTBT.close()
    # For each of the 5 MTBT lines
    fileTopCandidates = open("Top10Candidates{}.txt".format(retrieval),"w")
    for M in MTBT.keys():
        fileTopCandidates.write("Sentence to be translated: \'{}\' \n".format(M.strip("\n")))
        fileTopCandidates.write("-----------------------------------------\n")
        # Find top 10 candidates from TMB using retrieval metric
        scores = {}
        # retrieval = PM
        if retrieval == "PM":
            for C in TMB.keys():
                scores[C] = percent_match(M,C)
            sortedScores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}
        # retrieval = EDscore
        if retrieval == "ED":
            for C in TMB.keys():
                ed_score, backtrace = sentence_edit_distance_score(M,C)
                scores[C] = [ed_score,backtrace]
            sortedScores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1][0], reverse=True)}

        # print top 10 candidates for sentence M
        sentences = list(sortedScores.keys())
        scoreVals = list(sortedScores.values())
        for i in range(10):
            C = sentences[i]
            fileTopCandidates.write("{}: {}".format(i+1, C))
            fileTopCandidates.write("T: {}".format(TMB[C]))
            # retrieval = percentage match
            if retrieval == "PM":
                score = scoreVals[i]
                fileTopCandidates.write("PM SCORE: {}\n".format(score))
            # retrieval = edit distance score
            if retrieval == "ED":
                score = scoreVals[i][0]
                backtrace = scoreVals[i][1]
                print_alignment(backtrace, M.split(), C.split(), fileTopCandidates, substitution_cost=1)
                fileTopCandidates.write("ED SCORE: {}\n".format(score))
            fileTopCandidates.write("\n")
    fileTopCandidates.close()


if __name__ == '__main__':

    # Debugging main
    # sent1 = input("Type your first sentence (M):")
    # sent2 = input("Type your second sentence (C):")
    # sent1 = sent1.split()
    # However we decide to normalize, make sure it is documented in README file
    # sent1[-1] = sent1[-1].strip(".!?")
    # sent2 = sent2.split()
    # sent2[-1] = sent2[-1].strip(".!?")
    # ed_score, backtrace = sentence_edit_distance_score(sent1, sent2)
    # print(f"ED_score: {ed_score}")
    # Note that we only have to print the alignment for the top 10 sentences
    # Hence, all backtraces need to be saved, and not printed automatically by
    #   the sentence_edit_distance_score function
    # print_alignment(backtrace, sent1, sent2, substitution_cost=1)

    # Debugging Translation Memory Retrieval
    retrievalType = ""
    while retrievalType != "PM" and retrievalType != "ED":
        retrievalType = input("Type memory retrieval metric [PM|ED]: ")
    translation_memory_retrieval(retrievalType)
