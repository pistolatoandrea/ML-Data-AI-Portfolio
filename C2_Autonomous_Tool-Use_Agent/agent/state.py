from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    task: str                          # original user task
    subtasks: list[str]                # sub-questions from last node
    search_results: Annotated[list[str], operator.add]  # cumulative result, not overwritten
    report: str                        # final report
    iterations: int                    # loop iterations counter
    run_folder: str