from azure.identity import DefaultAzureCredential
from langchain import PromptTemplate
from openai import AzureOpenAI

from app.models.request.nlp_request import NLPRequest

credential = DefaultAzureCredential()
token = credential.get_token("https://cognitiveservices.azure.com/.default")


client = AzureOpenAI(
    api_key=token.token,
    api_version="2023-05-15",
    azure_endpoint="https://ic-ent-e2-cw-oai-dev.openai.azure.com/",
)

conversation = [{"role": "system", "content": "You are a helpful assistant"}]


class AzureOpenAIService:
    @staticmethod
    def run_azure_open_ai(request: NLPRequest, ocr_text: str):
        prompt_template = PromptTemplate(
            input_variables=["knowledge", "context"],
            template=request.template,
        )

        system_prompt = prompt_template.format(
            knowledge=request.knowledge, context=ocr_text
        )

        response = client.chat.completions.create(
            model="dev-gpt4-32k-cpl",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.user_content},
            ],
            frequency_penalty=request.frequency_penalty,
            max_tokens=request.max_tokens,
            presence_penalty=request.presence_penalty,
            # response_format={"type": "json_object"},
            stop=request.stop,
            temperature=request.temperature,
            top_p=request.top_p,
        )
        return response.choices[0].message.content
