import random
import csv


def main():
    print("Save .csv files from previous runs before running it again!")
    starting_weights = {'A': 1, 'B': 1, "A'": 0, "B'": 0}
    for key in starting_weights:
        starting_weights[key] = int(input(f"weight of {key}? "))
    mut_chance = float(input("mutation chance? "))
    n = int(input("population size? "))
    gen_count = int(input("how many generations? "))
    trial_count = int(input("how many trials? "))
    for trial in range(trial_count):
        prob_lists = {'A': [], 'B': [], "A'": [], "B'": []}
        weights = starting_weights.copy()
        for gen in range(gen_count):
            population = random.choices(list(weights), weights=list(weights.values()), k=2 * n)
            population = [i + j for i, j in
                          zip(population, random.choices(["'", ''], cum_weights=[mut_chance, 1], k=2 * n))]
            for key in weights:
                weights[key] = population.count(key)
                prob_lists[key].append(weights[key] / len(population))
        with open(f'trial{trial + 1}.csv', 'w', newline='') as csvfile:
            w = csv.writer(csvfile, delimiter=',')
            w.writerow(['probs'] + [f'gen{i}' for i in range(gen_count + 1)])
            for key, prob_list in prob_lists.items():
                w.writerow([key] + [str(starting_weights[key] / sum(starting_weights.values()))] + prob_list)


if __name__ == '__main__':
    main()
