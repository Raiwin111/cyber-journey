import sys

def analyze_password(password):
    if len(password) <8:
        return "Weak (Too short!)"
    elif password.isdigit():
        return "Medium (Only numbersM Try adding letters!)"
    else:
        return "Strong (Good job!)"

if __name__ == "__main__":
    user_input = sys.argv[1]
    result = analyze_password(user_input)
    print(result)
