# SMARTMEET
# Performance Testing for DAA Core Algorithm

import random
import time

from algorithm import find_common_free_intervals


# ============================================================
# GENERATE RANDOM SCHEDULES
# ============================================================

def generate_schedules(number_of_participants):
    """
    Generate random busy schedules for testing.

    Each participant receives several busy intervals.
    """

    schedules = {}

    for person_number in range(
        1,
        number_of_participants + 1
    ):

        person_name = f"Person{person_number}"

        intervals = []

        # Generate 5 busy intervals per participant
        for _ in range(5):

            start_minute = random.randint(
                9 * 60,
                16 * 60
            )

            duration = random.randint(
                15,
                90
            )

            end_minute = min(
                start_minute + duration,
                17 * 60
            )

            if start_minute < end_minute:

                start_hour = start_minute // 60
                start_min = start_minute % 60

                end_hour = end_minute // 60
                end_min = end_minute % 60

                intervals.append(
                    (
                        f"{start_hour:02d}:{start_min:02d}",
                        f"{end_hour:02d}:{end_min:02d}"
                    )
                )

        schedules[person_name] = intervals

    return schedules


# ============================================================
# RUN ONE PERFORMANCE TEST
# ============================================================

def measure_performance(number_of_participants):

    schedules = generate_schedules(
        number_of_participants
    )

    start_time = time.perf_counter()

    result = find_common_free_intervals(
        schedules,
        "09:00",
        "17:00",
        30
    )

    end_time = time.perf_counter()

    execution_time = (
        end_time - start_time
    )

    return execution_time, len(result)


# ============================================================
# MAIN PERFORMANCE TEST
# ============================================================

def main():

    print()
    print("=" * 70)
    print("             SMARTMEET - PERFORMANCE TEST")
    print("=" * 70)

    print()
    print(
        "Measuring algorithm execution time "
        "for different numbers of participants."
    )

    print()
    print("-" * 70)

    print(
        f"{'Participants':<18}"
        f"{'Busy Intervals':<20}"
        f"{'Execution Time':<20}"
        f"{'Free Periods':<15}"
    )

    print("-" * 70)

    test_sizes = [
        10,
        50,
        100,
        500,
        1000,
        2000,
        5000
    ]

    for number_of_participants in test_sizes:

        execution_time, free_periods = (
            measure_performance(
                number_of_participants
            )
        )

        total_intervals = (
            number_of_participants * 5
        )

        print(
            f"{number_of_participants:<18}"
            f"{total_intervals:<20}"
            f"{execution_time:.6f} seconds"
            f"{'':<7}"
            f"{free_periods:<15}"
        )

    print("-" * 70)

    print()
    print("Performance testing completed.")
    print()

    print("DAA Observation:")
    print(
        "The algorithm sorts interval events before "
        "performing the sweep-line operation."
    )

    print(
        "Therefore, sorting is the dominant operation "
        "and the expected complexity is approximately O(I log I),"
    )

    print(
        "where I is the total number of busy intervals."
    )

    print()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()