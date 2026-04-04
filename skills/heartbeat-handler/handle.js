#!/usr/bin/env node
/**
 * Heartbeat Handler Skill
 * Handles OpenClaw heartbeat events by checking goals and spawning subagents
 */

const fs = require('fs');
const path = require('path');

const GOALS_PATH = '/root/.openclaw/workspace/memory/GOALS.md';
const GOAL_LOG_PATH = '/root/.openclaw/workspace/memory/GOAL_LOG.md';

function parseGoals(content) {
  const goals = [];
  const goalBlocks = content.split('### ').slice(1);
  
  for (const block of goalBlocks) {
    const lines = block.split('\n');
    const title = lines[0].trim();
    
    const statusMatch = block.match(/\*\*Status:\*\* (🔴|🟡|🟢) ([^\n]+)/);
    const status = statusMatch ? statusMatch[2].trim() : 'unknown';
    
    goals.push({
      title,
      status,
      raw: block
    });
  }
  
  return goals;
}

function readGoals() {
  try {
    const content = fs.readFileSync(GOALS_PATH, 'utf8');
    return parseGoals(content);
  } catch (err) {
    return [];
  }
}

function isActiveGoal(goal) {
  return goal.status.includes('In Progress') || goal.status.includes('Not Started');
}

function logAction(message) {
  const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 16);
  const logEntry = `[${timestamp}] - Heartbeat Orchestration - ${message}\n`;
  
  try {
    fs.appendFileSync(GOAL_LOG_PATH, logEntry);
  } catch (err) {
    console.error('Failed to log:', err);
  }
}

function main() {
  const goals = readGoals();
  const activeGoals = goals.filter(isActiveGoal);
  
  if (activeGoals.length === 0) {
    console.log('HEARTBEAT_OK');
    process.exit(0);
  }
  
  // Spawn subagent instructions
  const goalList = activeGoals.map((g, i) => `${i + 1}. ${g.title}`).join('\n');
  
  console.log(`Spawn ${activeGoals.length} subagents for parallel goal execution:

${goalList}

Each subagent should work independently on its assigned goal and report results when complete.`);
  
  logAction(`Spawned ${activeGoals.length} subagents for: ${activeGoals.map(g => g.title).join(', ')}`);
}

main();
