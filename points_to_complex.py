import simpcells as sc
import tuple as tup
import numpy as np  # for square and square root


class point:
    """Points in the real dimensional space.

    Notes:
        We want to save points as lists and do it as object for the same reason
        as for tuple.

    Args:
        list(list): List of values representing a point in a finite dimensional
            real vecotr space.

    Attributes:
        coordinates(list): Coordinates of the point in form of a list.
        dimension(int): Dimension des Punktes.
    """

    def __init__(self, list):
        self.coordinates = list
        self.dimension = len(list)

    def distance(self, other_point):
        """Distance to another point."""
        x = 0
        for i in range(self.dimension):
            x = x + np.square(self.coordinates[i] - other_point.coordinates[i])
        return np.sqrt(x)

    def add(self, other_point):
        """Return the sum of the point and the other point."""
        list = []
        for i in range(self.dimension):
            list.append(self.coordinates[i] + other_point.coordinates[i])
        p = point(list)
        return p

    def scalarmult(self, scalar):
        """Return the multiplication with a scalar."""
        list = []
        for i in range(self.dimension):
            list.append(scalar * self.coordinates[i])
        p = point(list)
        return p

    def absolute_value(self):
        """Compute the absolute value of the point."""
        x = 0
        for i in range(self.dimension):
            x = x + np.square(self.coordinates[i])
        return np.sqrt(x)

    def __eq__(self, other_point):
        """Decide whether two points coincide by =."""
        if self.dimension != other_point.dimension:
            return False
        token = True
        for i in range(self.dimension):
            if self.coordinates[i] != other_point.coordinates[i]:
                token = False
        return token

    def __repr__(self):
        """Return the string of a point."""
        return str(self.coordinates)

    def __getitem__(self, ii):
        """Get a coordinate."""
        return self.coordinates[ii]


def points_to_cells_VR(list_of_points, max_radius):
    """Compute the Vietoris Rips complex for a list of points.

    Args:
        list_of_points(list): List of all points.
        max_radius: prescribed radius for the construction.

    Returns:
        list: List of cells already ordered in the right way.
    """

    list_of_cells = []  # list of all cells
    list_of_cells_by_len = [[]]  # store by dimension of cells
    index_list = [[]]  # queue of lists of indices
    number_of_points = len(list_of_points)

    printindex = 0

    while len(index_list) != 0:  # while there are lists in the queue
        last_index = index_list.pop(0)  # take the last element
        max_last_index = max(last_index) if len(last_index) != 0 else -1
        for i in range(max_last_index+1, number_of_points):
            indices = last_index + [i]  # create new list of indices
            # create tuple of points for this list of indices:
            list_some_points = []
            for i in indices:
                list_some_points.append(list_of_points[i])
            tuple_some_points = tup.tuple(list_some_points)
            # compute boundary:
            boundary_some_points = []
            for i in indices:  # loop over all elements in the boundary
                new_boundary = []
                for j in indices:
                    if i != j:
                        new_boundary.append(list_of_points[j])
                new_boundary_tuple = tup.tuple(new_boundary)
                # search for cells in right dimension:
                for c in list_of_cells_by_len[len(new_boundary_tuple.tuple)-1]:
                    if c.name == new_boundary_tuple:
                        boundary_some_points.append(c)  # append boundary
            # create a cell using the tuple as name and the computed boundary:
            new_cell = sc.cell(tuple_some_points, boundary_some_points)
            # add dimension:
            new_cell.dimension = len(indices)-1
            # add order to the cell:
            new_cell_distance = 0
            for k1 in range(len(indices)):
                for k2 in range(k1+1, len(indices)):
                    dist = tuple_some_points.tuple[k1].distance(
                        tuple_some_points.tuple[k2])
                    if dist > new_cell_distance:
                        new_cell_distance = dist
            new_cell.order = new_cell_distance/2
            # add cell to the list if it does not exceed the maximal radius
            if new_cell_distance/2 <= max_radius:
                list_of_cells.append(new_cell)  # add to cell list
                index_list.append(indices)  # add list of indices to queue
                if len(new_cell.name.tuple)-1 >= len(list_of_cells_by_len):
                    list_of_cells_by_len.append([])
                list_of_cells_by_len[len(new_cell.name.tuple)-1].append(new_cell)
        if printindex % 100 == 0:
            print(printindex)
        printindex += 1
    # At this point the cells are ordered by dimension. We order them at first
    # by their order and then by their dimension.
    list_of_cells = sort_by_order(list_of_cells)

    return list_of_cells


