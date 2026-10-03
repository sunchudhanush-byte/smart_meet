# SMARTMEET
# Automated Testing for DAA Core Algorithm

from algorithm import (
    find_common_free_intervals,
    generate_meeting_slots
)


# ============================================================
# TEST COUNTERS
# ============================================================

tests_passed = 0
tests_failed = 0


# ============================================================
# TEST HELPER
# ============================================================

def run_test(test_number, test_name, test_function):
    """
    Run one test and display PASS or FAIL.
    """

    global tests_passed
    global tests_failed

    try:

        test_function()

        print(
            f"Test {test_number:02d}: "
            f"{test_name:<35} PASS"
        )

        tests_passed += 1

    except AssertionError as error:

        print(
            f"Test {test_number:02d}: "
            f"{test_name:<35} FAIL"
        )

        print(
            f"          Reason: {error}"
        )

        tests_failed += 1

    except Exception as error:

        print(
            f"Test {test_number:02d}: "
            f"{test_name:<35} ERROR"
        )

        print(
            f"          Reason: {error}"
        )

        tests_failed += 1


# ============================================================
# TEST 1
# NORMAL CASE
# ============================================================

def test_normal_case():

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

    result = find_common_free_intervals(
        schedules,
        "09:00",
        "17:00",
        30
    )

    expected = [
        ("11:30", "13:00", 90),
        ("15:00", "17:00", 120)
    ]

    assert result == expected, (
        f"Expected {expected}, got {result}"
    )


# ============================================================
# TEST 2
# EVERYONE FREE
# ============================================================

def test_everyone_free():

    schedules = {
        "Alice": [],
        "Bob": [],
        "Charlie": []
    }

    result = find_common_free_intervals(
        schedules,
        "09:00",
        "17:00",
        30
    )

    expected = [
        ("09:00", "17:00", 480)
    ]

    assert result == expected, (
        f"Expected {expected}, got {result}"
    )


# ============================================================
# TEST 3
# NO COMMON TIME
# ============================================================

def test_no_common_time():

    schedules = {

        "Alice": [
            ("09:00", "17:00")
        ],

        "Bob": [
            ("09:00", "17:00")
        ]
    }

    result = find_common_free_intervals(
        schedules,
        "09:00",
        "17:00",
        30
    )

    assert result == [], (
        f"Expected no available time, got {result}"
    )


# ============================================================
# TEST 4
# OVERLAPPING INTERVALS
# ============================================================

def test_overlapping_intervals():

    schedules = {

        "Alice": [
            ("09:00", "10:00"),
            ("09:30", "11:00")
        ],

        "Bob": [
            ("09:00", "11:30")
        ]
    }

    result = find_common_free_intervals(
        schedules,
        "09:00",
        "17:00",
        30
    )

    expected = [
        ("11:30", "17:00", 330)
    ]

    assert result == expected, (
        f"Expected {expected}, got {result}"
    )


# ============================================================
# TEST 5
# ONE PARTICIPANT
# ============================================================

def test_one_participant():

    schedules = {

        "Alice": [
            ("10:00", "11:00")
        ]
    }

    result = find_common_free_intervals(
        schedules,
        "09:00",
        "17:00",
        30
    )

    expected = [
        ("09:00", "10:00", 60),
        ("11:00", "17:00", 360)
    ]

    assert result == expected, (
        f"Expected {expected}, got {result}"
    )


# ============================================================
# TEST 6
# MEETING DURATION TOO LONG
# ============================================================

def test_duration_too_long():

    schedules = {

        "Alice": [
            ("09:00", "10:00")
        ],

        "Bob": [
            ("09:00", "10:00")
        ]
    }

    result = find_common_free_intervals(
        schedules,
        "09:00",
        "10:00",
        120
    )

    assert result == [], (
        f"Expected no slot, got {result}"
    )


# ============================================================
# TEST 7
# BUSY AT BEGINNING
# ============================================================

def test_busy_at_beginning():

    schedules = {

        "Alice": [
            ("09:00", "10:00")
        ],

        "Bob": [
            ("09:00", "10:30")
        ]
    }

    result = find_common_free_intervals(
        schedules,
        "09:00",
        "17:00",
        30
    )

    expected = [
        ("10:30", "17:00", 390)
    ]

    assert result == expected, (
        f"Expected {expected}, got {result}"
    )


# ============================================================
# TEST 8
# BUSY AT END
# ============================================================

def test_busy_at_end():

    schedules = {

        "Alice": [
            ("16:00", "17:00")
        ],

        "Bob": [
            ("15:30", "17:00")
        ]
    }

    result = find_common_free_intervals(
        schedules,
        "09:00",
        "17:00",
        30
    )

    expected = [
        ("09:00", "15:30", 390)
    ]

    assert result == expected, (
        f"Expected {expected}, got {result}"
    )


# ============================================================
# TEST 9
# SAME BOUNDARY TIME
# ============================================================

def test_same_boundary_time():

    schedules = {

        "Alice": [
            ("09:00", "10:00")
        ],

        "Bob": [
            ("10:00", "11:00")
        ]
    }

    result = find_common_free_intervals(
        schedules,
        "09:00",
        "17:00",
        30
    )

    expected = [
        ("11:00", "17:00", 360)
    ]

    assert result == expected, (
        f"Expected {expected}, got {result}"
    )


# ============================================================
# TEST 10
# MULTIPLE OVERLAPS
# ============================================================

