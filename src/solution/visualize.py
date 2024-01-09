from typing import Dict, List

import numpy as np
from matplotlib import pyplot as plt

from ..elements.operating_room import OperatingRoom
from ..elements.uce_room import UceRoom
from .assignment import Assignment


def visualize_or(assignments_by_or: Dict[OperatingRoom, List[Assignment]]):
    for operating_room in assignments_by_or:
        if not assignments_by_or[operating_room]:
            plt.barh(operating_room.id, 0, left=0, height=0.5, align="center", alpha=0.7)
            continue

        for assignment in assignments_by_or[operating_room]:
            plt.barh(
                operating_room.id,
                assignment.operation_cleaning_interval.upper - assignment.operation_cleaning_interval.lower,
                left=assignment.operation_cleaning_interval.lower,
                height=0.5,
                align="center",
                alpha=0.7,
            )
            plt.text(
                (assignment.operation_cleaning_interval.upper + assignment.operation_cleaning_interval.lower) / 2,
                operating_room.id,
                f"{assignment.patient.id}",
                ha="center",
                va="center",
            )

    plt.xlabel("Value")
    plt.ylabel("Interval")
    plt.title("Non-Overlapping Intervals")
    plt.xticks(np.arange(8, 95, 12))
    plt.xticks(np.arange(8, 95, 3))

    plt.yticks(np.arange(1, 9), [operating_room.surgical_type.id for operating_room in assignments_by_or])
    plt.grid(axis="x")
    plt.show()


def visualize_ur(assignments_by_ur: Dict[UceRoom, List[Assignment]]):
    two_patients: Dict[UceRoom, Dict[int, bool]] = {}
    for ur in assignments_by_ur:
        two_patients[ur] = {}
        for assignment in sorted(assignments_by_ur[ur], key=lambda x: x.uce_interval.lower):
            interval_range = np.arange(assignment.uce_interval.lower, assignment.uce_interval.upper)
            bottom = False
            for num in interval_range:
                if num in two_patients[ur]:
                    bottom = False if two_patients[ur][num] else True
                    break

            plt.barh(
                ur.id + (0 if bottom else 0.5),
                assignment.uce_interval.upper - assignment.uce_interval.lower,
                left=assignment.uce_interval.lower,
                height=0.5,
                align="center",
                alpha=0.7,
            )
            plt.text(
                (assignment.uce_interval.upper + assignment.uce_interval.lower) / 2,
                ur.id + (0 if bottom else 0.5),
                (
                    f"id={assignment.patient.id}, {'m' if assignment.patient.sex == 1 else 'w'}, "
                    + f"p={assignment.patient.priority}, st={assignment.patient.surgical_type.id}"
                ),
                ha="center",
                va="center",
            )

            for num in interval_range:
                two_patients[ur][num] = bottom

    plt.xlabel("Value")
    plt.ylabel("Interval")
    plt.title("Non-Overlapping Intervals")
    plt.xticks(np.arange(12, 13 + 24 * 6.5, 12))

    plt.yticks(np.arange(1, 11), [ur.id for ur in assignments_by_ur])
    plt.grid(axis="x")
    plt.show()
