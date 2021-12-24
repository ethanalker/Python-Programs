class Compound:
    def __init__(self, coefficient, elements, element_counts):
        self.coef = coefficient
        self.elem = elements
        self.counts = element_counts

    def formula(self):
        return ''.join(
            [str(element) + str(count if count != 1 else '') for element, count in zip(self.elem, self.counts)]
        )

    def mass(self):
        return float(sum([periodic_mass[element] * count for element, count in zip(self.elem, self.counts)]))


periodic_mass = {
    'H': 1.0079,
    'Li': 6.941,
    'Be': 9.0122,
    'B': 10.811,
    'C': 12.0107,
    'N': 14.0067,
    'O': 15.9994,
    'F': 18.9984,
    'Na': 22.9897,
    'Mg': 24.305,
    'Al': 26.9815,
    'Si': 28.0855,
    'P': 30.9738,
    'S': 32.065,
    'Cl': 35.453,
    'K': 39.0983,
    'Ca': 40.078,
    'Ti': 47.867,
    'Fe': 55.845,
    'Ni': 58.6934,
    'Co': 58.9332,
    'Cu': 63.546,
    'Zn': 65.39,
    'Br': 79.904,
    'Rb': 85.4678,
    'Sr': 87.62,
    'Ag': 107.8682,
    'I': 126.9045,
    'Cs': 132.9055,
    'Ba': 137.327,
    'Au': 196.9665,
    'Hg': 200.59,
    'Pb': 207.2,
    'U': 238.0289,
}


def reaction_in():
    input_reactants = input("Balanced reactants? \n").replace(' ', '').split('+')
    input_compounds = input_reactants + input("Balanced products? \n").replace(' ', '').split('+')
    return input_compounds, len(input_reactants)


def format_compounds(raw):
    compound_list = []
    for compound in raw:
        coef = str()
        elem = []
        counts = []

        if not(compound[0].isdigit()):
            coef = 1
        else:
            while compound[0].isdigit():
                coef += str(compound[0])
                compound = compound[1:]
        coef = int(coef)

        last_char = '1'
        for char in compound:
            if char.isupper():
                if not(last_char.isdigit()):
                    counts.append(1)
                elem.append(char)
            elif char.islower():
                elem[-1] += char
            elif char.isdigit():
                if last_char.isdigit():
                    counts[-1] += char
                else:
                    counts.append(char)
            last_char = char
        if not (last_char.isdigit()):
            counts.append(1)
        counts = [int(count) for count in counts]
        compound_list.append(Compound(coef, elem, counts))
    return compound_list


def reaction_out(compound_list, len_react):
    reaction = ''
    for i, compound in enumerate(compound_list):
        reaction += str(compound.coef if compound.coef != 1 else '') + compound.formula()
        if i + 1 == len_react:
            reaction += ' -> '
        else:
            reaction += ' + '
    reaction = reaction[:-3]
    return reaction


def get_known_compound(compound_list):
    raw_known = input('Known compound? \n').replace(' ', '')
    formula_list = [molecule.formula() for molecule in compound_list]
    known_compound = Compound(0, [], [])
    if raw_known in formula_list:
        known_compound = compound_list[formula_list.index(raw_known)]
        print('Compound {} Identified \n'.format(known_compound.formula()))
    else:
        print("Failed to identify compound")
        exit()
    known_amount = input('Known amount? (include unit mol or g) \n').replace(' ', '').lower()
    if known_amount[-1] == 'g':
        known_mol = float(known_amount[:-1]) / known_compound.mass()
    elif known_amount[-3:] == 'mol':
        known_mol = float(known_amount[:-3])
    else:
        known_mol = 0
        print('Unknown unit')
        exit()
    return known_compound, known_mol


def return_reaction_data(compound_list, known_compound, known_mol):
    for molecule in compound_list:
        unknown_mol = float(known_mol) * float(molecule.coef) / float(known_compound.coef)
        print(str(round(unknown_mol, 6)) + 'mol ' + molecule.formula())
        print(str(round(unknown_mol * molecule.mass(), 6)) + 'g ' + molecule.formula())


def main():
    raw_compounds, react_len = reaction_in()
    comp_list = format_compounds(raw_compounds)
    print('Reaction: {} \n'.format(reaction_out(comp_list, react_len)))
    return_reaction_data(comp_list, *get_known_compound(comp_list))


main()
