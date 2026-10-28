import sys
import random
from main import IterativeCode

def main():
    if len(sys.argv) < 4:
        print("Usage: cli.py k1 k2 groups [input_bits]")
        print("groups: comma separated e.g. 2,3,4,5")
        return
    
    k1 = int(sys.argv[1])
    k2 = int(sys.argv[2])
    groups_str = sys.argv[3]
    parity_groups = [int(g.strip()) for g in groups_str.split(',')]
    
    code = IterativeCode(k1, k2, parity_groups)
    
    if len(sys.argv) > 4:
        input_str = sys.argv[4]
        bits = [int(c) for c in input_str if c in '01']
    else:
        bits = [random.randint(0, 1) for _ in range(code.k)]
    
    print(f"k={code.k} k1={k1} k2={k2} n={code.n} r={code.r} groups={parity_groups}")
    print(f"Input:   {''.join(map(str, bits))}")
    
    encoded = code.encode(bits)
    print(f"Encoded: {''.join(map(str, encoded))}")
    
    corrupted = encoded[:]
    num_errors = 1
    positions = random.sample(range(code.k), num_errors)
    for p in positions:
        corrupted[p] ^= 1
    print(f"Corrupt ({num_errors}): {''.join(map(str, corrupted))} at {positions}")
    
    corrected, found = code.decode(corrupted)
    print(f"Corrected: {''.join(map(str, corrected))}")
    print(f"Match: {corrected == bits}")

if __name__ == "__main__":
    main()
