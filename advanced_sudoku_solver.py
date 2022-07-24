digits = '123456789'
rows = 'ABCDEFGHI'
def cross(rows, columns):
    return [a+b for a in rows for b in columns]
squares = cross(rows, digits)
unit_list = ([cross(row, digits) for row in rows] +
             [cross(rows, digit) for digit in digits] +
             [cross(row, digit) for row in ['ABC', 'DEF', 'GHI'] for digit in ['123', '456', '789']])
units = dict((s, [u for u in unit_list if s in u]) for s in squares)
peers = dict((s, set(sum(units[s], []))- set([s])) for s in squares)

def parse_grid(grid):
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign_values(values, s, d):
            return False
    return values

def grid_values(grid):
    vals = [str(v) for unit in grid for v in unit if str(v) in digits or v == 0]
    return dict(zip(squares, vals))

def assign_values(values, s, d):
    other_vals = values[s].replace(d, '')
    if all(eliminate(values, s, d1) for d1 in other_vals):
        return values
    return False

def eliminate(values, s, d):
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d, '')
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        if not all(eliminate(values, s1, values[s]) for s1 in peers[s]):
            return False
    elif len(values[s]) == 2:
        twin = [place for place in units[s][-1] if values[place] == values[s]]
        if len(twin) == 2:
            s1, s2 = twin[0], twin[1]
            if s1[0] == s2[0]:
                others = set(units[s][0]) - set([s1]) - set([s2])
                if not all(eliminate(values, s3, d1) for s3 in others for d1 in values[s]):
                    return False
            elif s1[1] == s2[1]:
                others = set(units[s][1]) - set([s1]) - set([s2])
                if not all(eliminate(values, s3, d1) for s3 in others for d1 in values[s]):
                    return False

    for u in units[s]:
        d_places = [s for s in u if d in values[s]]
        if len(d_places) == 0:
            return False
        elif len(d_places) == 1:
            if not assign_values(values, d_places[0], d):
                return False
    return values

def display(values):
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print (''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in digits))
        if r in 'CF': print(line)

def get_arr(values):
    return [[sum(list(map(lambda x: int(x), values[r+c]))) for c in digits] for r in rows]

def solve(grid): return search(parse_grid(grid))

def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign_values(values.copy(), s, d))
		for d in values[s])

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False



