def print_distance_table(d, word1, word2, backtrace=None, like_in_notes=True, with_colors=True):
    """
    Debug function - Prints distance table like we have in our notes unless like_in_notes=False

    If like_in_notes=False, it prints it like on the website: http://www.let.rug.nl/~kleiweg/lev/
    This includes terminal colors, which may break on your terminal (especially on Windows)
    Passing with_colors=False will disable this, but still print the table "upside down"

    When passed a backtrace, here is how the function behaves with the different values for like_in_notes:
    True: replaces numbers with asterisks
    False: colors numbers yellow (again, note this may not work with your terminal)
           If used with with_colors=False, will also replace numbers with asterisks

    """
    # Get lengths of words
    m = len(word1)
    n = len(word2)

    # Create backtrace list if specified
    if backtrace is not None:
        backtrace = [(i, j) for i, j, k in backtrace]
    else:
        backtrace = []

    if like_in_notes:

        for i in range(m):

            print(f"{word1[m-i-1]}  ", end="")
            if m-i > 9:
                space = " "
            else:
                space = "  "
            if (m-i, 0) in backtrace:
                print("*", end="  ")
            else:
                print(d[m-i][0], end=space)
            print("|  ", end="")
            for j in range(1, n+1):
                if (m-i, j) in backtrace:
                    print("*", end="  ")
                else:
                    if d[m-i][j] > 9:
                        space = " "
                    else:
                        space = "  "
                    print(d[m-i][j], end=space)
            print()

        print("-- "*(3+n))

        if backtrace:
            print("#  *  |  ", end="")
        else:
            print("#  0  |  ", end="")
        for j in range(n):
            if j > 9:
                space = " "
            else:
                space = "  "
            if (0, j+1) in backtrace:
                print('*', end=space)
            else:
                print(d[0][j+1], end=space)
        print()

        print("   #  |  ", end="")
        for j in range(n):
            print(word2[j], end="  ")

    else:

        if with_colors:
            red_text_color = "\033[1;31m"
            reset_text_color = "\033[0m"
            yellow_text_color = "\033[1;33m"
        else:
            red_text_color = ""
            reset_text_color = ""
            yellow_text_color = ""

        print(f"      {red_text_color}", end="")
        for j in range(n):
            if j > 9:
                space = " "
            else:
                space = "  "
            print(word2[j], end=space)
        print(reset_text_color)

        print(f"   ", end="")
        for j in range(n+1):
            if j > 9:
                space = " "
            else:
                space = "  "
            if (0, j) in backtrace:
                if with_colors:
                    print(f"{yellow_text_color}{d[0][j]}", end=f"{space}{reset_text_color}")
                else:
                    print("*", end="  ")
            else:
                print(d[0][j], end=space)
        print()

        for i in range(1, m+1):
            print(f"{red_text_color}{word1[i-1]}  {reset_text_color}", end="")
            if i > 9:
                space = " "
            else:
                space = "  "
            if (i-1, 0) in backtrace:
                if with_colors:
                    print(f"{d[i][0]}", end=space)
                else:
                    print("*", end="  ")
            else:
                print(d[i][0], end=space)
            for j in range(1, n+1):
                if d[i][j] > 9:
                    space = " "
                else:
                    space = "  "
                if (i, j) in backtrace:
                    if with_colors:
                        print(f"{yellow_text_color}{d[i][j]}", end=f"{space}{reset_text_color}")
                    else:
                        print("*", end="  ")
                else:
                    print(d[i][j], end=space)
            print()

    print()
    print()