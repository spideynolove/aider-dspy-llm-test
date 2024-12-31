import dspy
import os
from dotenv import load_dotenv
from typing import Literal

load_dotenv('.env', override=True)


class ExtractInfo(dspy.Signature):
    """Extract structured information from text."""
    text: str = dspy.InputField()
    title: str = dspy.OutputField()
    headings: list[str] = dspy.OutputField()
    entities: list[dict[str, str]] = dspy.OutputField(
        desc="a list of entities and their metadata")


class Classify(dspy.Signature):
    """Classify sentiment of a given sentence."""

    sentence: str = dspy.InputField()
    sentiment: Literal['positive', 'negative', 'neutral'] = dspy.OutputField()
    confidence: float = dspy.OutputField()


def search_wikipedia_l(query: str) -> list[str]:
    results = dspy.ColBERTv2(
        url='http://20.102.90.50:2017/wiki17_abstracts')(query, k=3)
    return [x['text'] for x in results]


# def search_wikipedia_o(query: str):
#     results = dspy.ColBERTv2(
#         url='http://20.102.90.50:2017/wiki17_abstracts')(query, k=3)
#     return [x['text'] for x in results]


# def evaluate_math(expression: str):
#     return dspy.PythonInterpreter({}).execute(expression)

class EvaluateMathTool:
    name = "evaluate_math"
    input_variable = "expression"
    desc = "evaluates a mathematical expression"

    def __call__(self, expression):
        return dspy.PythonInterpreter({}).execute(expression)


class SearchWikipediaTool:
    name = "search_wikipedia"
    input_variable = "query"
    desc = "searches Wikipedia for information"

    def __call__(self, query):
        results = dspy.ColBERTv2(
            url='http://20.102.90.50:2017/wiki17_abstracts')(query, k=3)
        return [x['text'] for x in results]


class Outline(dspy.Signature):
    """Outline a thorough overview of a topic."""

    topic: str = dspy.InputField()
    title: str = dspy.OutputField()
    sections: list[str] = dspy.OutputField(
        desc="""Return ONLY a Python list literal containing section headings as strings.
        Example format: ["Introduction", "Historical Background", "Key Events", "Impact"]"""
    )
    section_subheadings: dict[str, list[str]] = dspy.OutputField(
        desc="""Return ONLY a Python dictionary literal mapping sections to subheading lists.
        Example format: {"Introduction": ["Overview", "Context"], "Historical Background": ["Early Period", "Modern Era"]}"""
    )

class DraftSection(dspy.Signature):
    """Draft a top-level section of an article."""

    topic: str = dspy.InputField()
    section_heading: str = dspy.InputField()
    section_subheadings: list[str] = dspy.InputField()
    content: str = dspy.OutputField(desc="markdown-formatted section")

class DraftArticle(dspy.Module):
    def __init__(self):
        self.build_outline = dspy.Predict(Outline)  # Changed from ChainOfThought to Predict
        self.draft_section = dspy.Predict(DraftSection)  # Changed from ChainOfThought to Predict

    def forward(self, topic):
        outline = self.build_outline(topic=topic)
        sections = []
        for heading in outline.sections:
            section = f"## {heading}"
            subheadings = outline.section_subheadings.get(heading, [])
            formatted_subheadings = [f"### {subheading}" for subheading in subheadings]
            section_content = self.draft_section(
                topic=outline.title,
                section_heading=section,
                section_subheadings=formatted_subheadings
            )
            sections.append(section_content.content)
        return dspy.Prediction(title=outline.title, sections=sections)


if __name__ == "__main__":
    lm = dspy.LM(os.getenv('OPENAI_MODEL_ID'), api_key=os.getenv(
        'OPENAI_API_KEY'), api_base=os.getenv('OPENAI_BASE_URL'))
    dspy.configure(lm=lm)

    # math = dspy.ChainOfThought("question -> answer: float")
    # response = math(question="Two dice are tossed. What is the probability that the sum equals two?")
    # print(response.reasoning)
    # print(response.answer)

    # module = dspy.Predict(ExtractInfo)
    # text = "Apple Inc. announced its latest iPhone 14 today." \
    #     "The CEO, Tim Cook, highlighted its new features in a press release."
    # response = module(text=text)
    # print(response.title)
    # print(response.headings)
    # print(response.entities)

    # classify = dspy.Predict(Classify)
    # response = classify(sentence="This book was super fun to read, though not the last chapter.")
    # print(response.sentiment)
    # print(response.confidence)

    # rag = dspy.ChainOfThought('context, question -> response')
    # question = "What's the name of the castle that David Gregory inherited?"
    # response = rag(context=search_wikipedia_l(question), question=question)
    # print(response.reasoning)
    # print(response.response)

    # evaluate_math = EvaluateMathTool()
    # search_wikipedia_o = SearchWikipediaTool()
    # react = dspy.ReAct("question -> answer: float",
    #                    tools=[evaluate_math, search_wikipedia_o])
    # pred = react(
    #     question="What is 9362158 divided by the year of birth of David Gregory of Kinnairdy castle?")
    # print(pred)

    draft_article = DraftArticle()
    article = draft_article(topic="World Cup 2022")
    print(article)
