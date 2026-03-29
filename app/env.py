from .tasks import load_tasks
from .grader import grade_action

class EmailTriageEnv:
    def __init__(self):
        self.tasks = load_tasks()

    def reset(self, task="easy"):
        self.emails = self.tasks[task]
        self.index = 0
        self.reputation = 0.5
        self.memory = []
        self.step_count = 0
        self.missed_urgent = False
        return self._obs()

    def _obs(self):
        return {
            "current_email": self.emails[self.index],
            "inbox_remaining": len(self.emails) - self.index,
            "memory_summary": self.memory[-3:],
            "reputation": self.reputation,
            "step_count": self.step_count,
            "goal": "Maximize inbox efficiency and safety"
        }

    def step(self, action):
        email = self.emails[self.index]

        state = {
            "reputation": self.reputation,
            "missed_urgent": self.missed_urgent
        }

        reward = grade_action(email, action, state)

        self.reputation += (reward - 0.5) * 0.1
        self.reputation = max(0.0, min(1.0, self.reputation))

        if email.is_urgent and action.action_type == "ignore":
            self.missed_urgent = True
            self.memory.append("Missed urgent email")

        self.step_count += 1
        self.index += 1

        done = self.index >= len(self.emails)

        return (None if done else self._obs()), reward, done, {}
