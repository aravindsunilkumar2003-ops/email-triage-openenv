import os
import json
from openai import OpenAI
from app.env import EmailTriageEnv
from app.models import Action

client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = os.getenv("MODEL_NAME")

def parse_action(output, email_id):
    try:
        data = json.loads(output)
        return Action(
            action_type=data.get("action_type", "ignore"),
            email_id=email_id,
            response=data.get("response")
        )
    except:
        return Action(action_type="ignore", email_id=email_id)

def decide_action(email):
    prompt = f"""
    Email:
    Subject: {email.subject}
    Body: {email.body}
    Thread: {email.thread}

    Respond in JSON:
    {{ "action_type": "...", "response": "..." }}
    """

    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )

    return res.choices[0].message.content

def run():
    env = EmailTriageEnv()

    for task in ["easy", "medium", "hard"]:
        obs = env.reset(task)
        total = 0
        done = False

        while not done:
            email = obs["current_email"]
            raw = decide_action(email)
            action = parse_action(raw, email.id)

            obs, reward, done, _ = env.step(action)
            total += reward

        print(f"{task}: {total:.2f}")

if __name__ == "__main__":
    run()
