from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import ChatOpenAI, ChatAnthropic, ChatOllama


class Assistant:
    def __init__(self, model_name='gpt-4'):
        self.history = []
        self.llm = self._get_llm(model_name)
        self.model_name = model_name

    def _get_llm(self, model_name):
        if model_name.startswith("gpt"):
            return ChatOpenAI(model=model_name)
        elif model_name.startswith("claude"):
            return ChatAnthropic(model=model_name)
        elif model_name.startswith("ollama:"):
            return ChatOllama(model=model_name.split("ollama:", 1)[1])
        else:
            raise ValueError(f"Unsupported model: {model_name}")

    def switch_model(self, new_model_name):
        self.llm = self._get_llm(new_model_name)
        self.model_name = new_model_name
        print(f"Switched to model: {new_model_name}")

    async def ask(self, query: str) -> str:
        self.history.append(HumanMessage(content=query))
        response = await self.llm.ainvoke(self.history)
        self.history.append(AIMessage(content=response.content))
        return response.content

    def print_history(self):
        for msg in self.history:
            who = "You" if isinstance(msg, HumanMessage) else "Assistant"
            print(f"{who}: {msg.content}")

    def reset_history(self):
        self.history = []

    def get_model_name(self):
        return self.model_name


# assistant = Assistant(model_name="ollama:mistral")
# print(assistant.ask("Hii my name is Vineet."))

# assistant.switch_model("ollama:qwen:0.5b")
# print(assistant.ask("what is my name?"))

# assistant.print_history()