def sort_by_order(list_of_cells):
    """Sort a list of cells at first by order and then by their dimension.

    Notes:
        The algorithm just sorts the elements that are not already ordered.
        Therefore, if the list is ordered before by dimension, then after this
        procedure it is ordered at first by the order of the cells and then by
        their dimension.

    Args:
        list_of_cells(list): A list of cells which we want to order.

    Returns:
        list: A new list containing all cells of list_of_cells but ordered by
        their order.
    """
    new_list_of_cells = []
    for c in list_of_cells:
        i = len(new_list_of_cells)  # we begin searchin on the right side
        while True:
            # if we arrive at 0, we add the cell there:
            if i == 0:
                new_list_of_cells.insert(i, c)
                break
            # if the order of the next one is still higher, we go one step
            elif new_list_of_cells[i-1].order > c.order:
                i = i-1
            # insert cell if the next one has at most the same order
            else:
                new_list_of_cells.insert(i, c)
                break

    return new_list_of_cells


def points_to_cells_Cech(list_of_points, max_radius, precision=0.01):
    """Compute the Cech complex for a list of points.

    Notes:
        This algorithm can just be used for points in two dimensional space
        since the function verification_for_cech() is just implemented for
        two dimensions.

    Args:
        list_of_points(list): List of all points.
        max_radius: prescribed radius for the construction.
        precision(float, optional): The value by which we enlarge the radius in
            each step.

    Returns:
        list: List of cells already ordered in the right way.
    """

    '''
    ACHTUNG: wir muessen draw_barcode mit einer tolerance benutzen, damit nicht
    jeder kleine strich angezeigt wird, der von den vielleicht nicht ganz
    genauen punkten stammt.
    '''
    # compute cells by Vietoris-Rips:
    cell_list = points_to_cells_VR(list_of_points, max_radius)

    # enlarge the radius for each cell until it satisfies the property for Cech
    radius = 0
    for c in cell_list:
        radius = c.order  # start with radius from VR
        while True:
            if verification_for_cech(c.name.tuple, radius):  # check
                c.order = radius  # set order
                break
            else:
                radius = radius + precision

    # order cells:
    cell_list = sort_by_order(cell_list)

    return cell_list


def verification_for_cech(candidate_points, radius):
    """Check whether all balls with presribed radius at the points intersect.

    Args:
        candidate_points(list): List of the points.
        radius(float): Radius of the balls.

    Returns:
        boolean: True if all balls at the points intersect.
    """
    # create list of all pairwise intersection points:
    intersection_points = []
    h = len(candidate_points)
    for i in range(h):
        for j in range(i+1, h):
            c1 = candidate_points[i]
            c2 = candidate_points[j]
            for k in intersection(c1, c2, radius):
                intersection_points.append([i, j, k])

    # if there are less then two balls then they all intersect:
    if h < 2:
        return True

    # check whether one intersection point is in all balls:
    veri = False
    for inter in intersection_points:
        # Note that inter[0] and inter[1] are indices of the points of the
        # center of the balls and inter[2] is one of their intersection points.
        veri = True
        for k in range(h):
            if k != inter[0] and k != inter[1]:
                point_in_all_balls = True
                for p in candidate_points:
                    if p.distance(inter[2]) > radius:
                        point_in_all_balls = False
                if not point_in_all_balls:
                    veri = False
                    break
        if veri:
            break
    return veri


def intersection(p1, p2, radius):
    """Compute the intersection of two balls.

    Args:
        p1,p2(point): Centers of the balls.
        radius(float): Radius of the balls.

    Returns:
        boolean: True if all balls at the points intersect.
    """
    # no intersection if their radius is smaller than 1/2 of their distance:
    distance = p1.distance(p2)
    if radius < distance/2.0:
        return []

    # compute intersection points:
    vector_p1_to_p2 = p2.add(p1.scalarmult(-1))
    center = p1.add(vector_p1_to_p2.scalarmult(0.5))
    ortho = orthonormal(vector_p1_to_p2)
    h = np.sqrt(np.square(radius) - np.square(distance/2.0))
    if h == 0:
        intersectionlist = [center]
    else:
        intersectionlist = []
        intersectionlist.append(center.add(ortho.scalarmult(h)))
        intersectionlist.append(center.add(ortho.scalarmult(-h)))

    return intersectionlist


def orthonormal(p):
    """Compute orthonormal vector.

    Notes:
        This function works only for two dimensions.

    Args:
        p(point): A vector of dimension 2.

    Returns:
        point: A vector which is orthonormal to p.
    """
    orthogonal = point([p.coordinates[1], -1 * p.coordinates[0]])
    orthonormal = orthogonal.scalarmult(1/orthogonal.absolute_value())

    return orthonormal
