def mymax(iterable, key=lambda x: x):
    # incijaliziraj maksimalni element i maksimalni ključ
    max_x = max_key = None

    # obiđi sve elemente
    for x in iterable:
        # ako je key(x) najveći -> ažuriraj max_x i max_key
        if max_x is None or key(x) > max_key:
            max_key = key(x)
            max_x = x
    # vrati rezultat
    return max_x


def main():
    maxint = mymax([1, 3, 5, 7, 4, 6, 9, 2, 0])
    maxchar = mymax("Suncana strana ulice")
    maxstring = mymax([
        "Gle", "malu", "vocku", "poslije", "kise",
        "Puna", "je", "kapi", "pa", "ih", "njise"])
    D = {'burek': 8, 'buhtla': 5}
    maxdict = mymax(D, D.get)
    people = [('pero', 'peric'), ('ivo', 'ivic'), ('ana', 'anic')]
    maxtuplelist = mymax(people)
    print(maxint, maxchar, maxstring, maxdict, maxtuplelist, sep='\n')


if __name__ == '__main__':
    main()
