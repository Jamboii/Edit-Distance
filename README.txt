CSC470 Natural Language Processing- Project 3
Edit Distance and Translation Memory Retrieval Systems
Alexander Bensutti, Ethan Kochis, Thomas Westra


README File


Running our program:

From a Mac in STEM112:

Run 'python3 edit_distance.py <word1> <word2>' to run program for T1 and T2.
It will output the cost and the alignment of editing word1 to word2.

Run 'python3 translation_memory_retrieval.py' to run program for T3, T4, and T5.
Perform translation memory retrieval on the EMEA parallel corpus by selecting one of two retrieval metrics, Percent Match (PM) or Edit Distance Score (ED). It will output 10000 randomly selected candidate sentences from the corpus to the Translation Memory Bank (TMB.txt), 5 randomly selected sentences to the Material To Be Translated (MTBT.txt), and the top 10 candidates for each MTBT sentence based on specified retrieval score.
It will ask you to input a retrieval metric, either ED or PM. It will then place all output to a file named "Top10Candidates%s.txt" where %s is replaced by the inputted memory retrieval metric.
Note: This program assumes that the corpus is found in the "en-fr" folder as downloaded from EMEA.


Individual File Description:

README.txt -> This README file.

edit_distance.py -> Python source file containing code for T1 and T2.

translation_memory_retrieval.py -> Python source file containing code for T3 and T4 that uses the base established in edit_distance.py and runs the experiments in T5.

TMB.txt -> Set of 10000 candidate sentences from EMEA parallel corpus selected for translation memory bank.

MTBT.txt -> Set of 5 sentences from EMEA parallel corpus of Material To Be Translated.

Top10CandidatesED.txt -> Top 10 candidate sentences from TMB for each MTBT using the Edit Distance Score retrieval metric.

Top10CandidatesPM.txt -> Top 10 candidate sentences from TMB for each MTBT using the Percent Match retrieval metric.

D3.txt -> Analysis as described in T6.

report.txt -> Responses to the questions as described in D4.

en-fr folder -> The downloaded EMEA en-fr corpus.
    EMEA.en-fr.en -> English-side sentences
    EMEA.en-fr.ft -> French-side sentences
    README -> README file that comes with the downloaded dataset






