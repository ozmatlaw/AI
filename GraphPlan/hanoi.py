import sys


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    "*** YOUR CODE HERE ***"

    propositions(disks, domain_file, pegs)
    actions(disks, domain_file, pegs)
    domain_file.close()


def propositions(disks, domain_file, pegs):
    domain_file.write("Propositions:\n")
    for disk in disks:
        for peg in pegs:
            domain_file.write(disk + peg + " not_" + disk + peg + " ")
    domain_file.write("\n")


def actions(disks, domain_file, pegs):
    domain_file.write("Actions:\n")
    counter = 0
    for disk in disks:
        for peg1 in pegs:
            for peg2 in pegs:
                if peg1 != peg2:
                    domain_file.write("Name: move_" + disk + peg1 + peg2 + "\n")
                    preconditions(counter, disk, disks, domain_file, peg1, peg2)
                    add_propositions(disk, domain_file, peg1, peg2)
                    delete_propositions(disk, domain_file, peg1, peg2)
        counter += 1


def preconditions(counter, disk, disks, domain_file, peg1, peg2):
    domain_file.write("pre: " + disk + peg1 + " ")
    for j in range(counter):
        domain_file.write("not_" + disks[j] + peg1 + " ")
    for k in range(counter):
        domain_file.write("not_" + disks[k] + peg2 + " ")
    domain_file.write("\n")


def add_propositions(disk, domain_file, peg1, peg2):
    domain_file.write("add: " + disk + peg2 + " not_" + disk + peg1 + "\n")


def delete_propositions(disk, domain_file, peg1, peg2):
    domain_file.write("delete: " + disk + peg1 + " not_" + disk + peg2 + "\n")


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    "*** YOUR CODE HERE ***"

    initial_state(disks, pegs, problem_file)
    goal_state(disks, pegs, problem_file)
    problem_file.close()


def initial_state(disks, pegs, problem_file):
    problem_file.write("Initial state: ")
    for i in range(len(disks)):
        problem_file.write(disks[i] + pegs[0] + " ")
        # problem_file.write(disks[len(disks) - i - 1] + pegs[0] + " ")
        for peg_idx in range(1, len(pegs)):
            problem_file.write("not_" + disks[i] + pegs[peg_idx] + " ")

    problem_file.write("\n")


def goal_state(disks, pegs, problem_file):
    problem_file.write("Goal state: ")
    for i in range(len(disks)):
        problem_file.write(disks[i] + pegs[len(pegs) - 1] + " ")

    #     problem_file.write(disks[len(disks) - i - 1] + pegs[len(pegs) - 1] + " ")
    problem_file.write("\n")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
