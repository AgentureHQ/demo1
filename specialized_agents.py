import asyncio
import re
from typing import Dict, List, Any
from agent_base import Agent, MessageType
import json


class PlannerAgent(Agent):
    """Agent responsible for breaking down complex tasks into subtasks"""
    
    def __init__(self, name: str = "Planner", coordinator=None):
        super().__init__(name, coordinator)
        self.task_templates = {
            "data_analysis": ["collect_data", "clean_data", "analyze_data", "generate_report"],
            "web_scraping": ["identify_sources", "extract_data", "validate_data", "store_results"],
            "calculation": ["parse_input", "perform_calculation", "validate_result", "format_output"],
            "text_processing": ["tokenize_text", "process_content", "apply_transformations", "generate_output"]
        }
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_description = task.get("description", "")
        task_type = self.identify_task_type(task_description)
        
        print(f"🧠 {self.name} analyzing task: {task_description}")
        await asyncio.sleep(1)  # Simulate thinking time
        
        if task_type in self.task_templates:
            subtasks = self.task_templates[task_type]
        else:
            subtasks = self.create_generic_plan(task_description)
        
        plan = {
            "task_id": task.get("id"),
            "original_task": task_description,
            "task_type": task_type,
            "subtasks": subtasks,
            "estimated_duration": len(subtasks) * 2
        }
        
        print(f"📋 {self.name} created plan with {len(subtasks)} subtasks")
        
        # Request collaboration from ExecutorAgent
        await self.send_message(
            "Executor",
            MessageType.COLLABORATION_REQUEST,
            {"action": "execute_plan", "plan": plan}
        )
        
        return plan
    
    def identify_task_type(self, description: str) -> str:
        description_lower = description.lower()
        
        if any(word in description_lower for word in ["analyze", "data", "statistics"]):
            return "data_analysis"
        elif any(word in description_lower for word in ["scrape", "web", "extract"]):
            return "web_scraping"
        elif any(word in description_lower for word in ["calculate", "compute", "math"]):
            return "calculation"
        elif any(word in description_lower for word in ["text", "process", "format"]):
            return "text_processing"
        else:
            return "generic"
    
    def create_generic_plan(self, description: str) -> List[str]:
        return ["understand_requirements", "gather_resources", "execute_main_task", "verify_results"]


class ExecutorAgent(Agent):
    """Agent responsible for executing tasks and subtasks"""
    
    def __init__(self, name: str = "Executor", coordinator=None):
        super().__init__(name, coordinator)
        self.execution_methods = {
            "collect_data": self.simulate_data_collection,
            "clean_data": self.simulate_data_cleaning,
            "analyze_data": self.simulate_data_analysis,
            "generate_report": self.simulate_report_generation,
            "calculate": self.perform_calculation,
            "text_processing": self.process_text
        }
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_description = task.get("description", "")
        print(f"⚡ {self.name} executing task: {task_description}")
        
        # Simulate task execution
        await asyncio.sleep(2)
        
        result = {
            "task_completed": True,
            "execution_time": 2.0,
            "output": f"Successfully executed: {task_description}",
            "status": "completed"
        }
        
        print(f"✅ {self.name} completed task")
        return result
    
    async def handle_collaboration_request(self, message):
        content = message.content
        
        if content.get("action") == "execute_plan":
            plan = content.get("plan", {})
            await self.execute_plan(plan)
    
    async def execute_plan(self, plan: Dict[str, Any]):
        subtasks = plan.get("subtasks", [])
        print(f"🚀 {self.name} executing plan with {len(subtasks)} subtasks")
        
        results = []
        for i, subtask in enumerate(subtasks):
            print(f"📝 Executing subtask {i+1}/{len(subtasks)}: {subtask}")
            await asyncio.sleep(1)  # Simulate execution time
            
            result = await self.execute_subtask(subtask)
            results.append(result)
            
            # Send progress update to coordinator
            if self.coordinator:
                await self.send_message(
                    "Coordinator",
                    MessageType.STATUS_UPDATE,
                    {
                        "progress": (i + 1) / len(subtasks),
                        "current_subtask": subtask,
                        "subtask_result": result
                    }
                )
        
        final_result = {
            "plan_id": plan.get("task_id"),
            "subtask_results": results,
            "overall_status": "completed",
            "total_subtasks": len(subtasks)
        }
        
        # Send final result to Planner
        await self.send_message(
            "Planner",
            MessageType.RESULT,
            {"execution_complete": True, "results": final_result}
        )
        
        print(f"🎉 {self.name} completed all subtasks for plan")
    
    async def execute_subtask(self, subtask: str) -> Dict[str, Any]:
        # Simulate different types of subtask execution
        if "data" in subtask.lower():
            return {"type": "data_operation", "status": "success", "records_processed": 100}
        elif "calculate" in subtask.lower():
            return {"type": "calculation", "status": "success", "result": 42}
        elif "report" in subtask.lower():
            return {"type": "report", "status": "success", "pages_generated": 5}
        else:
            return {"type": "generic", "status": "success", "operation": subtask}
    
    async def simulate_data_collection(self) -> Dict[str, Any]:
        await asyncio.sleep(1)
        return {"records_collected": 1000, "sources": ["API", "Database"]}
    
    async def simulate_data_cleaning(self) -> Dict[str, Any]:
        await asyncio.sleep(1)
        return {"records_cleaned": 950, "errors_fixed": 50}
    
    async def simulate_data_analysis(self) -> Dict[str, Any]:
        await asyncio.sleep(2)
        return {"insights_found": 5, "accuracy": 0.95}
    
    async def simulate_report_generation(self) -> Dict[str, Any]:
        await asyncio.sleep(1)
        return {"report_pages": 10, "charts_created": 3}
    
    async def perform_calculation(self, data: str) -> Dict[str, Any]:
        # Simple calculator for demo
        try:
            # Extract numbers and basic operations
            numbers = re.findall(r'\d+', data)
            if len(numbers) >= 2:
                result = int(numbers[0]) + int(numbers[1])
                return {"calculation_result": result, "operation": "addition"}
        except:
            pass
        return {"calculation_result": "Unable to calculate", "operation": "unknown"}
    
    async def process_text(self, text: str) -> Dict[str, Any]:
        word_count = len(text.split())
        char_count = len(text)
        return {
            "word_count": word_count,
            "character_count": char_count,
            "processed": True
        }