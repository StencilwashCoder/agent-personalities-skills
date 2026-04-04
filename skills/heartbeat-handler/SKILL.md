# heartbeat-handler

Handle OpenClaw heartbeat events by checking goals and orchestrating subagents.

## Purpose

This skill provides a standardized way to handle heartbeat events:
1. Read GOALS.md to check for active goals
2. If goals exist → spawn 1 subagent per goal
3. If no goals → return HEARTBEAT_OK
4. Log all actions appropriately

## Usage

```bash
# Execute heartbeat handling
heartbeat-handle
```

## Behavior

### When Goals Exist
- Spawns 1 subagent per active goal
- Logs orchestration action to GOAL_LOG.md
- Reports: "Spawned N subagents for parallel goal execution"
- Each subagent works independently

### When No Goals
- Returns: HEARTBEAT_OK

## Files

- Input: `memory/GOALS.md`
- Output: `memory/GOAL_LOG.md`
- Log: Console output

## Implementation

```javascript
// Pseudocode
function handleHeartbeat() {
  const goals = readGoals();
  const activeGoals = goals.filter(g => !g.complete);
  
  if (activeGoals.length === 0) {
    return "HEARTBEAT_OK";
  }
  
  // Spawn subagent per goal
  activeGoals.forEach((goal, i) => {
    spawnSubagent({
      task: `Work on Goal #${i+1}: ${goal.title}`,
      goal: goal
    });
  });
  
  logToGoalLog(`Spawned ${activeGoals.length} subagents`);
  
  return `Spawned ${activeGoals.length} subagents for Goals: ${activeGoals.map(g => g.title).join(', ')}`;
}
```

## Notes

- This counts as ONE action (orchestration)
- Subagents work in parallel and report results independently
- Always check GOALS.md before deciding on HEARTBEAT_OK
