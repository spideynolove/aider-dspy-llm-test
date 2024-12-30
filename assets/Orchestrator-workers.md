Workflow: Orchestrator-workers  

In the orchestrator-workers workflow, a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results.  

```mermaid  
graph LR  
    A((In)) --> B[Orchestrator]  
    B -.-> C[LLM Call 1]  
    B -.-> D[LLM Call 2]  
    B -.-> E[LLM Call 3]  
    C -.-> F[Synthesizer]  
    D -.-> F  
    E -.-> F  
    F --> G((Out))  

    style A fill:#FFEFEF  
    style B fill:#F0FFF0  
    style C fill:#F0FFF0  
    style D fill:#F0FFF0  
    style E fill:#F0FFF0  
    style F fill:#F0FFF0  
    style G fill:#FFEFEF  
```  

When to use this workflow: This workflow is well-suited for complex tasks where you can’t predict the subtasks needed (in coding, for example, the number of files that need to be changed and the nature of the change in each file likely depend on the task). Whereas it’s topographically similar, the key difference from parallelization is its flexibility—subtasks aren't pre-defined, but determined by the orchestrator based on the specific input.  

Example where orchestrator-workers is useful:  

- Coding products that make complex changes to multiple files each time.  
- Search tasks that involve gathering and analyzing information from multiple sources for possible relevant information.  