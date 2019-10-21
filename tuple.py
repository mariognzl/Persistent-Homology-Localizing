

class tuple:
    """A general tuple.

    Notes:
        If their entries coincide, they should be equal. If we just compare
        lists itself in python, they do not coincide in general if their
        entries coincide.

    Args:
        list_of_points(list): A list of points representing a tuple.

    Attributes:
        tuple(list): The tuple
    """

    def __init__(self, list):
        self.tuple = list

    def without(self, number):
        """Returns a new tuple without item with index 'number'."""
        t = self.tuple[:number]+self.tuple[number+1:]
        return tuple(t)

    def __eq__(self, other):
        """Decide whether two points coincide by =."""
        if len(self.tuple) != len(other.tuple):
            return False
        token = True
        for i in range(len(self.tuple)):
            if self.tuple[i] != other.tuple[i]:
                token = False
        return token

    def __repr__(self):
        """Return the string of a tuple."""
        return str(self.tuple)

    def __getitem__(self, ii):
        """Get a list item."""
        return self.tuple[ii]


def all_indices(k, m):
    """Yield all ordered lists of length k with pairwise different entries
        in {0,...,m-1} .

    Notes:
        Yield is used in this function. It behaves like return but it returns a
        generator over which we can iterate.

    Args:
        k(int): Number of entries in the sublists we want to generate.
        m(int): Length of the list that we want to choose from.
    """

    # yield the first sublist:
    liste = []
    for i in range(k):
        liste.append(i)
    yield liste

    # function to modify the sublist:
    def moveentry(j, list):
        # if no element in the sublist can be changed return the empty list
        if j == -1:
            return []
        # increase the j-th element and minimize all following entries
        if list[j]+1 < m and list[j]+1 not in list:
            new_list = list[:j]
            for i in range(len(list)-len(new_list)):
                new_list.append(list[j]+1+i)
            return new_list
        # if the j-th entry can not be increased, try the (j-1)-th
        else:
            return moveentry(j-1, list)

    # yield a sublist and change change it by the function from above:
    while True:
        liste = moveentry(len(liste)-1, liste)
        if liste == []:  # quit if the list can not be changed anymore
            break
        else:
            yield liste
