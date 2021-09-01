import multiprocessing as mp
from threading import Thread
import threading
import time


#-----------------------------------------------------------------------------
 # SOURCE FILE:    assn1-thread.py
 #
 # PROGRAM:        assn1-thread.py
 #
 # FUNCTIONS:      int[] factors(nr)
 #                 void workerfunction(i, endnum, lockindex, lockprint)
 #                 void main()
 #
 # DATE:           January 22, 2021
 #
 # REVISIONS:      N/A
 #
 # DESIGNER:       Kevin Lo
 #
 # PROGRAMMER:     Kevin Lo
 #
 # NOTES:
 # This is a program that tests the speed of using threads to compute a function multiple times
# --------------------------------------------------------------------------


#--------------------------------------------------------------------------
 # FUNCTION:       factors
 #
 # REVISIONS:      N/A (Date and explanation of revisions if applicable)
 #
 # INTERFACE:      int[] factors(int nr)
 #                 int nr: the number to get the prime factorization of
 #
 # RETURNS:        int[]
 #
 # NOTES:
 # prime factor function as to use as a load from
 # https://stackoverflow.com/questions/43129076/prime-factorization-of-a-number
 # -----------------------------------------------------------------------
def factors(nr):
    i = 2
    factors = []
    while i <= nr:
        if (nr % i) == 0:
            factors.append(i)
            nr = nr / i
        else:
            i = i + 1
    return factors

lockindex = threading.Lock()
lockprint = threading.Lock()
#--------------------------------------------------------------------------
 # FUNCTION:       factors
 #
 # DATE:           January 22, 2021
 #
 # REVISIONS:      N/A (Date and explanation of revisions if applicable)
 #
 # INTERFACE:      void workerfunction(int i, int endnum)
 #                      int[] i: the current index
 #                      int endnum: the last number it needs to compute
 #
 # RETURNS:        void
 #
 # NOTES:
 # The child thread that will calculate the prime factorization of the numbers
 # -----------------------------------------------------------------------
def workerfunction(i,endnum):

    currentnum = 0
    while(i[0] <= endnum):
        start = time.perf_counter()
        with lockindex:
            currentnum = i[0]
            i[0] = i[0] + 1

        factorization = factors(currentnum)
        end = time.perf_counter()
        exectime = end-start
        stroutput = str(currentnum) + " ID:" + str(threading.get_ident()) + " Time:" + str(exectime) + " " + str(factorization)

        with lockprint:
            print(stroutput)
            filewrite = open("threadlog.txt", "a")
            filewrite.write(stroutput + '\n')
            filewrite.close()

#--------------------------------------------------------------------------
 # FUNCTION:       main
 #
 # DATE:           January 22, 2021
 #
 # REVISIONS:      N/A (Date and explanation of revisions if applicable)
 #
 # INTERFACE:      void main()
 #
 # RETURNS:        void
 #
 # NOTES:
 # The parent thread running the program
 # -----------------------------------------------------------------------
def main():
    workercount = int(input("Enter number of workers:"))
    endnum = int(input("Enter the end number to prime factorize:"))
    filewrite = open("threadlog.txt", "w")
    filewrite.close()

    index = [2]
    workers = []

    start1 = time.perf_counter()
    for n in range(workercount):
        #print(n)
        w = Thread(target=workerfunction, args=(index,endnum))
        w.start()
        workers.append(w)
    for w in workers:
        w.join()
    end1 = time.perf_counter()
    exectime1 = end1-start1

    filewrite = open("threadlog.txt", "a")
    print("Time Elapsed:", exectime1)
    filewrite.write("Time elapsed" + str(exectime1) + '\n')
    filewrite.close()

main()
