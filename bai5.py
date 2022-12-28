import numpy as np
from ortools.graph.python import linear_sum_assignment
def main():
    """Linear Sum Assignment example."""
    assignment = linear_sum_assignment.SimpleLinearSumAssignment()

    costs = np.array([
        [90, 76, 75, 70],
        [35, 85, 55, 65],
        [125, 95, 90, 105],
        [45, 110, 95, 115],
    ])
    end_nodes_unraveled, start_nodes_unraveled = np.meshgrid(
        np.arange(costs.shape[1]), np.arange(costs.shape[0]))
    start_nodes = start_nodes_unraveled.ravel()
    end_nodes = end_nodes_unraveled.ravel()
    arc_costs = costs.ravel()

    assignment.add_arcs_with_cost(start_nodes, end_nodes, arc_costs)

    status = assignment.solve()

    if status == assignment.OPTIMAL:
        print(f'Total cost = {assignment.optimal_cost()}\n')
        for i in range(0, assignment.num_nodes()):
            print(f'Worker {i} assigned to task {assignment.right_mate(i)}.' +
                  f'  Cost = {assignment.assignment_cost(i)}')
    elif status == assignment.INFEASIBLE:
        print('No assignment is possible.')
    elif status == assignment.POSSIBLE_OVERFLOW:
        print(
            'Some input costs are too large and may cause an integer overflow.')

if __name__ == '__main__':
    main()