from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI


def create_client():
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")

    return AzureOpenAI(
        api_key=token.token,
        api_version="2023-05-15",
        azure_endpoint="https://ic-ent-e2-cw-oai-dev.openai.azure.com/",
    )


class AzureOpenAIService:
    @staticmethod
    def run_azure_open_ai(
        system_content: str,
        user_content: str,
        frequency_penalty: float,
        presence_penalty: float,
        temperature: float,
        top_p: float,
        max_tokens: int,
        stop: str | list[str],
    ):
        client = create_client()
        response = client.chat.completions.create(
            model="dev-gpt4-32k-cpl",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
            frequency_penalty=frequency_penalty,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            # response_format={"type": "json_object"},
            stop=stop,
            temperature=temperature,
            top_p=top_p,
        )
        return response.choices[0].message.content
