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
    ]

    MISSING_OPERATORS = [
        "2 len('test')",
        "3(4 + 5)",
        "len('abc')(4 / 2)",
        "3.5(2 + 3)",
        "(3 + 4)(5 - 2)",
        "abs(4)(2 + 2)",
        "2 + 3(4 * 5)",
        "5(2 + len('test'))"
    ]

    INVALID_CHARACTERS = [
        "3 + $",
        "3 + 3 @ 4",
        "3 _ ",
        "# + 5",
        "len('test') ^ 2",
        "5 % 2",
        "2 & 3",
        "4 | 2",
        "2 ~ 3",
        "3 ! 4",
        "5 < 2",
        "7 > 3",
        "abs(3) ` 2",
        "3 ; 4",
        "len('a') : 3",
    ]

    TRAILING_OPERATORS = [
        "7 /",
        "4 + 5 -",
        "3 *",
        "2 +",
        "(5 + 2) *",
        "abs(-3) +",
        "len('test') -",
        "3 / 2 +",
        "4 **",
        "(3 - 2) /",
        "2 ** 3 *",
        "5 - 2 +",
        "3 + len('abc') /",
        "abs(4 - 2) -",
        "(4 + 3) **",
        "2 - 3 /",
        "len('hello') +",
        "4 * (2 + 3) -",
    ]

    MISMATCHED_PARENTHESES = [
        "(3 + 5",
        "2 * (4 + 3))",
        "((2 + 3) * 5",
        "abs(-4) + (3 - 2))",
        "(4 + (3 - 2)",
        "2 + 3) * 4",
        "((2 * 3) + 4",
        "(len('test' * 3)",
        "4 + 5) - (2 * 3",
        "len('hello'",
        "2 + (3 - 4",
        "(abs(-2) * 4",
        "(4 - 3)) + 2",
        "(3 * (2 + 5)",
        "(2 + 3 * (4 - 1)",
        "(2 + (3 - 4)",
        "3 - (2 + 3))",
        "((2 + 3) - 4",
        "((2 + 3) * (4 - 1)"
    ]

    CONSECUTIVE_OPERATORS = [
        "4 **+ 3",  # Triple asterisk followed by a slash
        "4 /// 3",  # Triple asterisk followed by a slash
        "7 **// 2",  # Double asterisk followed by double slash
        "6 */ 3",  # Asterisk followed by slash
        "8 /+ 4",  # Slash followed by minus
        "4 +* 2",  # Plus followed by asterisk
        "3 *-/ 2",  # Asterisk followed by minus-slash
        "2 +** 3",  # Minus followed by double asterisk
        "4 ** --2",  # Double asterisk followed by double minus
        "7 //++ 3",  # Double slash followed by double plus
        "3 +/** 4",  # Plus followed by slash-asterisk
        "6 /-+ 2",  # Slash followed by minus-plus
        "6 /* 2",  # Slash followed by minus-plus
        "6 */ 2",  # Slash followed by minus-plus
    ]

