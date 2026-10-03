from algorithm import (
    find_common_free_intervals,
    generate_meeting_slots
)


def display_schedule(schedules):
    """
    Display all participant schedules.
    """

    print("\nParticipant Schedules")
    print("-" * 40)

    for person, intervals in schedules.items():

        print(f"\n{person}:")

        if not intervals:
            print("  No busy periods")

        else:
            for start, end in intervals:
                print(f"  {start} - {end}")


def main():

    print("=" * 60)
    print("              SMARTMEET")
    print("       Common Meeting Time Finder")
    print("=" * 60)

    # -----------------------------------------
    # Sample participant schedules
    # -----------------------------------------

    schedules = {

        "Alice": [
            ("09:00", "10:00"),
            ("13:00", "14:00")
        ],

        "Bob": [
            ("09:30", "11:00"),
            ("14:00", "15:00")
        ],

        "Charlie": [
            ("10:00", "11:30")
        ]
    }

    # -----------------------------------------
    # Meeting settings
    # -----------------------------------------

    work_start = "09:00"
    work_end = "17:00"

    meeting_duration = 30

    # -----------------------------------------
    # Display input
    # -----------------------------------------

    display_schedule(schedules)

    print("\nWorking Hours:")
    print(f"{work_start} - {work_end}")

    print("\nRequired Meeting Duration:")
    print(f"{meeting_duration} minutes")

    # -----------------------------------------
    # Run the DAA algorithm
    # -----------------------------------------

    print("\nSearching for common available time...")

    result = find_common_free_intervals(
        schedules,
        work_start,
        work_end,
        meeting_duration
    )

    # -----------------------------------------
    # Generate actual meeting slots
    # -----------------------------------------

    meeting_slots = generate_meeting_slots(
        result,
        meeting_duration
    )

    # -----------------------------------------
    # Display common free intervals
    # -----------------------------------------

    print("\n" + "=" * 60)
    print("COMMON AVAILABLE TIMES")
    print("=" * 60)

    if not result:

        print("No suitable meeting time found.")

    else:

        for number, (start, end, duration) in enumerate(
            result,
            start=1
        ):

            print(
                f"{number}. {start} - {end}"
                f" ({duration} minutes)"
            )

    # -----------------------------------------
    # Display possible meeting slots
    # -----------------------------------------

    print("\n" + "=" * 60)
    print("POSSIBLE MEETING SLOTS")
    print("=" * 60)

    if not meeting_slots:

        print("No meeting slots available.")

    else:

        for number, (start, end) in enumerate(
            meeting_slots,
            start=1
        ):

            print(
                f"{number}. {start} - {end}"
            )

    # -----------------------------------------
    # Program completed
    # -----------------------------------------

    print("\n" + "=" * 60)
    print("Program completed successfully.")
    print("=" * 60)


# ---------------------------------------------
# Start the program
# ---------------------------------------------

if __name__ == "__main__":
    main()