# SMARTMEET
# Common Meeting Time Finder
# DAA Core Algorithm


def time_to_minutes(time_str):
    """Convert HH:MM into minutes."""

    hours, minutes = map(int, time_str.split(":"))

    if hours < 0 or hours > 23:
        raise ValueError("Invalid hour.")

    if minutes < 0 or minutes > 59:
        raise ValueError("Invalid minute.")

    return hours * 60 + minutes


def minutes_to_time(minutes):
    """Convert minutes into HH:MM."""

    hours = minutes // 60
    mins = minutes % 60

    return f"{hours:02d}:{mins:02d}"


def merge_intervals(intervals):
    """Merge overlapping busy intervals."""

    if not intervals:
        return []

    # Sort intervals according to start time
    intervals.sort(key=lambda x: x[0])

    merged = [intervals[0]]

    for current_start, current_end in intervals[1:]:

        last_start, last_end = merged[-1]

        if current_start <= last_end:

            merged[-1] = (
                last_start,
                max(last_end, current_end)
            )

        else:

            merged.append(
                (current_start, current_end)
            )

    return merged


def find_common_free_intervals(
    schedules,
    work_start,
    work_end,
    meeting_duration
):
    """
    Find common available time for all participants.

    schedules example:

    {
        "Alice": [
            ("09:00", "10:00")
        ],

        "Bob": [
            ("09:30", "11:00")
        ]
    }
    """

    # ---------------------------------
    # Validate meeting duration
    # ---------------------------------

    if meeting_duration <= 0:
        raise ValueError(
            "Meeting duration must be greater than 0."
        )

    # ---------------------------------
    # Convert working hours to minutes
    # ---------------------------------

    start = time_to_minutes(work_start)
    end = time_to_minutes(work_end)

    if start >= end:
        raise ValueError(
            "Working start time must be before end time."
        )

    # ---------------------------------
    # Store sweep-line events
    # ---------------------------------

    all_events = []

    # ---------------------------------
    # Process every participant
    # ---------------------------------

    for person, busy_intervals in schedules.items():

        converted_intervals = []

        for busy_start, busy_end in busy_intervals:

            start_time = time_to_minutes(busy_start)
            end_time = time_to_minutes(busy_end)

            if start_time >= end_time:
                raise ValueError(
                    f"Invalid interval for {person}: "
                    f"{busy_start} - {busy_end}"
                )

            # Ignore intervals completely outside
            # working hours

            if end_time <= start or start_time >= end:
                continue

            # Keep interval inside working hours

            start_time = max(start_time, start)
            end_time = min(end_time, end)

            converted_intervals.append(
                (start_time, end_time)
            )

        # Merge overlapping intervals
        merged = merge_intervals(converted_intervals)

        # Create sweep-line events
        for interval_start, interval_end in merged:

            # Start of busy interval
            all_events.append(
                (interval_start, +1)
            )

            # End of busy interval
            all_events.append(
                (interval_end, -1)
            )

    # ---------------------------------
    # Sort events by time
    # ---------------------------------

    all_events.sort(key=lambda x: x[0])

    # ---------------------------------
    # Sweep through timeline
    # ---------------------------------

    common_free_intervals = []

    busy_count = 0
    previous_time = start

    i = 0

    while i < len(all_events):

        current_time = all_events[i][0]

        # If everyone is free
        if (
            busy_count == 0
            and current_time > previous_time
        ):

            duration = current_time - previous_time

            if duration >= meeting_duration:

                common_free_intervals.append(
                    (
                        previous_time,
                        current_time
                    )
                )

        # Process all events at current time
        while (
            i < len(all_events)
            and all_events[i][0] == current_time
        ):

            busy_count += all_events[i][1]

            i += 1

        previous_time = current_time

    # ---------------------------------
    # Check remaining working time
    # ---------------------------------

    if busy_count == 0 and previous_time < end:

        duration = end - previous_time

        if duration >= meeting_duration:

            common_free_intervals.append(
                (
                    previous_time,
                    end
                )
            )

    # ---------------------------------
    # Convert result to HH:MM
    # ---------------------------------

    result = []

    for free_start, free_end in common_free_intervals:

        result.append(
            (
                minutes_to_time(free_start),
                minutes_to_time(free_end),
                free_end - free_start
            )
        )

    return result