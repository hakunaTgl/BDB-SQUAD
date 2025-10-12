"""
AetherOS Recursive Meta-Prompting (RMP) Orchestrator
Self-optimizing agent swarm with utility-based reflexes

This module implements the cognitive control layer that enables
autonomous problem-solving, task delegation, and continuous self-improvement.
"""

import asyncio
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
from loguru import logger


class AgentRole(Enum):
    """Specialized agent roles in the swarm"""
    ORCHESTRATOR = "orchestrator"
    PIGC_ARCHITECT = "pigc_architect"
    MEMORY_AGENT = "memory_agent"
    ETHICS_AGENT = "ethics_agent"
    VIDEO_GENERATOR = "video_generator"
    AUDIO_GENERATOR = "audio_generator"
    VOICE_SYNTHESIZER = "voice_synthesizer"
    QUALITY_EVALUATOR = "quality_evaluator"


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class Task:
    """Represents a delegated task in the swarm"""
    task_id: str
    role: AgentRole
    description: str
    priority: float  # 0 to 1
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MetaPrompt:
    """Recursive meta-prompt template"""
    template_id: str
    version: int
    content: str
    performance_score: float = 0.0
    usage_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    parent_template_id: Optional[str] = None


class BaseAgent:
    """Base agent with utility-based reflex capabilities"""
    
    def __init__(self, role: AgentRole, capabilities: List[str]):
        self.role = role
        self.capabilities = capabilities
        self.task_queue: List[Task] = []
        self.performance_history: List[float] = []
        
        logger.info(f"Initialized {role.value} agent with capabilities: {capabilities}")
    
    async def execute_task(self, task: Task) -> Any:
        """Execute a task based on role capabilities"""
        raise NotImplementedError("Subclasses must implement execute_task")
    
    def evaluate_utility(self, task: Task) -> float:
        """
        Calculate utility score for a task
        
        Utility = (task_priority * capability_match) - estimated_cost
        """
        # Check capability match
        capability_match = 1.0  # Default full match
        
        # Estimate computational cost
        estimated_cost = 0.3  # Base cost
        
        # Factor in current load
        load_penalty = len(self.task_queue) * 0.1
        
        # Factor in historical performance
        avg_performance = sum(self.performance_history[-10:]) / max(len(self.performance_history[-10:]), 1) if self.performance_history else 0.5
        
        utility = (task.priority * capability_match * avg_performance) - estimated_cost - load_penalty
        
        return max(0.0, utility)
    
    def add_to_queue(self, task: Task):
        """Add task to agent's queue"""
        self.task_queue.append(task)
        self.task_queue.sort(key=lambda t: t.priority, reverse=True)


