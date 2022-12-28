from ortools.sat.python import cp_model
def main():
    costs = [
        [90, 76, 75, 70],
        [35, 85, 55, 65],
        [125, 95, 90, 105],
        [45, 110, 95, 115],
        [60, 105, 80, 75],
        [45, 65, 110, 95],
    ]
    num_workers = len(costs)
    num_tasks = len(costs[0])
    team1 = [0, 2, 4]
    team2 = [1, 3, 5]
    team_max = 2
    model = cp_model.CpModel()
    x = {}
    for worker in range(num_workers):
        for task in range(num_tasks):
            x[worker, task] = model.NewBoolVar(f'x[{worker},{task}]')
    for worker in range(num_workers):
        model.AddAtMostOne(x[worker, task] for task in range(num_tasks))
    for task in range(num_tasks):
        model.AddExactlyOne(x[worker, task] for worker in range(num_workers))
    team1_tasks = []
    for worker in team1:
        for task in range(num_tasks):
            team1_tasks.append(x[worker, task])
    model.Add(sum(team1_tasks) <= team_max)

    team2_tasks = []
    for worker in team2:
        for task in range(num_tasks):
            team2_tasks.append(x[worker, task])
    model.Add(sum(team2_tasks) <= team_max)
    objective_terms = []
    for worker in range(num_workers):
        for task in range(num_tasks):
            objective_terms.append(costs[worker][task] * x[worker, task])
    model.Minimize(sum(objective_terms))
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Total cost = {solver.ObjectiveValue()}\n')
        for worker in range(num_workers):
            for task in range(num_tasks):
                if solver.BooleanValue(x[worker, task]):
                    print(f'Worker {worker} assigned to task {task}.' +
                          f' Cost = {costs[worker][task]}')
    else:
        print('No solution found.')


if __name__ == '__main__':
    main()