def semantic_score(response):
    if not response:
        return 0.0
    length_score = min(len(response.split()) / 20, 1.0)
    polite = 0.2 if "please" in response.lower() else 0.0
    return min(1.0, length_score + polite)

def grade_action(email, action, env_state):
    reward = 0.0

    if action.action_type == "classify":
        if email.is_spam:
            reward += 0.8 * email.risk_score if action.response == "spam" else -1.0
        else:
            reward += 0.6 if action.response == "not_spam" else -0.8

    elif action.action_type == "reply":
        if email.requires_response:
            reward += semantic_score(action.response)
        else:
            reward -= 0.7

    elif action.action_type == "escalate":
        if email.is_urgent:
            reward += 0.7
        else:
            reward -= 0.5

    elif action.action_type == "ignore":
        if email.is_spam:
            reward += 0.5
        else:
            reward -= 1.0

    if env_state["missed_urgent"]:
        reward -= 0.5

    reward *= (0.5 + env_state["reputation"])

    return max(0.0, min(1.0, reward))
