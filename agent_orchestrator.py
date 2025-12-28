#!/usr/bin/env python3
"""
Agent Orchestrator - Manages multiple agentic workflows
"""

from main import AgentWorkflow
from typing import List, Dict
import json

class AgentOrchestrator:
    """Orchestrates multiple agentic workflows"""
    
    def __init__(self, orchestrator_name: str):
        self.orchestrator_name = orchestrator_name
        self.agents: List[AgentWorkflow] = []
        self.execution_history: List[Dict] = []
    
    def create_agent(self, agent_name: str, agent_id: str) -> AgentWorkflow:
        """Create and register a new agent"""
        agent = AgentWorkflow(agent_name, agent_id)
        self.agents.append(agent)
        return agent
    
    def get_all_workflows_status(self) -> Dict:
        """Get status of all agents"""
        return {
            "orchestrator": self.orchestrator_name,
            "total_agents": len(self.agents),
            "agents": [agent.get_workflow_status() for agent in self.agents],
            "total_pending": sum(len(agent.get_pending_tasks()) for agent in self.agents),
            "total_completed": sum(len(agent.completed_tasks) for agent in self.agents)
        }
    
    def execute_all_pending_tasks(self) -> Dict:
        """Execute all pending tasks across all agents"""
        execution_report = {
            "timestamp": str(__import__('datetime').datetime.now()),
            "agents_processed": 0,
            "tasks_executed": 0,
            "details": []
        }
        
        for agent in self.agents:
            pending_count = len(agent.get_pending_tasks())
            if pending_count > 0:
                for task in list(agent.tasks):
                    agent.execute_task(task["id"])
                    execution_report["tasks_executed"] += 1
                
                execution_report["agents_processed"] += 1
                execution_report["details"].append({
                    "agent": agent.agent_name,
                    "tasks_completed": pending_count
                })
        
        return execution_report
    
    def distribute_task(self, agent_id: str, task_id: str, description: str, priority: str = "normal"):
        """Distribute a task to a specific agent"""
        for agent in self.agents:
            if agent.agent_id == agent_id:
                return agent.add_task(task_id, description, priority)
        return None

if __name__ == "__main__":
    print("=== Agent Orchestrator System ===")
    
    # Create orchestrator
    orchestrator = AgentOrchestrator("MasterOrchestrator")
    
    # Create multiple agents
    agent1 = orchestrator.create_agent("DataFetcher", "agent-001")
    agent2 = orchestrator.create_agent("DataProcessor", "agent-002")
    agent3 = orchestrator.create_agent("ReportGenerator", "agent-003")
    
    # Add tasks to agents
    agent1.add_task("df1", "Fetch from API", "high")
    agent1.add_task("df2", "Fetch from Database", "normal")
    
    agent2.add_task("dp1", "Clean data", "high")
    agent2.add_task("dp2", "Transform data", "normal")
    
    agent3.add_task("rg1", "Generate summary", "normal")
    agent3.add_task("rg2", "Generate charts", "low")
    
    print("\n=== Initial Status ===")
    print(json.dumps(orchestrator.get_all_workflows_status(), indent=2))
    
    print("\n=== Executing All Tasks ===")
    result = orchestrator.execute_all_pending_tasks()
    print(json.dumps(result, indent=2))
    
    print("\n=== Final Status ===")
    print(json.dumps(orchestrator.get_all_workflows_status(), indent=2))
