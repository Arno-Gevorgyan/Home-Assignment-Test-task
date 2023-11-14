class SyntaxValidatorConstants:
    VALID_EXPRESSIONS = [
        "10 / abs(5) + len('hello world')",
        "abs(-100) * len('abc') / 2",
        "len('data') - abs(-4) * 3",
        "len('Django') ** 2 + abs(-15) // 3",
        "(len('Python3') + abs(-7)) * 4",
        "abs(len('syntax') - 10) ** 3",
        "len('') + abs(-20) / 5",
        "len('valid') * 2 + abs(3 - len('expr'))",
        "abs(-50 / len('test')) + 2 ** len('valid')",
        "(len('compute') + 3) * abs(-2) - 5"
    ]

    EMPTY_PARENTHESES = [
        "len('') - ()",
        "abs(()) + 5",
        "() / 3 + 2",
        "2 * (3 + ())",
        "4 ** (2 - ())",
        "(() + 3) * 5",
        "len('test' + ())",
        "abs(-3) * ()",
        "(()) + 3",
        "3 - (() / 2)",
        "5 / (2 - ())",
        "len('()') - ()",
        "() * abs(-2)",
        "3 + abs(())",
    ]

    MISSING_OPERATORS = [
        "2 len('test')",
    ]

    INVALID_CHARACTERS = [
        "3 + $",
        "3 + 3 @ 4",
        "3 _ "
    ]

    TRAILING_OPERATORS = [
        "7 /",
        "4 + 5 -"
    ]

    MISMATCHED_PARENTHESES = [
        "(3 + 5",
    ]

    CONSECUTIVE_OPERATORS = [
        "4 ***/ 3",
    ]
