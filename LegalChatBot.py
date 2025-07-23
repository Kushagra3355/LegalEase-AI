from langgraph.graph import StateGraph
from typing import List, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from bare_act_retriever import BareActRetriever


class GraphState(TypedDict):
    query: str
    context_docs: List[str]
    messages: List[BaseMessage]
    response: str


class LegalGraphChatBot:
    def __init__(
        self,
        faiss_path: str = "faiss_index_legal",
        embedding_model: str = "text-embedding-3-small",
        llm_model: str = "gpt-4o-mini",
    ):
        self.retriever = BareActRetriever(faiss_path=faiss_path, model=embedding_model)
        self.llm = ChatOpenAI(model=llm_model)
        self.graph = self._build_graph()

    def _memory_node(self, state: GraphState) -> GraphState:
        query = state["query"]
        state["messages"].append(HumanMessage(content=query))
        return state

    def _retriever_node(self, state: GraphState) -> GraphState:
        docs = self.retriever.retrieve(state["query"])
        state["context_docs"] = [doc["content"] for doc in docs]

    def _llm_node(self, state: GraphState) -> GraphState:
        system_prompt = """You are a legal assistant specialized in Indian law. You help users understand the law simply,  
            based on their question and the context retrieved from bare acts.
            Keep the explaination as small as possible.
            NEVER give legal advice. Always cite the source (act or section)."""
        context = "\n\n".join(state["context_docs"])
        messages = [
            {"role": "system", "content": system_prompt},
            *state["messages"],
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{state['query']}",
            },
        ]

        response = self.llm.invoke(messages)
        state["messages"].append(AIMessage(content=response.content))
        state["response"] = response.content
        return state

    def _build_graph(self):

        graph_builder = StateGraph(GraphState)
        graph_builder.add_node("memory", self._memory_node)
        graph_builder.add_node("retrieve", self._retriever_node)
        graph_builder.add_node("llm", self._llm_node)

        graph_builder.set_entry_point("memory")
        graph_builder.add_edge("memory", "retrieve")
        graph_builder.add_edge("retrieve", "llm")
        graph_builder.set_finish_point("llm")

        return graph_builder.compile()

    def init_state(self) -> GraphState:
        return {"query": "", "messages": [], "context_docs": [], "response": ""}

    def invoke(self, state: GraphState, query: str) -> GraphState:
        state["query"] = query
        return self.graph.invoke(state)