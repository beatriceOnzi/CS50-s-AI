import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
        

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.domains:
            for option in self.domains[v].copy():
                if len(option) == v.length:
                    continue
                else:
                    self.domains[v].remove(option)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]
        consistent_x = []

        if not overlap:
            return False

        for op_1 in self.domains[x]:
            for op_2 in self.domains[y]:
                if op_1[overlap[0]] == op_2[overlap[1]]:
                    consistent_x.append(op_1)
                    break

        if len(self.domains[x]) == len(consistent_x):
            return False

        for option in self.domains[x].copy():
            if option not in consistent_x:
                self.domains[x].remove(option)

        return True
                    

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            queue = self.get_all_arcs()
        else:
            queue = arcs

        while queue:
            arc = queue[-1]
            queue.pop(-1)
            if self.revise(arc[0], arc[1]):
                if not self.domains[arc[0]]:
                    return False
                
                neighbors = self.crossword.neighbors(arc[0])
                neighbors.remove(arc[1])

                for neighbor in neighbors:
                    new_arc = (neighbor, arc[0])
                    queue.append(new_arc)
        return True

    def get_all_arcs(self):
        arcs = []

        for x in self.domains:
            neighbors = self.crossword.neighbors(x)

            for neighbor in neighbors:
                new_arc = x, neighbor
                arcs.append(new_arc)

        return arcs

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        variables = self.crossword.variables

        for value in variables:
            if assignment.get(value) == None:
                return False
            
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        values = list(assignment.values())
        values_has_duplicates = len(set(values)) < len(values)
        if values_has_duplicates:
            return False
    
        variables = list(assignment)
        for variable in variables:
            if variable.length != len(assignment[variable]):
                return False

        for v1 in variables:
            for v2 in variables:
                if v1 != v2:
                    overlap = self.crossword.overlaps[v1, v2]
                    word_1 = assignment[v1]
                    word_2 = assignment[v2]
                    if overlap:
                        if word_1[overlap[0]] != word_2[overlap[1]]:
                            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        domain_values = self.domains[var]
        assigned_values = list(assignment.values())

        values = [op for op in domain_values if op not in assigned_values]


        neighbors = self.crossword.neighbors(var) - set(assignment)

        conts_values = {}

        for option in values:
            conts_values[option] = 0
            for neighbor in neighbors:

                if option in self.domains[neighbor]:
                    conts_values[option] += 1

                for option_neighbor in self.domains[neighbor]:
                    if option_neighbor != option:
                        overlap = self.crossword.overlaps[var, neighbor]
                        if overlap:
                            if option[overlap[0]] != option_neighbor[overlap[1]]:
                                conts_values[option] +=1

        ordered_values = sorted(values, key=lambda a: conts_values[a])
        return ordered_values
        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
