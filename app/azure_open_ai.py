from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

# credential = InteractiveBrowserCredential()
credential = DefaultAzureCredential()
token = credential.get_token("https://cognitiveservices.azure.com/.default")


client = AzureOpenAI(
    api_key=token.token,
    api_version="2023-05-15",
    azure_endpoint="https://ic-ent-e2-cw-oai-dev.openai.azure.com/",
)

conversation = [{"role": "system", "content": "You are a helpful assistant"}]


def read_root(user_input: str):
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="dev-gpt4-32k-cpl", messages=conversation
    )
    return response.choices[0].message.content
