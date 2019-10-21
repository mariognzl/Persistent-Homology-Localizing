import simpcells as sc
import tuple as tup


def construct_mv_blowup(cell_list, cover):
    """Construct the Mayer-Vietoris blowup for a given cover.

    Args:
        cell_list(list): A list of cells describing the simplicial complex.
        cover(list): A list of cell lists, describing the cover by
            subcomplexes.

    Returns:
        list: A new list of cells describing the complex of the Mayer-Vietoris
            blowup.
    """
    n = len(cover)  # number of subcomplexes in the cover
    new_cell_list = []

    # compute generators for the blowup and safe them as pairs:
    for i in range(n):  # consider i-th intersections
        for l in tup.all_indices(i+1, n):  # J from the end of Chapter 5
            l_cover = []
            for j in l:
                l_cover.append(cover[j])
            inter = intersection(l_cover)  # compute intersection
            for c in inter:  # sigma from the end of Chapter 5
                # create cell for the pair (sigma, J):
                new_cell = sc.cell(tup.tuple([c, tup.tuple(l)]), [])
                new_cell_list.append(new_cell)  # append cell to new_cell_list

    # sort by #J and then by dim(sigma):
    new_cell_list = sort_for_loc(new_cell_list)

    # compute and set boundary
    for c in new_cell_list:
        boundary_list = []
        sigma = c.name.tuple[0]
        # the part where we take the boundary of sigma:
        J = c.name.tuple[1]
        for b in sigma.boundary:
            # search for boundary in new_cell_list:
            for i in new_cell_list:
                if i.name.tuple[0] == b and i.name.tuple[1] == J:
                    boundary_list.append(i)
                    break
        # the part where we take the boundary of J
        if len(J.tuple) > 1:  # otherwise the boundary forms no cell
            for j in range(len(J.tuple)):
                new_J = J.without(j)
                for i in new_cell_list:
                    if i.name.tuple[0] == sigma and i.name.tuple[1] == new_J:
                        boundary_list.append(i)
                        break
        # store the boundary list in the cell
        c.boundary = boundary_list

    # set dimension
    for c in new_cell_list:
        d = c.name.tuple[0].dimension + len(c.name.tuple[1].tuple)-1
        c.dimension = d

    # set order
    for c in new_cell_list:
        o = len(c.name.tuple[1].tuple)-1
        c.order = o

    return new_cell_list


def intersection(list_of_lists):
    """Compute the intersection of several lists.

    Args:
        list_of_lists(list): A list, which contains all lists, that we want to
            intersect.

    Returns:
        list: The intersection of all lists in list_of_lists.
    """
    new_list = []
    # take elements in the first list:
    for i in list_of_lists[0]:
        token = True
        # check if they are in all other lists:
        for l in list_of_lists[1:]:
            if i not in l:
                token = False
                break
        # if they are in all other lists, add them to the intersection:
        if token:
            new_list.append(i)
    return new_list


def sort_for_loc(list_of_cells):
    """Sort the list for the Mayer-Viertoris blowup."""
    new_list_of_cells = sort_by_dimension_of_sigma(list_of_cells)
    new_list_of_cells = sort_by_len_of_J(new_list_of_cells)
    return new_list_of_cells


def sort_by_dimension_of_sigma(list_of_cells):
    """Sort the list for the Mayer-Viertoris blowup by dimension of sigma."""
    # insertion sort
    new_list_of_cells = []
    for c in list_of_cells:
        i = len(new_list_of_cells)
        token = True
        while token:
            if i == 0:
                new_list_of_cells.insert(i, c)
                token = False
            elif (new_list_of_cells[i-1].name.tuple[0].dimension
                  > c.name.tuple[0].dimension):
                i = i-1
            else:
                new_list_of_cells.insert(i, c)
                token = False

    return new_list_of_cells


def sort_by_len_of_J(list_of_cells):
    """Sort the list for the Mayer-Viertoris blowup by length of J."""
    # insertion sort
    new_list_of_cells = []
    for c in list_of_cells:
        i = len(new_list_of_cells)
        token = True
        while token:
            if i == 0:
                new_list_of_cells.insert(i, c)
                token = False
            elif (len(new_list_of_cells[i-1].name.tuple[1].tuple)
                  > len(c.name.tuple[1].tuple)):
                i = i-1
            else:
                new_list_of_cells.insert(i, c)
                token = False

    return new_list_of_cells
