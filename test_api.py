from utils.config import client, MODEL

response = client.models.generate_content(
    model=MODEL,
    contents="Say hello in one sentence."
)

print(response.text)