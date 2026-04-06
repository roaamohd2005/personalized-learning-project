from collections import defaultdict

def generate_personalized_plan(responses):
    topic_data = defaultdict(lambda: {"correct": 0, "total": 0, "times": [], "conf": []})
    
    for r in responses:
        t = r["topic"]
        topic_data[t]["correct"] += 1 if r.get("correct", False) else 0
        topic_data[t]["total"] += 1
        topic_data[t]["times"].append(r.get("time_sec", 60))
        topic_data[t]["conf"].append(r.get("confidence", 5))

    plan_items = []
    for topic, data in topic_data.items():
        accuracy = (data["correct"] / data["total"] * 100) if data["total"] > 0 else 0
        avg_time = sum(data["times"]) / len(data["times"])
        avg_conf = sum(data["conf"]) / len(data["conf"])
        
        time_factor = max(0.1, 1 - (avg_time - 20) / 120)
        mastery = round(accuracy * time_factor * (avg_conf / 10))
        
        if mastery < 50:
            priority = "HIGH - Start here"
            difficulty = "Beginner"
            sessions = 5
        elif mastery < 75:
            priority = "MEDIUM"
            difficulty = "Intermediate"
            sessions = 3
        elif mastery < 90:
            priority = "LOW - Quick review"
            difficulty = "Advanced"
            sessions = 1
        else:
            priority = "SKIP / Challenge"
            difficulty = "Expert"
            sessions = 1
        
        plan_items.append({
            "topic": topic,
            "mastery_score": mastery,
            "priority": priority,
            "difficulty": difficulty,
            "recommended_sessions": sessions,
            "estimated_time_minutes": round(sessions * avg_time / 60) + 10
        })
    
    # Sort by priority
    priority_order = {"HIGH - Start here": 1, "MEDIUM": 2, "LOW - Quick review": 3, "SKIP / Challenge": 4}
    plan_items.sort(key=lambda x: priority_order.get(x["priority"], 5))
    
    return {
        "weak_topics": [item["topic"] for item in plan_items if item["mastery_score"] < 50],
        "recommended_plan": plan_items
    }