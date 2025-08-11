# Multi-Agent Collaboration Demo

A Python-based demonstration of two intelligent agents collaborating to complete user-provided tasks.

## Architecture

The system consists of:

- **PlannerAgent**: Analyzes tasks and breaks them into subtasks
- **ExecutorAgent**: Executes plans and individual tasks
- **TaskCoordinator**: Manages communication and task distribution
- **User Interface**: Command-line interface for interaction

## Features

✨ **Agent Collaboration**: Two agents work together on complex tasks
🧠 **Intelligent Planning**: Automatic task breakdown based on task type  
⚡ **Parallel Execution**: Asynchronous task processing
📊 **Real-time Monitoring**: Live progress updates and status tracking
🎭 **Demo Scenarios**: Pre-built examples showcasing different capabilities

## Quick Start

### Interactive Mode
```bash
python main.py
```

### Demo Mode
```bash
# Run all demo scenarios
python main.py --demo

# Run specific scenario
python main.py --demo data      # Data analysis demo
python main.py --demo calc      # Calculation demo  
python main.py --demo text      # Text processing demo
python main.py --demo web       # Web scraping demo
```

## Usage Examples

In interactive mode, you can submit various types of tasks:

```
💭 Enter task: Analyze quarterly sales data and generate insights
💭 Enter task: Calculate compound interest for $5000 at 4% for 10 years
💭 Enter task: Process customer feedback text for sentiment analysis
💭 Enter task: Scrape competitor pricing from multiple websites
```

## Available Commands

- `help` - Show available commands
- `status` - Display system status  
- `history [n]` - Show last n messages
- `demo` - Access demo scenarios menu
- `quit` - Exit the application

## How It Works

1. **Task Submission**: User submits a task description
2. **Planning Phase**: PlannerAgent analyzes the task and creates a structured plan
3. **Collaboration**: PlannerAgent requests ExecutorAgent to execute the plan
4. **Execution**: ExecutorAgent processes each subtask with progress updates
5. **Completion**: Results are reported back through the coordination system

## Agent Capabilities

### PlannerAgent
- Task type identification (data analysis, calculation, text processing, web scraping)
- Intelligent task breakdown into subtasks
- Estimation of execution time
- Collaboration request management

### ExecutorAgent  
- Subtask execution simulation
- Progress reporting
- Result aggregation
- Multiple execution method support

## File Structure

```
demo1/
├── agent_base.py          # Base Agent class and message system
├── specialized_agents.py  # PlannerAgent and ExecutorAgent implementations  
├── coordinator.py         # TaskCoordinator and DemoScenarios
├── main.py               # Main application and user interface
└── README.md             # This file
```

## Example Output

```
🎯 Multi-Agent Collaboration Demo
========================================
Two agents (Planner & Executor) are ready to collaborate!
Type 'help' for commands, 'quit' to exit

💭 Enter task: Analyze sales data from Q3 2024

🤖 Planner agent started
🤖 Executor agent started
📥 New task submitted: Analyze sales data from Q3 2024
🆔 Task ID: task_1_1723987654
📨 Planner received task_request from User  
🧠 Planner analyzing task: Analyze sales data from Q3 2024
📋 Planner created plan with 4 subtasks
📨 Executor received collaboration_request from Planner
🚀 Executor executing plan with 4 subtasks
📝 Executing subtask 1/4: collect_data
📝 Executing subtask 2/4: clean_data  
📝 Executing subtask 3/4: analyze_data
📝 Executing subtask 4/4: generate_report
🎉 Executor completed all subtasks for plan
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## License

MIT License