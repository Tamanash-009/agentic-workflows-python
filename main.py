#!/usr/bin/env python3
"""
Agentic Workflows in Python
Demonstrates multi-agent orchestration and task automation
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime

class AgentWorkflow:
    """Core agent workflow system"""
    
    def __init__(self, agent_name: str, agent_id: str):
        self.agent_name = agent_name
        self.agent_id = agent_id
        self.tasks: List[Dict] = []
        self.completed_tasks: List[Dict] = []
        self.created_at = datetime.now()
    
    def add_task(self, task_id: str, description: str, priority: str = "normal", 
                 action_type: str = "process"):
        """Add a task to the workflow"""
        task = {
            "id": task_id,
            "description": description,
            "priority": priority,
            "action_type": action_type,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        return task
    
    def execute_task(self, task_id: str) -> Optional[Dict]:
        """Execute a single task"""
        for idx, task in enumerate(self.tasks):
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                self.completed_tasks.append(task)
                self.tasks.pop(idx)
                return task
        return None
    
    def get_pending_tasks(self) -> List[Dict]:
        """Get all pending tasks"""
        return sorted(self.tasks, key=lambda x: {"high": 0, "normal": 1, "low": 2}.get(x["priority"], 1))
    
    def get_workflow_status(self) -> Dict:
        """Get workflow status"""
        return {
            "agent_name": self.agent_name,
            "agent_id": self.agent_id,
            "pending_tasks": len(self.get_pending_tasks()),
            "completed_tasks": len(self.completed_tasks),
            "total_tasks": len(self.tasks) + len(self.completed_tasks),
            "completion_percentage": (len(self.completed_tasks) / (len(self.tasks) + len(self.completed_tasks)) * 100) if (len(self.tasks) + len(self.completed_tasks)) > 0 else 0
        }

if __name__ == "__main__":
    # Example: Create an agent and manage workflows
    print("=== Agentic Workflows System ===")
    
    agent = AgentWorkflow("DataProcessor", "agent-001")
    
    # Add tasks
    agent.add_task("t1", "Fetch data from API", "high", "fetch")
    agent.add_task("t2", "Validate data", "high", "validate")
    agent.add_task("t3", "Process data", "normal", "process")
    agent.add_task("t4", "Generate report", "normal", "report")
    
    print(f"\nInitial Status:")
    print(json.dumps(agent.get_workflow_status(), indent=2))
    
    print(f"\nPending Tasks:")
    for task in agent.get_pending_tasks():
        print(f"  - {task['id']}: {task['description']} (Priority: {task['priority']})")
    
    # Execute tasks
    print("\n--- Executing Tasks ---")
    for task_id in ["t1", "t2"]:
        result = agent.execute_task(task_id)
        if result:
            print(f"✓ Completed: {result['id']}")
    
    print(f"\nUpdated Status:")
    print(json.dumps(agent.get_workflow_status(), indent=2))
