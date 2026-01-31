Based on your request and the fermats and Eulers theorem.pptx file, here is the "fucking" breakdown of Fermat's Little Theorem, the algorithm, and the generalized code.The "Fuck" Explained: Fermat's Little TheoremThis theorem is the "Cheat Code" for modular arithmetic, but it has one strict rule: The Modulus MUST be a Prime Number.The Core Rule:
If $p$ is a prime number and $a$ is any integer not divisible by $p$, then:
$$a^{p-1} \equiv 1 \pmod p$$What does this actually mean?It means the powers of $a$ "reset" to 1 every time the exponent hits $p-1$.If you calculate $a^{p-1}$, the remainder is 1.If you calculate $a^{2(p-1)}$, the remainder is 1.If you calculate $a^{\text{massive number}}$, you can just chop off chunks of $p-1$ from the exponent because they all equal 1.The Alternative Form:
If you don't care about the "not divisible by $p$" rule, you can use this version:
$$a^p \equiv a \pmod p$$(This works even if $a$ is a multiple of $p$, because $0 \equiv 0$).The Algorithm (Step-by-Step)Goal: Calculate $a^E \pmod p$ efficiently.Check Constraint (The Prime Check):Is $p$ a prime number?If NO: STOP. You cannot use Fermat's Little Theorem (You must use Euler's Theorem instead).If YES: Proceed.Check Base (The Divisibility Check):Is $a$ a multiple of $p$? (i.e., is $a \% p == 0$?)If YES: The answer is immediately 0.If NO: Proceed to optimization.Reduce the Exponent (The Cheat):According to the theorem, $a^{p-1} \equiv 1$.We only care about the "leftover" exponent after removing all groups of $p-1$.New Exponent ($E_{new}$):$$E_{new} = E \pmod{p-1}$$Final Calculation:Calculate $a^{E_{new}} \pmod p$.This is now a tiny calculation compared to the original.
import math

print("\n========== FERMAT'S LITTLE THEOREM SOLVER ==========\n")

# --------------------------------------------------
# UTILITY: Primality Test
# Fermat's Theorem only works if Modulus (p) is Prime.
# --------------------------------------------------
def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# --------------------------------------------------
# THE MAIN ALGORITHM
# --------------------------------------------------
def solve_fermats(base, exponent, modulus):
    print(f"INPUT: {base}^{exponent} mod {modulus}\n")

    # STEP 1: Check if Modulus is Prime
    print(f"STEP 1: Checking if modulus {modulus} is Prime...")
    if not is_prime(modulus):
        print(f"   ERROR: {modulus} is NOT a prime number.")
        print("   Fermat's Little Theorem CANNOT be used.")
        print("   (Use Euler's Theorem for non-prime moduli).")
        return None
    print(f"   Yes, {modulus} is Prime. Proceeding.\n")

    # STEP 2: Check Divisibility (GCD)
    # If base is a multiple of modulus, answer is 0.
    if base % modulus == 0:
         print(f"STEP 2: Base {base} is divisible by {modulus}.")
         print(f"   Result is immediately 0.")
         return 0
    
    # STEP 3: Apply the Theorem
    # a^(p-1) = 1 (mod p)
    # We reduce the exponent by (p-1)
    fermat_power = modulus - 1
    print(f"STEP 3: Applying Fermat's Rule: a^{fermat_power} = 1 (mod {modulus})")
    
    reduced_exponent = exponent % fermat_power
    print(f"   Original Exponent: {exponent}")
    print(f"   Reduction: {exponent} % {fermat_power} = {reduced_exponent}")
    print(f"   New Problem: {base}^{reduced_exponent} mod {modulus}\n")

    # STEP 4: Final Calculation
    print(f"STEP 4: Calculating Final Result")
    # Using python's pow(base, exp, mod) for efficiency
    result = pow(base, reduced_exponent, modulus)
    
    print(f"   {base}^{reduced_exponent} mod {modulus} = {result}")
    
    print("\n===================================")
    print(f"FINAL ANSWER: {result}")
    print("===================================")
    return result

# --------------------------------------------------
# RUNNING THE CODE
# --------------------------------------------------
# Example 1: Standard Case (3^100 mod 7)
solve_fermats(3, 100, 7)

# Example 2: Invalid Case (Modulus 10 is not prime)
# solve_fermats(7, 20, 10)