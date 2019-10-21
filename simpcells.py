

class cell:
    """Simplicial cells.

    Args:
        name: Name of the cell.
        boundary(list): The boundary cells.

    Attributes:
        name: Name of the cell.
        boundary(list): List of boundary cells.
        partner: Partner cell.
        basisel: Corresponding basis element.
        order: Order of the cell.
        dimension: Dimension of the cell.
        index: Index of the cell in the filtration.
    """

    def __init__(self, name, boundary):
        self.name = name
        self.boundary = boundary
        self.partner = None
        self.basisel = [self, ]
        self.order = None
        self.dimension = None
        self.index = None

    def __repr__(self):
        """Return the string of a cell."""
        # return 'name: '+str(self.name) + ', boundary: '+str(self.boundary)
        return str(self.name)


def boundary(list):
    """Computes the boundary of a chain.

    Args:
        list(list): A list of cells representing a chain in F2.

    Returns:
        list: A list of cells representing the boundary in F2.
    """
    boundary_list = []
    for k in list:
        for j in k.boundary:
            if j in boundary_list:
                boundary_list.remove(j)
            else:
                boundary_list.append(j)
    return boundary_list


def add_chains(A, B):
    """Addition of two chains in F2.

    Args:
        A(list): List of cells.
        B(list): list of cells.

    Returns:
        list: The addition of A and B.
    """
    C = A.copy()
    for b in B:
        if b in C:
            C.remove(b)
        else:
            C.append(b)
    return C
