from problemState import State, Vehicle, Package
from searchNode import SearchNode
import copy

class Problem():
    """ Problem Class """
    m = None
    n = None
    k = None
    y = None
    initState = None

    def __init__(self, _m, _n, _k, _y, packs):
        """
        Initializes a problem.
        :param _m: number of vehicles.
        :param _n: number of packages.
        :param _k: capacity of each vehicle.
        :param _y: dimension of the space.
        """
        self.m = _m
        self.n = _n
        self.k = _k
        self.y = _y
        vehicles = {}
        packages = {}
        for i in range(_m):
            vehicles[i] = Vehicle(tuple([0 for i in range(_y)]), i, _k)
        for j in range(len(packs)):
            packages[j] = Package(packs[j][0], packs[j][1], j)
        self.initState = State(vehicles, packages)

    def getInitState(self):
        """
        Return current state.
        :return: state.
        """
        return SearchNode(self.initState, None)

    def readProblem():
        """
        Reads a problem from standard input.
        Input format: <m>
                      <n>
                      <k>
                      <y>
                      s11 s12 s13 ... s1y | d11 d12 d13 ... d1y
                      s21 s22 s23 ... s2y | d21 d22 d23 ... d2y
                      ...
                      ...
                      sn1 sn2 sn3 ... sny | dn1 dn2 dn3 ... dny
        """
        m = int(input())
        n = int(input())
        k = int(input())
        y = int(input())
        packages = []
        for i in range(n):
            interm = list(map(int,input().strip().split(' ')))
            src = tuple(interm[0:int(len(interm)/2)])
            des =  tuple(interm[int(len(interm)/2):len(interm)])
            packages.append((src, des))

        return Problem(m, n, k, y, packages)

    def successors(self, node):
        """
        Set of possible transitions from the current state.
        :return: list of all possible states.
        """

        possibleSuccessors = []
        for k1, v in node.getState().getVehicles().items():
            print("SUCCESSOR ON VEHICLE: ", v.getIndex(), " AT" , v.getPosition())
            for k2, p in node.getState().getPackages().items():

                # Vehicle is not carrying this package and it has no more room:
                if p.getPosition() != v.getPosition() and v.getRoom() <= 0:
                    print("VEHICLE: ", v.getIndex(), " NO ROOM, SKIPPED!")
                    # it can neither pickup this package nor deliver it:
                    continue

                # First, cover the case when you can deliver something
                # For each package picked up by/moving with v:
                else:
                    # Generate a new state:
                    newState = copy.deepcopy(node.getState())

                    if p.getPosition() == v.getPosition():
                        # Change copied state to reflect a delivery:
                        # Increase distance travelled for vehicle:
                        currVehicle = newState.getVehicles()[v.getIndex()]
                        # Moving to destination:

                        print("---VEHICLE: ", v.getIndex(), " DELIVERS"\
                                " PACKAGE: ", p.getPosition(), "\n")

                        currVehicle.setPosition(p.getDestination())
                        # Decrease room in vehicle because of the new package:
                        currVehicle.setRoom(v.getRoom() + 1)
                        # a delivered package is no longer under consideration:
                        newState.getPackages().pop(p.getIndex()) # removed
                        # Append to list of possible states:
                        possibleSuccessors.append(SearchNode(newState, node))

                    # If the vehicle can pick up more packages:
                    elif (v.getRoom() > 0) and (p.isCarried() is False):
                        # Change copied state to reflect a pick up of package p by v
                        currVehicle = newState.getVehicles()[v.getIndex()]
                        # Now move the vehicle to the position of the package
                        currVehicle.setPosition(p.getPosition())

                        print("VEHICLE: ", currVehicle.getIndex(),\
                                " PICKS UP MORE: ", p.getPosition())

                        # Adjust the room available for the vehicle
                        currVehicle.setRoom(v.getRoom() - 1)
                        # Set package as carried
                        newState.getPackages()[p.getIndex()].setCarried(v.getIndex())

                        # Append to the list of possible states:
                        possibleSuccessors.append(SearchNode(newState, node))

            # Vehicle is empty, an option is to go back to origin:
            if v.getRoom() == self.k\
                    and v.getPosition() != tuple([0 for x in range(self.y)]):
                # Make a deep copy of the state

                print("VEHICLE: ", v.getPosition(), " MOVES TO ORIGIN")

                newState = copy.deepcopy(node.getState())
                # Define origin
                garage = tuple([0 for x in range(self.y)])
                currVehicle = newState.getVehicles()[v.getIndex()]
                # Move the vehicle to the origin
                currVehicle.setPosition(garage)
                # Append state to the possible successor
                possibleSuccessors.append(SearchNode(newState, node))

        return possibleSuccessors

    def isGoal(self, state):
        """
        Returns whether the given state is the goal state.
        :param state: a State.
        :return: true if goal state, false otherwise.
        """
        origin = tuple([0 for i in range(self.y)])
        for k, v in state.getVehicles().items():
            if v.getPosition() != origin:
                return False
        if state.getPackages() != {}:
            return False
        return True

    def __str__(self):
        """  String representation of Problem """
        return "(M, N, K, Y) := " + str((self.m, self.n, self.k, self.y)) +\
            "\n" + "Current State:\n" + str(self.initState)

    def getValues(self):
        """ String representation of the current values used """
        return("(M, N, K, Y) := " + str((self.m, self.n, self.k, self.y)))
