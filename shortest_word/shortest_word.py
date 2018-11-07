import enum
from copy import copy

INFTY = 10**16


class Result(enum.Enum):
    FOUND_MIN = 0
    NOT_FOUND = 1
    INCORRECT_REGEX = 2


class IncorrectRegexError(Exception):
    pass


class LanguageInfo:
    def __init__(self, needed_len, needed_symb, symb):
        self._needed_len = needed_len

        if symb == needed_symb:
            # map: k->min(len(word)), word ends with x^k, k <= needed_len
            self.ends_with_letter = {0: 1, 1: 1}
            # all lens of x^k in language, k <= needed_len
            self.only_letter = {1}

            self.best_ends = self.best_only = 1 if needed_len <= 1 else INFTY
        elif symb == '1':
            self.ends_with_letter, self.only_letter = {0: 0}, {0}
            self.best_ends = self.best_only = 0 if needed_len == 0 else INFTY
        else:
            self.ends_with_letter, self.only_letter = {0: 1}, set()
            self.best_ends = 1 if needed_len == 0 else INFTY
            self.best_only = INFTY

    @staticmethod
    def put_if_min(di, key, value):
        if key in di:
            di[key] = min(di[key], value)
        else:
            di[key] = value

    def plus(self, right):
        self.best_ends = min(self.best_ends, right.best_ends)
        self.best_only = min(self.best_only, right.best_only)
        self.only_letter.update(right.only_letter)

        for xlen, l2 in right.ends_with_letter.items():
            self.put_if_min(self.ends_with_letter, xlen, l2)

    def mult(self, right):
        ml = min(list(self.ends_with_letter.values()) + list(self.only_letter))
        new_ends_with_letter = copy(right.ends_with_letter)
        for key in new_ends_with_letter:
            new_ends_with_letter[key] += ml
        self.best_ends = right.best_ends + ml

        for xlen, l1 in self.ends_with_letter.items():
            for l2 in sorted(right.only_letter):
                if xlen + l2 < self._needed_len:
                    self.put_if_min(new_ends_with_letter, xlen + l2, l1 + l2)
                elif l1 + l2 < self.best_ends:
                    self.put_if_min(new_ends_with_letter, xlen + l2, l1 + l2)
                    self.best_ends = l1 + l2
        self.ends_with_letter = new_ends_with_letter

        new_only_letter = set()
        self.best_only = INFTY
        for l1 in sorted(self.only_letter):
            for l2 in sorted(right.only_letter):
                l12 = l1 + l2
                if l12 < self._needed_len:
                    new_only_letter.add(l12)
                elif l12 < self.best_only:
                    new_only_letter.add(l12)
                    self.best_only = l12
        self.only_letter = new_only_letter

    def apply_star(self):
        self.ends_with_letter[0] = 0
        self.only_letter.add(0)

        prev_only = set()
        new_only = set()
        for i in range(self._needed_len + 1):
            for length in self.only_letter:
                new_len = length * i
                if new_len < self._needed_len:
                    new_only.add(new_len)
                elif new_len < self.best_only:
                    new_only.add(new_len)
                    self.best_only = new_len

            if prev_only == new_only:
                self.only_letter = new_only
                break
            prev_only = new_only
            new_only = set()

        for xlen, l1 in list(self.ends_with_letter.items()):
            for l2 in self.only_letter:
                if xlen + l2 < self._needed_len:
                    self.ends_with_letter[xlen + l2] = l1 + l2
                elif l1 + l2 < self.best_ends:
                    self.ends_with_letter[xlen + l2] = l1 + l2
                    self.best_ends = l1 + l2

    def __repr__(self):
        return (str(self.best_ends) + ' ' + str(self.best_only) + ' ' +
                str(self.ends_with_letter) + ' ' + str(self.only_letter))


def check_stack_len(stack, required_len):
    if len(stack) < required_len:
        raise IncorrectRegexError()


def find_min_len(regex, needed_symb, needed_len):
    stack = []
    try:
        for symb in regex:
            if symb == '*':
                check_stack_len(stack, 1)
                stack[-1].apply_star()
            elif symb == '+':
                check_stack_len(stack, 2)
                right = stack.pop()
                stack[-1].plus(right)
            elif symb == '.':
                check_stack_len(stack, 2)
                right = stack.pop()
                stack[-1].mult(right)
            else:
                if symb not in 'abc1':
                    raise IncorrectRegexError()
                stack.append(LanguageInfo(needed_len, needed_symb, symb))

        if len(stack) != 1:
            raise IncorrectRegexError()
    except IncorrectRegexError:
        return 0, Result.INCORRECT_REGEX

    result = min(stack[0].best_ends, stack[0].best_only)
    return result, Result.FOUND_MIN if result < INFTY else Result.NOT_FOUND


if __name__ == '__main__':
    regex, needed_symb, needed_len = input().split()
    needed_len = int(needed_len)
    ans, res = find_min_len(regex, needed_symb, needed_len)
    if res is Result.FOUND_MIN:
        print(ans)
    elif res is Result.NOT_FOUND:
        print('INF')
    else:
        print('ERROR')
