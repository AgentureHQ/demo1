import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from enum import Enum
import uuid
import time


class MessageType(Enum):
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    STATUS_UPDATE = "status_update"
    COLLABORATION_REQUEST = "collaboration_request"
    RESULT = "result"


@dataclass
class Message:
    id: str
    sender: str
    recipient: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: float
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'sender': self.sender,
            'recipient': self.recipient,
            'message_type': self.message_type.value,
            'content': self.content,
            'timestamp': self.timestamp
        }


class Agent(ABC):
    def __init__(self, name: str, coordinator=None):
        self.name = name
        self.coordinator = coordinator
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.is_running = False
        
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    async def send_message(self, recipient: str, message_type: MessageType, content: Dict[str, Any]):
        message = Message(
            id=str(uuid.uuid4()),
            sender=self.name,
            recipient=recipient,
            message_type=message_type,
            content=content,
            timestamp=time.time()
        )
        
        if self.coordinator:
            await self.coordinator.route_message(message)
    
    async def receive_message(self, message: Message):
        await self.message_queue.put(message)
    
    async def start(self):
        self.is_running = True
        print(f"🤖 {self.name} agent started")
        
        while self.is_running:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                await self.handle_message(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"❌ Error in {self.name}: {e}")
    
    async def handle_message(self, message: Message):
        print(f"📨 {self.name} received {message.message_type.value} from {message.sender}")
        
        if message.message_type == MessageType.TASK_REQUEST:
            result = await self.process_task(message.content)
            await self.send_message(
                message.sender,
                MessageType.TASK_RESPONSE,
                {"result": result, "original_task_id": message.id}
            )
        elif message.message_type == MessageType.COLLABORATION_REQUEST:
            await self.handle_collaboration_request(message)
    
    async def handle_collaboration_request(self, message: Message):
        pass
    
    async def stop(self):
        self.is_running = False
        print(f"🛑 {self.name} agent stopped")