class OrchestratorAgent(BaseAgent):
    """Master orchestrator that coordinates the agent swarm"""
    
    def __init__(self):
        super().__init__(
            role=AgentRole.ORCHESTRATOR,
            capabilities=[
                "task_decomposition",
                "delegation",
                "coordination",
                "meta_prompt_generation"
            ]
        )
        
        self.agents: Dict[AgentRole, BaseAgent] = {}
        self.tasks: Dict[str, Task] = {}
        self.meta_prompts: Dict[str, MetaPrompt] = {}
        self.current_meta_prompt: Optional[MetaPrompt] = None
    
    async def execute_task(self, task: Task) -> Any:
        """Orchestrate complex task execution"""
        
        logger.info(f"Orchestrating task: {task.description}")
        
        # Generate/select meta-prompt
        meta_prompt = await self.select_meta_prompt(task)
        
        # Decompose into subtasks
        subtasks = await self.decompose_task(task, meta_prompt)
        
        # Delegate subtasks
        results = await self.delegate_and_execute(subtasks)
        
        # Aggregate results
        final_result = await self.aggregate_results(results)
        
        # Evaluate performance and update meta-prompt
        await self.evaluate_and_update_meta_prompt(meta_prompt, final_result)
        
        return final_result
    
    async def select_meta_prompt(self, task: Task) -> MetaPrompt:
        """Select or generate appropriate meta-prompt for task"""
        
        # Check if we have high-performing prompts for this task type
        relevant_prompts = [
            mp for mp in self.meta_prompts.values()
            if mp.performance_score > 0.7
        ]
        
        if relevant_prompts:
            # Select best performing prompt
            best_prompt = max(relevant_prompts, key=lambda p: p.performance_score)
            logger.debug(f"Selected meta-prompt {best_prompt.template_id} (score: {best_prompt.performance_score:.2f})")
            return best_prompt
        
        # Generate new meta-prompt
        new_prompt = await self.generate_meta_prompt(task)
        self.meta_prompts[new_prompt.template_id] = new_prompt
        return new_prompt
    
    async def generate_meta_prompt(self, task: Task) -> MetaPrompt:
        """Generate new meta-prompt using recursive refinement"""
        
        template_id = f"mp_{len(self.meta_prompts)}_{datetime.now().timestamp()}"
        
        # Base meta-prompt structure (SPARC-inspired)
        content = f"""
# Meta-Prompt for: {task.description}

## SITUATION
Analyze the current creative task and its requirements.
Task: {task.description}
Priority: {task.priority}
Metadata: {task.metadata}

## PROBLEM
Identify the core challenges and constraints:
- What needs to be generated?
- What quality standards must be met?
- What ethical considerations apply?
- What resources are available?

## ACTIONS
Define the execution strategy:
1. Decompose into atomic subtasks
2. Assign to specialized agents based on utility
3. Establish dependency chains
4. Set quality checkpoints

## RESULT
Specify success criteria:
- Output format and specifications
- Quality metrics and thresholds
- Ethical compliance verification
- Performance benchmarks

## CRITIQUE
Evaluate the approach:
- Potential failure modes
- Alternative strategies
- Optimization opportunities
- Learning points for future iterations
"""
        
        meta_prompt = MetaPrompt(
            template_id=template_id,
            version=1,
            content=content,
            performance_score=0.5  # Initial neutral score
        )
        
        logger.info(f"Generated new meta-prompt {template_id}")
        return meta_prompt
    
    async def decompose_task(self, task: Task, meta_prompt: MetaPrompt) -> List[Task]:
        """Decompose complex task into subtasks"""
        
        subtasks = []
        
        # Analyze task type from description
        description_lower = task.description.lower()
        
        # Always start with affective analysis
        subtasks.append(Task(
            task_id=f"{task.task_id}_affective",
            role=AgentRole.ETHICS_AGENT,
            description="Analyze emotional and cultural context",
            priority=1.0,
            metadata={'parent_task': task.task_id}
        ))
        
        # Memory retrieval
        subtasks.append(Task(
            task_id=f"{task.task_id}_memory",
            role=AgentRole.MEMORY_AGENT,
            description="Retrieve relevant context from NGM",
            priority=0.9,
            metadata={'parent_task': task.task_id}
        ))
        
        # Content generation tasks based on type
        if 'video' in description_lower or 'visual' in description_lower:
            subtasks.append(Task(
                task_id=f"{task.task_id}_video",
                role=AgentRole.VIDEO_GENERATOR,
                description="Generate video content",
                priority=0.8,
                dependencies=[f"{task.task_id}_affective", f"{task.task_id}_memory"],
                metadata={'parent_task': task.task_id}
            ))
        
        if 'audio' in description_lower or 'music' in description_lower:
            subtasks.append(Task(
                task_id=f"{task.task_id}_audio",
                role=AgentRole.AUDIO_GENERATOR,
                description="Generate audio/music content",
                priority=0.8,
                dependencies=[f"{task.task_id}_affective"],
                metadata={'parent_task': task.task_id}
            ))
        
        if 'voice' in description_lower or 'dialogue' in description_lower:
            subtasks.append(Task(
                task_id=f"{task.task_id}_voice",
                role=AgentRole.VOICE_SYNTHESIZER,
                description="Synthesize voice content",
                priority=0.7,
                dependencies=[f"{task.task_id}_affective"],
                metadata={'parent_task': task.task_id}
            ))
        
        # Quality evaluation
        subtasks.append(Task(
            task_id=f"{task.task_id}_quality",
            role=AgentRole.QUALITY_EVALUATOR,
            description="Evaluate output quality and ethics",
            priority=0.9,
            dependencies=[t.task_id for t in subtasks if t.role in [
                AgentRole.VIDEO_GENERATOR,
                AgentRole.AUDIO_GENERATOR,
                AgentRole.VOICE_SYNTHESIZER
            ]],
            metadata={'parent_task': task.task_id}
        ))
        
        logger.info(f"Decomposed task into {len(subtasks)} subtasks")
        return subtasks
    
    async def delegate_and_execute(self, subtasks: List[Task]) -> Dict[str, Any]:
        """Delegate subtasks to agents and execute in parallel"""
        
        results = {}
        
        # Build dependency graph
        dependency_graph = {task.task_id: task.dependencies for task in subtasks}
        
        # Execute tasks respecting dependencies
        completed = set()
        pending = {task.task_id: task for task in subtasks}
        
        while pending:
            # Find tasks ready to execute (dependencies met)
            ready_tasks = [
                task for task_id, task in pending.items()
                if all(dep in completed for dep in task.dependencies)
            ]
            
            if not ready_tasks:
                logger.error("Circular dependency detected or no ready tasks")
                break
            
            # Execute ready tasks in parallel
            execute_coroutines = []
            for task in ready_tasks:
                agent = self.agents.get(task.role)
                if agent:
                    execute_coroutines.append(self._execute_with_agent(agent, task))
                else:
                    logger.warning(f"No agent available for role {task.role.value}")
            
            if execute_coroutines:
                task_results = await asyncio.gather(*execute_coroutines, return_exceptions=True)
                
                for task, result in zip(ready_tasks, task_results):
                    if isinstance(result, Exception):
                        logger.error(f"Task {task.task_id} failed: {result}")
                        task.status = TaskStatus.FAILED
                        task.error = str(result)
                    else:
                        task.status = TaskStatus.COMPLETED
                        task.result = result
                        results[task.task_id] = result
                        completed.add(task.task_id)
                    
                    task.completed_at = datetime.now()
                    del pending[task.task_id]
        
        return results
    
    async def _execute_with_agent(self, agent: BaseAgent, task: Task) -> Any:
        """Execute task with specific agent"""
        task.status = TaskStatus.IN_PROGRESS
        logger.debug(f"Executing {task.task_id} with {agent.role.value}")
        
        result = await agent.execute_task(task)
        
        # Update agent performance history
        performance = 1.0 if task.status != TaskStatus.FAILED else 0.0
        agent.performance_history.append(performance)
        
        return result
    
    async def aggregate_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate subtask results into final output"""
        
        aggregated = {
            'status': 'success',
            'components': results,
            'metadata': {
                'task_count': len(results),
                'timestamp': datetime.now().isoformat()
            }
        }
        
        # Check for failures
        if any(isinstance(r, Exception) for r in results.values()):
            aggregated['status'] = 'partial_failure'
        
        return aggregated
    
    async def evaluate_and_update_meta_prompt(
        self,
        meta_prompt: MetaPrompt,
        result: Dict[str, Any]
    ):
        """Evaluate performance and update meta-prompt"""
        
        # Calculate performance score
        performance_score = 1.0 if result['status'] == 'success' else 0.5
        
        # Update meta-prompt statistics
        meta_prompt.usage_count += 1
        
        # Update performance score with exponential moving average
        alpha = 0.3
        meta_prompt.performance_score = (
            alpha * performance_score +
            (1 - alpha) * meta_prompt.performance_score
        )
        
        logger.info(f"Meta-prompt {meta_prompt.template_id} score: {meta_prompt.performance_score:.2f}")
        
        # If performance is low, consider generating refined version
        if meta_prompt.performance_score < 0.6 and meta_prompt.usage_count > 5:
            await self.refine_meta_prompt(meta_prompt)
    
    async def refine_meta_prompt(self, meta_prompt: MetaPrompt):
        """Generate refined version of underperforming meta-prompt"""
        
        new_template_id = f"{meta_prompt.template_id}_v{meta_prompt.version + 1}"
        
        # Create refined version (in production, use LLM for refinement)
        refined_content = meta_prompt.content + "\n\n## REFINEMENTS\n- Enhanced error handling\n- Improved task decomposition\n- Better resource allocation"
        
        refined_prompt = MetaPrompt(
            template_id=new_template_id,
            version=meta_prompt.version + 1,
            content=refined_content,
            performance_score=meta_prompt.performance_score,
            parent_template_id=meta_prompt.template_id
        )
        
        self.meta_prompts[new_template_id] = refined_prompt
        
        logger.info(f"Refined meta-prompt: {meta_prompt.template_id} -> {new_template_id}")
    
    def register_agent(self, agent: BaseAgent):
        """Register agent in the swarm"""
        self.agents[agent.role] = agent
        logger.info(f"Registered agent: {agent.role.value}")
    
    def get_swarm_status(self) -> Dict[str, Any]:
        """Get current status of the agent swarm"""
        return {
            'agents': {
                role.value: {
                    'queue_size': len(agent.task_queue),
                    'avg_performance': sum(agent.performance_history[-10:]) / max(len(agent.performance_history[-10:]), 1) if agent.performance_history else 0.0
                }
                for role, agent in self.agents.items()
            },
            'tasks': {
                'total': len(self.tasks),
                'pending': sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING),
                'in_progress': sum(1 for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS),
                'completed': sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED),
                'failed': sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
            },
            'meta_prompts': {
                'total': len(self.meta_prompts),
                'high_performing': sum(1 for mp in self.meta_prompts.values() if mp.performance_score > 0.7)
            }
        }


class RecursiveMetaPromptingOrchestrator:
    """
    Main RMP orchestration system
    
    Coordinates the self-optimizing agent swarm with recursive meta-prompting
    """
    
    def __init__(self):
        """Initialize the RMP orchestrator"""
        
        # Create orchestrator agent
        self.orchestrator = OrchestratorAgent()
        
        # Track active sessions
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        logger.info("Initialized Recursive Meta-Prompting Orchestrator")
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        self.orchestrator.register_agent(agent)
    
    async def execute(
        self,
        description: str,
        priority: float = 0.8,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Execute a high-level creative task
        
        Args:
            description: Task description
            priority: Task priority (0-1)
            metadata: Additional context
            
        Returns:
            Execution results
        """
        
        # Create main task
        task_id = f"task_{datetime.now().timestamp()}"
        task = Task(
            task_id=task_id,
            role=AgentRole.ORCHESTRATOR,
            description=description,
            priority=priority,
            metadata=metadata or {}
        )
        
        # Store task
        self.orchestrator.tasks[task_id] = task
        
        # Execute through orchestrator
        result = await self.orchestrator.execute_task(task)
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status"""
        return self.orchestrator.get_swarm_status()


# Example usage
async def example_usage():
    """Example of RMP orchestrator in action"""
    
    # Initialize orchestrator
    rmp = RecursiveMetaPromptingOrchestrator()
    
    # Create and register agents (placeholders for now)
    memory_agent = BaseAgent(AgentRole.MEMORY_AGENT, ["retrieval", "storage"])
    ethics_agent = BaseAgent(AgentRole.ETHICS_AGENT, ["analysis", "validation"])
    
    rmp.register_agent(memory_agent)
    rmp.register_agent(ethics_agent)
    
    # Execute a creative task
    result = await rmp.execute(
        description="Create a 2-minute cinematic video about a child discovering magic",
        priority=0.9,
        metadata={
            'style': 'cinematic',
            'duration': 120,
            'tone': 'wonder'
        }
    )
    
    print(json.dumps(result, indent=2, default=str))
    print(json.dumps(rmp.get_status(), indent=2))


if __name__ == "__main__":
    asyncio.run(example_usage())
