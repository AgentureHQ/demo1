import asyncio
import json
from typing import Dict, List, Any, Optional
from agent_base import Agent, Message, MessageType
from specialized_agents import PlannerAgent, ExecutorAgent
import time


class TaskCoordinator:
    """Central coordinator managing agent communication and task distribution"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.message_history: List[Message] = []
        self.active_tasks: Dict[str, Dict] = {}
        self.task_counter = 0
        
    def register_agent(self, agent: Agent):
        self.agents[agent.name] = agent
        agent.coordinator = self
        print(f"🔗 Registered agent: {agent.name}")
    
    async def route_message(self, message: Message):
        self.message_history.append(message)
        
        recipient = self.agents.get(message.recipient)
        if recipient:
            await recipient.receive_message(message)
        else:
            print(f"⚠️ Unknown recipient: {message.recipient}")
    
    async def submit_user_task(self, task_description: str) -> str:
        self.task_counter += 1
        task_id = f"task_{self.task_counter}_{int(time.time())}"
        
        task = {
            "id": task_id,
            "description": task_description,
            "submitted_at": time.time(),
            "status": "submitted"
        }
        
        self.active_tasks[task_id] = task
        
        print(f"📥 New task submitted: {task_description}")
        print(f"🆔 Task ID: {task_id}")
        
        # Route task to PlannerAgent first
        await self.route_message(Message(
            id=f"msg_{task_id}",
            sender="User",
            recipient="Planner",
            message_type=MessageType.TASK_REQUEST,
            content=task,
            timestamp=time.time()
        ))
        
        return task_id
    
    async def get_task_status(self, task_id: str) -> Optional[Dict]:
        return self.active_tasks.get(task_id)
    
    def get_message_history(self, limit: int = 10) -> List[Dict]:
        recent_messages = self.message_history[-limit:] if limit > 0 else self.message_history
        return [msg.to_dict() for msg in recent_messages]
    
    async def start_agents(self):
        print("🚀 Starting all agents...")
        tasks = []
        for agent in self.agents.values():
            task = asyncio.create_task(agent.start())
            tasks.append(task)
        
        return tasks
    
    async def stop_agents(self):
        print("🛑 Stopping all agents...")
        for agent in self.agents.values():
            await agent.stop()
    
    def print_status(self):
        print("\n" + "="*50)
        print("📊 SYSTEM STATUS")
        print("="*50)
        print(f"Active Agents: {len(self.agents)}")
        for name in self.agents.keys():
            print(f"  • {name}")
        
        print(f"\nActive Tasks: {len(self.active_tasks)}")
        for task_id, task in self.active_tasks.items():
            print(f"  • {task_id}: {task['description'][:50]}...")
        
        print(f"\nMessage History: {len(self.message_history)} messages")
        
        # Show recent messages
        if self.message_history:
            print("\n📨 Recent Messages:")
            for msg in self.message_history[-3:]:
                print(f"  {msg.sender} → {msg.recipient}: {msg.message_type.value}")
        
        print("="*50 + "\n")


class DemoScenarios:
    """Predefined demo scenarios showcasing agent collaboration"""
    
    def __init__(self, coordinator: TaskCoordinator):
        self.coordinator = coordinator
        
    async def run_data_analysis_demo(self):
        print("🎬 Running Data Analysis Demo")
        await self.coordinator.submit_user_task(
            "Analyze sales data from Q3 2024 and generate insights report"
        )
        await asyncio.sleep(10)  # Let agents work
    
    async def run_calculation_demo(self):
        print("🎬 Running Calculation Demo")
        await self.coordinator.submit_user_task(
            "Calculate the compound interest for $1000 at 5% annually for 10 years"
        )
        await asyncio.sleep(8)  # Let agents work
    
    async def run_text_processing_demo(self):
        print("🎬 Running Text Processing Demo")
        await self.coordinator.submit_user_task(
            "Process and format the user manual text for better readability"
        )
        await asyncio.sleep(6)  # Let agents work
    
    async def run_web_scraping_demo(self):
        print("🎬 Running Web Scraping Demo")
        await self.coordinator.submit_user_task(
            "Scrape product information from e-commerce sites and create comparison report"
        )
        await asyncio.sleep(12)  # Let agents work
    
    async def run_all_demos(self):
        print("🎭 Running all demo scenarios...")
        await self.run_data_analysis_demo()
        await asyncio.sleep(2)
        
        await self.run_calculation_demo()
        await asyncio.sleep(2)
        
        await self.run_text_processing_demo()
        await asyncio.sleep(2)
        
        await self.run_web_scraping_demo()
        
        print("🎉 All demos completed!")


async def create_demo_system() -> TaskCoordinator:
    """Initialize the demo system with agents and coordinator"""
    coordinator = TaskCoordinator()
    
    # Create and register agents
    planner = PlannerAgent("Planner")
    executor = ExecutorAgent("Executor")
    
    coordinator.register_agent(planner)
    coordinator.register_agent(executor)
    
    return coordinator