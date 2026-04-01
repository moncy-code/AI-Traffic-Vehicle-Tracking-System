from collections import defaultdict


def build_transition_map(events):
    transitions = defaultdict(lambda: defaultdict(int))

    for i in range(len(events) - 1):
        current_camera = events[i]["camera_id"]
        next_camera = events[i + 1]["camera_id"]
        transitions[current_camera][next_camera] += 1

    return transitions


def predict_next_camera(events):
    if len(events) < 2:
        return None

    transitions = build_transition_map(events)
    last_camera = events[-1]["camera_id"]

    if last_camera in transitions and transitions[last_camera]:
        next_cams = transitions[last_camera]
        predicted = max(next_cams, key=next_cams.get)
        total = sum(next_cams.values())
        probability = next_cams[predicted] / total

        return {
            "predicted_camera": predicted,
            "probability": round(probability, 2)
        }

    # fallback: use the most common transition overall
    overall_counts = defaultdict(int)
    for from_cam, to_dict in transitions.items():
        for to_cam, count in to_dict.items():
            overall_counts[to_cam] += count

    if not overall_counts:
        return None

    predicted = max(overall_counts, key=overall_counts.get)
    total = sum(overall_counts.values())
    probability = overall_counts[predicted] / total

    return {
        "predicted_camera": predicted,
        "probability": round(probability, 2)
    }