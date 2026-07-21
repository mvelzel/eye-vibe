#!/usr/bin/env python3
"""Test a five-direction S3 transducer against the nine header edges."""

from eye_mystery.conformance_grid import marker_control_edge
from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.s3_transducer import (
    calibrate_body_assignments,
    scan_s3_direction_transducers,
)


def main() -> None:
    bodies = tuple(MESSAGES[name][3:] for name in MESSAGE_ORDER)
    edges = tuple(
        marker_control_edge(trigram_values(MESSAGES[name])[0])
        for name in MESSAGE_ORDER
    )
    scan = scan_s3_direction_transducers(bodies, edges)
    print("model match histogram:", scan.match_histogram)
    print("best edge matches:", scan.best_match_count)
    print("number of best models:", len(scan.best_models))
    best = scan.best_models[0]
    print("best eye order:", best.eye_order)
    print("best direction operations:", best.direction_operations)
    print("best body outputs:", best.body_outputs)

    calibration = calibrate_body_assignments(scan.all_outputs, edges)
    print("body-assignment calibration:", calibration)
    print(
        "fraction with at least eight:",
        (calibration.exactly_eight + calibration.all_nine) / calibration.total,
    )
    print("fraction with all nine:", calibration.all_nine / calibration.total)


if __name__ == "__main__":
    main()
