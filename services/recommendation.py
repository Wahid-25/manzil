def recommend_transport(results):
    """
    Analyzes the travel results and identifies the cheapest, fastest, and
    best balanced option (comfort, safety, cost, time combined score).
    """
    if not results:
        return None, None, None
    cheapest = min(results, key=lambda x: x["fare"])
    fastest = min(results, key=lambda x: x["time"])
    # Score option by prioritizing comfort and safety, penalizing fare and time
    # Higher score is better
    def calculate_score(option):
        comfort = option["comfort"]
        safety = option["safety"]
        # Normalize fare division (assume average PKR fare is around 500-5000)
        fare_penalty = option["fare"] / 1000.0
        time_penalty = option["time"]
        return (comfort * 1.5) + (safety * 1.5) - fare_penalty - (time_penalty * 2)
    best_balanced = max(results, key=calculate_score)
    return cheapest, fastest, best_balanced