"""
String Efficiency Calculator
Power Systems-II
Suspension Insulator String
"""

import numpy as np


def calculate_string(n, k, total_voltage):
    """
    Calculate voltage distribution across a suspension
    insulator string using the capacitance-network equations.

    n = number of insulator units
    k = shunt capacitance / self-capacitance
    total_voltage = total string voltage in kV
    """

    # Unknown node voltages:
    # V1, V2, ..., V(n-1)
    #
    # Bottom/conductor voltage = total_voltage
    # Top/earth voltage = 0

    if n < 2:
        raise ValueError("Number of units must be at least 2.")

    if k < 0:
        raise ValueError("Capacitance ratio cannot be negative.")

    if total_voltage <= 0:
        raise ValueError("String voltage must be positive.")

    # Matrix equation A*x = b
    A = np.zeros((n - 1, n - 1))
    b = np.zeros(n - 1)

    # Build capacitance network
    for i in range(n - 1):

        A[i, i] = 2 + k

        if i > 0:
            A[i, i - 1] = -1

        if i < n - 2:
            A[i, i + 1] = -1

    # Conductor-side boundary
    b[0] = total_voltage

    # Solve node voltages
    node_voltages = np.linalg.solve(A, b)

    # Node voltages from earth to conductor
    nodes = [0.0] + list(node_voltages) + [total_voltage]

    # Voltage across each disc
    disc_voltages = []

    for i in range(n):
        voltage = nodes[i + 1] - nodes[i]
        disc_voltages.append(voltage)

    maximum_voltage = max(disc_voltages)

    efficiency = (
        total_voltage
        / (n * maximum_voltage)
    ) * 100

    return disc_voltages, maximum_voltage, efficiency


def main():

    print("=" * 65)
    print("       SUSPENSION INSULATOR STRING EFFICIENCY")
    print("                   POWER SYSTEMS-II")
    print("=" * 65)

    try:

        n = int(
            input("\nEnter number of insulator units: ")
        )

        k = float(
            input(
                "Enter shunt-to-self capacitance ratio (k): "
            )
        )

        total_voltage = float(
            input(
                "Enter total string voltage (kV): "
            )
        )

        if n < 2:
            raise ValueError(
                "Number of units must be at least 2."
            )

        if k < 0:
            raise ValueError(
                "Capacitance ratio cannot be negative."
            )

        if total_voltage <= 0:
            raise ValueError(
                "Voltage must be greater than zero."
            )

        disc_voltages, maximum_voltage, efficiency = (
            calculate_string(
                n,
                k,
                total_voltage
            )
        )

        print("\n" + "=" * 65)
        print("                    RESULTS")
        print("=" * 65)

        print("\nVOLTAGE DISTRIBUTION")
        print("-" * 65)

        print(
            f"{'Unit':<15}"
            f"{'Voltage (kV)':<20}"
            f"{'% of String Voltage':<20}"
        )

        print("-" * 65)

        for i, voltage in enumerate(
            disc_voltages, start=1
        ):

            percentage = (
                voltage / total_voltage
            ) * 100

            print(
                f"{i:<15}"
                f"{voltage:<20.4f}"
                f"{percentage:<20.2f}"
            )

        print("-" * 65)

        print(
            f"\nTotal String Voltage : "
            f"{total_voltage:.4f} kV"
        )

        print(
            f"Maximum Unit Voltage : "
            f"{maximum_voltage:.4f} kV"
        )

        print(
            f"Number of Units      : "
            f"{n}"
        )

        print(
            f"Capacitance Ratio    : "
            f"{k}"
        )

        print(
            f"\nString Efficiency    : "
            f"{efficiency:.2f} %"
        )

        print("=" * 65)

    except ValueError as error:

        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
