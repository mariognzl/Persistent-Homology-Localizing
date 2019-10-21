import simpcells as sc


def change_basis(K):
    """Algorithm 1.

    Args:
        K(list): List of cells representing the filtration.
    """
    i = 0  # number of iteration
    for k in K:
        # STEP 1
        while True:
            boundary_of_basisel = sc.boundary(k.basisel)  # compute boundary
            if len(boundary_of_basisel) == 0:
                break
            else:
                tau = youngest(boundary_of_basisel)
                if tau.partner is None:
                    assign_partner(tau, k)
                    break
                else:
                    k.basisel = sc.add_chains(k.basisel, tau.partner.basisel)
        # STEP 2
        partner = k.partner  # For better readability
        if partner is not None:
            eliminate = sc.add_chains(partner.basisel, sc.boundary(k.basisel))
            while len(eliminate) != 0:
                tau = youngest(eliminate)
                partner.basisel = sc.add_chains(partner.basisel, tau.basisel)
                eliminate = sc.add_chains(eliminate, tau.basisel)
        # print number to track the progress for long lists:
        if i % 100 == 0:
            print(i)
        i += 1


def youngest(list_of_cells):
    """Find the youngest cell in a list of cells.

    Notes:
        Every cells needs to have an index.

    Args:
        list_of_cells(list): List of cells to search for youngest.

    Returns:
        cell: Youngest cell in list_of_cells.
    """
    min = None
    min_index = None
    for k in list_of_cells:
        if min is None:
            min = k
            min_index = k.index
        else:
            if min_index < k.index:
                min = k
                min_index = k.index
    return min


def assign_partner(cell1, cell2):
    """Algorithm 2.

    Args:
        cell1(cell): Cell to assign the other cell as partner.
        cell2(cell): Cell to assign the other cell as partner.
    """
    cell1.partner = cell2
    cell2.partner = cell1


def change_basis_without2(K):
    """Algorithm 3.

    Args:
        K(list): List of cells representing the filtration.
    """
    i = 0  # number of iteration
    for k in K:
        while True:
            boundary_of_basisel = sc.boundary(k.basisel)  # compute boundary
            if len(boundary_of_basisel) == 0:
                break
            else:
                tau = youngest(boundary_of_basisel)
                if tau.partner is None:
                    assign_partner(tau, k)
                    break
                else:
                    k.basisel = sc.add_chains(k.basisel, tau.partner.basisel)
        # print number to track the progress for long lists:
        if i % 100 == 0:
            print(i)
        i += 1


def adjust_basisel(K):
    """Algorithm 4.

    Args:
        K(list): List of cells representing the filtration.
    """
    i = 0  # number of iteration
    for k in K:
        partner = k.partner  # For better readability
        if partner is not None and partner.index > k.index:
            k.basisel = sc.boundary(partner.basisel)
        # print number to track the progress for long lists:
        if i % 100 == 0:
            print(i)
        i += 1


def compute_homology(K, step2=False):
    """Compute homology with Algorithm 3 (and Algorithm 4).

    Args:
        K(list): List of cells representing the filtration.
        step2(boolean, optional): Decide whether to execute step 2 or not.
            Defaults to False.
    """
    add_indices(K)  # Add indices to the cells in the list
    print(' -- change basis without step 2 -- ')
    change_basis_without2(K)
    if step2:
        print(' -- adjust basis elements -- ')
        adjust_basisel(K)


def add_indices(K):
    """Adds indices to the cells with resprect to the list.

    Args:
        K(list): List of all cells.
    """
    i = 0
    for k in K:
        k.index = i
        i += 1


def get_barcodes(K, max_value=None):
    """Get the barcodes of cells by partner assignment.

    Notes:
        The function compute_homology() should habe beeen used before.
        The order of each simplicial cell has to be defined.

    Args:
        K(list): List of cells.
        max_value(optional): Value that should be used as right entry of the
            interval. Defaults to None.

    Returns:
        list: List of intervals.
        list: List of corresponding generators.
    """
    max_dimension = 0
    for k in K:
        if k.dimension > max_dimension:
            max_dimension = k.dimension

    list = []
    list2 = []
    for i in range(max_dimension+1):
        list.append([i, []])
        list2.append([i, []])

    for k in K:
        if k.partner is None:
            list[k.dimension][1].append([k.order, max_value])
            list2[k.dimension][1].append(k)
        elif k.partner.order > k.order:
            list[k.dimension][1].append([k.order, k.partner.order])
            list2[k.dimension][1].append(k)

    return list, list2


def draw_barcode(list, dimension, K, max_value=None):
    """Draw a barcode.

    Notes:
        The function uses the module matplotlib.

    Args:
        list(list): List of intervals obtained from get_barcodes() that should
            be drawn.
        dimension(int): Dimension of the homology that should be drawn.
        K: List where the barcode comes from. We need this to compute the
            maximal value of the intervals to decide where to end the diagram.
        max_value(optional): Value where to cut the diagram. If this argument
            is given, K can be set to an arbitrary value like None.
    """

    if max_value is None:
        max_value = 0
        for k in K:
            if k.order > max_value:
                max_value = k.order

    if dimension > len(list)-1:
        print('no homology in this dimension')
        return

    import matplotlib.pyplot as plt

    item = list[dimension]
    print(item)
    index = 0
    fig, ax = plt.subplots()
    for interval in item[1]:
        if interval[1] is None:
            ax.arrow(interval[0], index, max_value-interval[0], 0,
                     color='black', width=0.02, head_width=0, head_length=0)
            ax.arrow(max_value, index, 0.1*max_value, 0,
                     color='r', width=0.02, head_width=0, head_length=0)
        else:
            ax.arrow(interval[0], index, interval[1]-interval[0], 0,
                     color='black', width=0.02, head_width=0, head_length=0)
        index = index + 1
    ax.set_yticks([])
    ax.set_ylim(-1, index)
    ax.set_xlim(0, max_value+1)
    plt.show()
