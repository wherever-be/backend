from typing import List

from backend.trip import Trip


def pick_varied(candidates: List[Trip], max_trips: int):
    """A list of trips, limited to a sensible number, picked based on goodnes and variety"""
    remaining_candidates = [trip for trip in candidates]
    results: List[Trip] = []

    def variety_score(trip: Trip):
        if len(results) == 0:
            return trip.goodness
        return trip.goodness - max(result.similarity(trip) for result in results)

    for _ in range(max_trips):
        if len(remaining_candidates) == 0:
            break
        best_candidate = max(remaining_candidates, key=variety_score)
        remaining_candidates.remove(best_candidate)
        results.append(best_candidate)
    return results
