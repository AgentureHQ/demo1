#!/usr/bin/env python3
"""
Multi-Agent Collaboration Demo
A demonstration of two agents working together to complete user tasks.

Usage:
  python main.py                    # Run interactive mode
  python main.py --demo             # Run all demo scenarios
  python main.py --demo <scenario>  # Run specific demo scenario
"""

import asyncio
import sys
from coordinator import TaskCoordinator, DemoScenarios, create_demo_system


class UserInterface:
    """Simple command-line interface for interacting with the agent system"""
    
    def __init__(self, coordinator: TaskCoordinator):
        self.coordinator = coordinator
        self.running = True
    
    async def start_interactive_mode(self):
        print("🎯 Multi-Agent Collaboration Demo")
        print("=" * 40)
        print("Two agents (Planner & Executor) are ready to collaborate!")
        print("Type 'help' for commands, 'quit' to exit")
        print()
        
        # Start agent tasks in background
        agent_tasks = await self.coordinator.start_agents()
        
        try:
            while self.running:
                try:
                    user_input = input("💭 Enter task: ").strip()
                    
                    if not user_input:
                        continue
                    
                    await self.handle_user_input(user_input)
                    
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
                except EOFError:
                    break
        
        finally:
            await self.coordinator.stop_agents()
            for task in agent_tasks:
                task.cancel()
    
    async def handle_user_input(self, user_input: str):
        command = user_input.lower()
        
        if command in ['quit', 'exit', 'q']:
            self.running = False
            return
        
        elif command in ['help', 'h']:
            self.show_help()
            return
        
        elif command in ['status', 's']:
            self.coordinator.print_status()
            return
        
        elif command.startswith('history'):
            parts = command.split()
            limit = 10
            if len(parts) > 1 and parts[1].isdigit():
                limit = int(parts[1])
            self.show_message_history(limit)
            return
        
        elif command == 'demo':
            await self.run_demo_menu()
            return
        
        # Regular task submission
        task_id = await self.coordinator.submit_user_task(user_input)
        print(f"✅ Task submitted with ID: {task_id}")
        print("🔄 Agents are collaborating... (watch the output above)")
        print()
    
    def show_help(self):
        print("\n📖 Available Commands:")
        print("  help, h           - Show this help message")
        print("  status, s         - Show system status")
        print("  history [n]       - Show last n messages (default 10)")
        print("  demo              - Run demo scenarios menu")
        print("  quit, exit, q     - Exit the application")
        print("  <any text>        - Submit task to agents")
        print()
        print("📝 Example tasks:")
        print("  • Analyze the quarterly sales data")
        print("  • Calculate compound interest for investment")
        print("  • Process customer feedback text")
        print("  • Scrape competitor pricing information")
        print()
    
    def show_message_history(self, limit: int):
        messages = self.coordinator.get_message_history(limit)
        
        if not messages:
            print("📭 No messages in history")
            return
        
        print(f"\n📜 Last {len(messages)} messages:")
        print("-" * 40)
        
        for msg in messages:
            timestamp = msg['timestamp']
            sender = msg['sender']
            recipient = msg['recipient']
            msg_type = msg['message_type']
            
            print(f"[{timestamp:.0f}] {sender} → {recipient}: {msg_type}")
        
        print("-" * 40 + "\n")
    
    async def run_demo_menu(self):
        print("\n🎭 Demo Scenarios:")
        print("1. Data Analysis")
        print("2. Calculation")  
        print("3. Text Processing")
        print("4. Web Scraping")
        print("5. Run All Demos")
        print("0. Back to main menu")
        
        try:
            choice = input("\nSelect demo (0-5): ").strip()
            
            demos = DemoScenarios(self.coordinator)
            
            if choice == '1':
                await demos.run_data_analysis_demo()
            elif choice == '2':
                await demos.run_calculation_demo()
            elif choice == '3':
                await demos.run_text_processing_demo()
            elif choice == '4':
                await demos.run_web_scraping_demo()
            elif choice == '5':
                await demos.run_all_demos()
            elif choice == '0':
                return
            else:
                print("❌ Invalid choice")
                
        except (KeyboardInterrupt, EOFError):
            pass
        
        print()


async def main():
    """Main entry point"""
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--demo':
            await run_demo_mode(sys.argv[2:])
        else:
            print("Usage: python main.py [--demo [scenario]]")
            sys.exit(1)
    else:
        await run_interactive_mode()


async def run_interactive_mode():
    """Run the interactive user interface"""
    coordinator = await create_demo_system()
    ui = UserInterface(coordinator)
    await ui.start_interactive_mode()


async def run_demo_mode(args):
    """Run demo scenarios automatically"""
    coordinator = await create_demo_system()
    demos = DemoScenarios(coordinator)
    
    # Start agents
    agent_tasks = await coordinator.start_agents()
    
    try:
        if not args:
            # Run all demos
            await demos.run_all_demos()
        else:
            scenario = args[0].lower()
            
            if scenario in ['data', 'analysis']:
                await demos.run_data_analysis_demo()
            elif scenario in ['calc', 'calculation']:
                await demos.run_calculation_demo()
            elif scenario in ['text', 'processing']:
                await demos.run_text_processing_demo()
            elif scenario in ['web', 'scraping']:
                await demos.run_web_scraping_demo()
            else:
                print(f"❌ Unknown demo scenario: {scenario}")
                print("Available: data, calc, text, web")
                return
    
    finally:
        await asyncio.sleep(2)  # Let final messages process
        await coordinator.stop_agents()
        for task in agent_tasks:
            task.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)