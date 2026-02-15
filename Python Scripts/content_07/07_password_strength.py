import re

def PasswordDetection(pw):
    missing = []

    # Rules as regex
    rules = {
        "at least 8 characters": r".{8,}",
        "an uppercase letter": r"[A-Z]",
        "a lowercase letter": r"[a-z]",
        "a number": r"\d"
    }

    for rule_name, rule_pattern in rules.items():
        if not re.search(rule_pattern, pw):
            missing.append(rule_name)

    if not missing:
        print("Good Password")
    else:
        print("Bad Password — missing:")
        for item in missing:
            print(f" - {item}")

PasswordDetection("Johnathan1")
