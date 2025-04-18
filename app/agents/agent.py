import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from tools.webscrap import WebScrap

class State(TypedDict):
    text: str
    webscrap: WebScrap

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
def webscrap_node(state: State):
    webscrap = WebScrap()
    webscrap.trip_flights(state["origin"], state["destination"])
    webscrap.date_trip(state["ida"], state["volta"])
    webscrap.search_flights()
    webscrap.capture_content()
    return {"webscrap": webscrap}

def decision_node(state: State):
    prompt_decision = PromptTemplate(
        input_variables=["text"],
        template="Analyse with the following information: {text} and decide if it is a good idea to book a flight to {destination} from {origin}."
    )

    message = HumanMessage(content=prompt_decision.format(text=state["text"], destination=state["destination"], origin=state["origin"]))

    decision = llm.invoke([message]).content.strip()

    return {"decision": decision}

def main():
    graph = StateGraph(State)
    graph.add_node("webscrap_node", webscrap_node)
    graph.add_node("decision_node", decision_node)
    graph.add_edge(START, "webscrap_node")
    graph.add_edge("webscrap_node", "decision_node")
    graph.add_edge("decision_node", END)
    graph.compile()

    app = graph.compile()

    state_input = {"text": "I want to book a flight to Paris from New York", "destination": "Paris", "origin": "New York"}
    result = app.invoke(state_input)
    print(result)

if __name__ == "__main__":
    main()