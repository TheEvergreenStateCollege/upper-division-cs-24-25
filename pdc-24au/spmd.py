from mpi4py import MPI

def main():
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()            #number of the process running the code
    numProcesses = comm.Get_size()  #total number of processes running
    myHostName = MPI.Get_processor_name()  #machine name running the code

    print("Greetings from process {} of {} on {}"\
    .format(id, numProcesses, myHostName))

########## Run the main function
main()
