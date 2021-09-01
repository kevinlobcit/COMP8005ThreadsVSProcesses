from multiprocessing import Process
import multiprocessing
from multiprocessing import Value
import time
import os

#-----------------------------------------------------------------------------
 # SOURCE FILE:    assn1-process.py
 #
 # PROGRAM:        assn1-process.py
 #
 # FUNCTIONS:      int[] factors(nr)
 #                 void workerfunction(i, endnum, lockindex, lockprint)
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
 # This is a program that tests the speed of using processes to compute a function multiple times
# --------------------------------------------------------------------------


#--------------------------------------------------------------------------
 # FUNCTION:       factors
 #
 # DATE:           March 30, 2017
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

#--------------------------------------------------------------------------
 # FUNCTION:       factors
 #
 # DATE:           January 22, 2021
 #
 # REVISIONS:      N/A (Date and explanation of revisions if applicable)
 #
 # INTERFACE:      void workerfunction(int i, int endnum, lock lockindex, lock lockprint)
 #                      int i: the current index
 #                      int endnum: the last number it needs to compute
 #                      lock lockindex: lock for access to the "i" index
 #                      lock lockprint: lock for access to the print/output
 #
 # RETURNS:        void
 #
 # NOTES:
 # The child process that will calculate the prime factorization of the numbers
 # -----------------------------------------------------------------------
def workerfunction(i,endnum, lockindex,lockprint):

    currentnum = 0
    while(i.value <= endnum):
        start = time.perf_counter()
        lockindex.acquire()
        currentnum = i.value
        i.value = i.value + 1
        lockindex.release()

        factorization = factors(currentnum)
        end = time.perf_counter()
        exectime = end-start
        stroutput = str(currentnum) + " ID:" + str(os.getpid()) + " Time:" + str(exectime) + " " + str(factorization)

        lockprint.acquire()
        print(stroutput)
        filewrite = open("processlog.txt", "a")
        filewrite.write(stroutput + '\n')
        filewrite.close()
        lockprint.release()

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
 # The parent tprocecss running the program
 # -----------------------------------------------------------------------
if __name__ == "__main__":
    lockindex = multiprocessing.Lock()
    lockprint = multiprocessing.Lock()
    filewrite = open("processlog.txt", "w") #create empty file to write to
    filewrite.close()

    workercount = int(input("Enter number of workers:"))
    endnum = int(input("Enter the end number to prime factorize:"))
    #index = []
    index = Value('i', 2)
    workers = []

    start1 = time.perf_counter()
    for n in range(workercount):
        w = Process(target=workerfunction, args=(index,endnum, lockindex,lockprint))
        w.start()
        workers.append(w)
    for w in workers:
        w.join()
    end1 = time.perf_counter()
    exectime1 = end1-start1

    filewrite = open("processlog.txt", "a") #append the finishing time
    print("Time Elapsed:", exectime1)
    filewrite.write("Time elapsed" + str(exectime1) + '\n')
    filewrite.close()
