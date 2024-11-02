from backend.models.debate import DebateState, DebateConfig
from backend.services.openai_service import OpenAIService
import uuid

class DebateService:
    def __init__(self):
        self.openai = OpenAIService()
        self.active_debates = {}  # Simple in-memory storage
    
    async def create_debate(self, config: DebateConfig) -> DebateState:
        debate_id = str(uuid.uuid4())
        debate = DebateState(
            id=debate_id,
            config=config
        )
        self.active_debates[debate_id] = debate
        return debate
    
    async def process_turn(self, debate_id: str, content: str) -> DebateState:
        debate = self.active_debates.get(debate_id)
        if not debate:
            raise ValueError("Debate not found")
        
        # Add turn content
        debate.turns.append(content)
        debate.current_turn += 1
        
        # Generate CPU response if needed
        if (debate.config.player2_type == PlayerType.CPU and 
            debate.current_turn % 2 == 1):
            cpu_response = await self._generate_cpu_response(debate)
            debate.turns.append(cpu_response)
            debate.current_turn += 1
        
        # Check if debate is complete
        if debate.current_turn >= debate.config.max_turns * 2:
            debate.status = "completed"
        
        return debate
    
    async def _generate_cpu_response(self, debate: DebateState) -> str:
        prompt = self._construct_prompt(debate)
        return await self.openai.get_completion(prompt)
    
    def _construct_prompt(self, debate: DebateState) -> str:
        current_figure = debate.config.figure2
        previous_turns = debate.turns
        
        return f"""You are {current_figure.name} from {current_figure.era}.
Your expertise includes {', '.join(current_figure.expertise)}.
You are debating about {debate.config.topic}.
The debate takes place in {debate.config.location}.

Previous turns in the debate:
{chr(10).join(previous_turns)}

Provide your response to the previous arguments, staying in character as {current_figure.name}.
"""