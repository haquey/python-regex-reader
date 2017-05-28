
def p0(s):
    x = []
    y = permutations(s)
    for item in y:
        x.append(item)
    
    return x


def set_permutations(s):
    unique_perms = set()
    all_perms = permutations(s)
    for perm in all_perms:
        unique_perms.add(perm)
    
    return unique_perms

def permutations(s, counter=0):
    
    s = list(s)
    
    if counter == len(s):
        word = ''
        for char in s:
            word += char
        res = [word]
    
    else:
        res = permutations(s, counter + 1)
        for i in range(counter + 1, len(s)):
            s[counter], s[i] = s[i], s[counter]
            res.extend(permutations(s, counter + 1))
            s[counter], s[i] = s[i], s[counter]

    return res

def get_perms(s, i=0):
    """
    Returns a list of all (len(s) - i)! permutations t of s where t[:i] = s[:i].
    """
    # To avoid memory allocations for intermediate strings, use a list of chars.
    if isinstance(s, str):
        s = list(s)

    # Base Case: 0! = 1! = 1.
    # Store the only permutation as an immutable string, not a mutable list.
    if i >= len(s) - 1:
        return ["".join(s)]

    # Inductive Step: (len(s) - i)! = (len(s) - i) * (len(s) - i - 1)!
    # Swap in each suffix character to be at the beginning of the suffix.
    perms = get_perms(s, i + 1)
    for j in range(i + 1, len(s)):
        s[i], s[j] = s[j], s[i]
        perms.extend(get_perms(s, i + 1))
        s[i], s[j] = s[j], s[i]
    return perms