def test_multiple_overlaps():

    schedules = {

        "Alice": [
            ("09:00", "10:00"),
            ("10:30", "11:30"),
            ("13:00", "14:00")
        ],

        "Bob": [
            ("09:30", "11:00"),
            ("12:30", "13:30")
        ],

        "Charlie": [
            ("10:00", "12:00"),
            ("13:30", "15:00")
        ]
    }

    result = find_common_free_intervals(
        schedules,
        "09:00",
        "17:00",
        30
    )

    expected = [
        ("12:00", "12:30", 30),
        ("15:00", "17:00", 120)
    ]

    assert result == expected, (
        f"Expected {expected}, got {result}"
    )


# ============================================================
# TEST 11
# OUTSIDE WORKING HOURS
# ============================================================

def test_outside_working_hours():

    schedules = {

        "Alice": [
            ("07:00", "08:00"),
            ("10:00", "11:00"),
            ("18:00", "19:00")
        ]
    }

    result = find_common_free_intervals(
        schedules,
        "09:00",
        "17:00",
        30
    )

    expected = [
        ("09:00", "10:00", 60),
        ("11:00", "17:00", 360)
    ]

    assert result == expected, (
        f"Expected {expected}, got {result}"
    )


# ============================================================
# TEST 12
# INVALID DURATION
# ============================================================

def test_invalid_duration():

    schedules = {
        "Alice": [
            ("09:00", "10:00")
        ]
    }

    try:

        find_common_free_intervals(
            schedules,
            "09:00",
            "17:00",
            0
        )

        assert False, (
            "Expected ValueError for duration 0"
        )

    except ValueError:

        pass


# ============================================================
# TEST 13
# INVALID WORKING HOURS
# ============================================================

def test_invalid_working_hours():

    schedules = {
        "Alice": [
            ("09:00", "10:00")
        ]
    }

    try:

        find_common_free_intervals(
            schedules,
            "17:00",
            "09:00",
            30
        )

        assert False, (
            "Expected ValueError for invalid working hours"
        )

    except ValueError:

        pass


# ============================================================
# TEST 14
# INVALID BUSY INTERVAL
# ============================================================

def test_invalid_busy_interval():

    schedules = {

        "Alice": [
            ("11:00", "10:00")
        ]
    }

    try:

        find_common_free_intervals(
            schedules,
            "09:00",
            "17:00",
            30
        )

        assert False, (
            "Expected ValueError for invalid busy interval"
        )

    except ValueError:

        pass


# ============================================================
# TEST 15
# GENERATE MEETING SLOTS
# ============================================================

def test_generate_meeting_slots():

    free_intervals = [
        ("09:00", "11:00", 120)
    ]

    result = generate_meeting_slots(
        free_intervals,
        30
    )

    expected = [
        ("09:00", "09:30"),
        ("09:30", "10:00"),
        ("10:00", "10:30"),
        ("10:30", "11:00")
    ]

    assert result == expected, (
        f"Expected {expected}, got {result}"
    )


# ============================================================
# TEST 16
# MEETING SLOT WITH REMAINDER
# ============================================================

def test_meeting_slot_remainder():

    free_intervals = [
        ("09:00", "10:15", 75)
    ]

    result = generate_meeting_slots(
        free_intervals,
        30
    )

    expected = [
        ("09:00", "09:30"),
        ("09:30", "10:00")
    ]

    assert result == expected, (
        f"Expected {expected}, got {result}"
    )


# ============================================================
# RUN ALL TESTS
# ============================================================

def main():

    print()
    print("=" * 70)
    print("             SMARTMEET - AUTOMATED TESTING")
    print("=" * 70)

    print()
    print("Testing the DAA Common Meeting Time Algorithm")
    print("-" * 70)

    # Reset counters

    global tests_passed
    global tests_failed

    tests_passed = 0
    tests_failed = 0

    # Run tests

    run_test(
        1,
        "Normal Case",
        test_normal_case
    )

    run_test(
        2,
        "Everyone Free",
        test_everyone_free
    )

    run_test(
        3,
        "No Common Time",
        test_no_common_time
    )

    run_test(
        4,
        "Overlapping Intervals",
        test_overlapping_intervals
    )

    run_test(
        5,
        "One Participant",
        test_one_participant
    )

    run_test(
        6,
        "Meeting Duration Too Long",
        test_duration_too_long
    )

    run_test(
        7,
        "Busy At Beginning",
        test_busy_at_beginning
    )

    run_test(
        8,
        "Busy At End",
        test_busy_at_end
    )

    run_test(
        9,
        "Same Boundary Time",
        test_same_boundary_time
    )

    run_test(
        10,
        "Multiple Overlaps",
        test_multiple_overlaps
    )

    run_test(
        11,
        "Outside Working Hours",
        test_outside_working_hours
    )

    run_test(
        12,
        "Invalid Duration",
        test_invalid_duration
    )

    run_test(
        13,
        "Invalid Working Hours",
        test_invalid_working_hours
    )

    run_test(
        14,
        "Invalid Busy Interval",
        test_invalid_busy_interval
    )

    run_test(
        15,
        "Generate Meeting Slots",
        test_generate_meeting_slots
    )

    run_test(
        16,
        "Meeting Slot With Remainder",
        test_meeting_slot_remainder
    )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    total_tests = (
        tests_passed
        + tests_failed
    )

    print()
    print("=" * 70)
    print("                    TEST SUMMARY")
    print("=" * 70)

    print(
        f"Total Tests : {total_tests}"
    )

    print(
        f"Tests Passed: {tests_passed}"
    )

    print(
        f"Tests Failed: {tests_failed}"
    )

    print("=" * 70)

    if tests_failed == 0:

        print()
        print("✓ ALL TESTS PASSED")
        print("✓ SMARTMEET algorithm is working correctly.")
        print()

    else:

        print()
        print("✗ SOME TESTS FAILED")
        print("Please check the failed tests above.")
        print()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()