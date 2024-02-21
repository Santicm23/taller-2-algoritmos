from enum import Enum


class Cercania(Enum):
    IGUAL = "igual"
    MENOR = "menor"
    MAYOR = "mayor"


def obtener_cercania(n: int) -> Cercania:
    """Obtener la cercanía del número ingresado por el usuario."""
    cercania = input(f"Ingrese la cercania del número {n}: ")
    try:
        return Cercania(cercania)
    except ValueError:
        print("\nLa cercania ingresada no es válida.\n")
        return obtener_cercania(n)


def obtener_cercanias(numeros: list[int]) -> list[Cercania]:
    """Obtiene las cercanías de los números (ordenados) ingresados por el usuario."""

    numeros_msg = ", ".join([str(n) for n in numeros])
    print(f"El número que pensaste está entre los siguientes números: {numeros_msg}?\n")

    cercanias: list[Cercania] = []

    for n in numeros:
        cercania = obtener_cercania(n)

        cercanias.append(cercania)

        if cercania == Cercania.IGUAL:
            return [cercania]
        elif cercania == Cercania.MENOR:
            break

    return cercanias


def adivinar(n: int, cota_inferior: int = 0, paso: int = 100) -> int:
    """Adivina el número que el usuario pensó."""

    pivotes = [
        i for i in range(cota_inferior + paso, (n + 1) * paso, paso)
    ]  # lista de n pivotes ordenados

    cercanias = obtener_cercanias(pivotes)
    num_cercanias = len(cercanias)

    if num_cercanias > 1:
        cota_inferior = pivotes[num_cercanias - 2] + 1
    else:
        cota_inferior += 1

    if cercanias[0] == Cercania.IGUAL:
        return pivotes[num_cercanias - 1]
    elif cercanias[-1] == Cercania.MENOR:
        return adivinar_aux(n, cota_inferior, pivotes[num_cercanias - 1] - 1)

    return adivinar(n, pivotes[num_cercanias - 1] + 1, paso * 10)


def adivinar_aux(n: int, b: int, e: int) -> int:
    """Adivina el número que el usuario pensó entre una cota inferior y una superior."""

    division = (e - b + 1) // n

    pivotes = [b + division * i for i in range(n)]

    if b >= e:
        return b

    cercanias = obtener_cercanias(pivotes)
    num_cercanias = len(cercanias)

    cota_inferior = b

    if len(cercanias) > 1:
        cota_inferior = pivotes[num_cercanias - 2] + 1
    else:
        cota_inferior += 1

    if cercanias[0] == Cercania.IGUAL:
        return pivotes[num_cercanias - 1]
    elif cercanias[-1] == Cercania.MENOR:
        return adivinar_aux(n, cota_inferior, pivotes[num_cercanias - 1] - 1)
    else:
        return adivinar_aux(n, pivotes[num_cercanias - 1] + 1, e)


def main() -> None:
    print("Bienvenido al juego de adivinar.")
    print("Piensa en un número yo trataré de adivinarlo.")
    print("Dame un número inicial n para hacer el intento de n números a la vez.")
    print(
        "Luego de cada intento, dime si el número entero que pensaste es igual, menor o mayor a los que te dije."
    )
    print("Comencemos.\n")
    n = int(input("Piense en un número de respuestas que desee recibir\n"))
    print()

    res = adivinar(n)

    print(f"\nEl número que pensaste es {res}. Gracias por jugar.")


if __name__ == "__main__":
    main()
