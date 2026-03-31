---
name: testing-debugging
description: Testing and debugging workflows for Codex. Use when writing tests, debugging failing tests, analyzing error logs, or troubleshooting code issues. Provides practical patterns for test-driven development, test organization, debugging strategies, and error analysis specifically optimized for AI-assisted coding sessions with Codex.
---

# Testing & Debugging for Codex

Efficient testing and debugging workflows optimized for Codex. Focuses on fast iteration, clear error analysis, and patterns that work well with AI-assisted development.

## Quick Start

### Run Tests
```bash
# Run all tests
npm test

# Run specific test file
npm test -- src/utils/helpers.test.js

# Run with watch mode
npm test -- --watch

# Run with coverage
npm test -- --coverage
```

### Debug a Failing Test
```bash
# 1. Run the specific failing test
npm test -- --testNamePattern="should calculate total"

# 2. Ask Codex to analyze
codex "This test is failing, help me debug it"
```

## Test Writing with Codex

### Generate Tests from Implementation
```bash
# Share function with Codex and ask for tests
codex "Write comprehensive tests for this function including edge cases and error handling:
$(cat src/utils/validator.js)"
```

### Unit Test Template
```javascript
// utils/calculator.test.js
import { calculateTotal, applyDiscount } from './calculator';

describe('calculateTotal', () => {
  it('should sum item prices correctly', () => {
    const items = [{ price: 10 }, { price: 20 }];
    expect(calculateTotal(items)).toBe(30);
  });

  it('should handle empty cart', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('should handle decimal prices', () => {
    const items = [{ price: 10.99 }, { price: 5.50 }];
    expect(calculateTotal(items)).toBeCloseTo(16.49);
  });
});
```

### Test Organization
```
src/
  components/
    Button.tsx
    Button.test.tsx          # Component tests alongside source
  utils/
    helpers.ts
    helpers.test.ts          # Unit tests alongside source
  e2e/
    checkout.spec.ts         # E2E tests in separate folder
  __mocks__/                 # Mock data and modules
    api.ts
```

## Common Test Patterns

### Async Testing
```javascript
it('should fetch user data', async () => {
  const user = await fetchUser(123);
  expect(user.id).toBe(123);
  expect(user.name).toBeDefined();
});

// Or with resolves/rejects
it('should resolve with user', () => {
  return expect(fetchUser(123)).resolves.toHaveProperty('id');
});
```

### Mocking with Jest
```javascript
import { jest } from '@jest/globals';

// Mock return values
const mockFn = jest.fn();
mockFn.mockReturnValue('mocked');
mockFn.mockResolvedValue({ data: [] });
mockFn.mockRejectedValue(new Error('fail'));

// Verify calls
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
expect(mockFn).toHaveBeenCalledTimes(1);

// Clear mocks between tests
beforeEach(() => {
  jest.clearAllMocks();
});
```

### Setup and Teardown
```javascript
beforeAll(() => {
  // Run once before all tests
});

beforeEach(() => {
  // Run before each test
});

afterEach(() => {
  // Clean up after each test
});

afterAll(() => {
  // Final cleanup
});
```

## Debugging Workflows

### The DEBUG Loop with Codex

When tests fail or bugs appear:

```bash
# 1. REPRODUCE - Get the error
npm test 2>&1 | head -50

# 2. ISOLATE - Run just that test
npm test -- --testNamePattern="failing test"

# 3. INSPECT - Share context with Codex
codex "Debug this failing test:
Test: $(cat src/utils/api.test.ts)
Impl: $(cat src/utils/api.ts)
Error: $(npm test -- api.test 2>&1 | tail -30)"

# 4. FIX - Implement solution
codex "Fix this based on the error above"

# 5. VERIFY - Run test again
npm test -- --testNamePattern="failing test"
```

### Reading Error Logs

**Parse Stack Traces:**
```bash
# Get just the error
npm test 2>&1 | grep -A 5 "FAIL\|Error\|expected"

# Get full output for Codex analysis
npm test 2>&1 > /tmp/test-output.txt
codex "Analyze this test failure: $(cat /tmp/test-output.txt)"
```

**Common Error Patterns:**
```
● Test suite failed to run
  → Missing import or syntax error in test file

● expect(received).toBe(expected)
  → Assertion failed, check values

● Cannot find module
  → Missing dependency or wrong import path

● Async callback was not invoked
  → Missing await or done() in async test

● Network Error
  → Unmocked API call in test
```

### Effective Codex Debugging Prompts

**Share Context Efficiently:**
```bash
# Share function + test + error
codex "Debug this:
Function: $(cat src/utils/api.ts)
Test: $(cat src/utils/api.test.ts)
Error: $(npm test -- api.test 2>&1 | tail -30)"
```

**Ask Specific Questions:**
```bash
# Good prompts
codex "Why is this async test timing out?"
codex "What's wrong with this mock setup?"
codex "How do I test this error case?"

# Bad prompts
codex "Fix this"  # Too vague
```

## Test-Driven Development (TDD) with Codex

### Red-Green-Refactor Loop

**1. Red - Write Failing Test:**
```bash
codex "Write a test for a function that validates email addresses"
# Creates validator.test.js with failing tests
```

**2. Green - Implement to Pass:**
```bash
codex "Implement the validateEmail function to pass these tests:
$(cat validator.test.js)"
```

**3. Refactor - Clean Up:**
```bash
codex "Refactor this code while keeping tests passing:
$(cat validator.js)"
```

### TDD Workflow Commands
```bash
# Watch mode for rapid TDD
npm test -- --watch --testPathPattern=validator

# Run only changed files
npm test -- --changedSince=main

# Run related to changed files
npm test -- --findRelatedTests src/utils/validator.js
```

## Integration & E2E Testing

### API Integration Tests
```javascript
// tests/api.test.js
import { setupServer } from 'msw/node';
import { rest } from 'msw';

const server = setupServer(
  rest.get('/api/user', (req, res, ctx) => {
    return res(ctx.json({ id: 1, name: 'Test' }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('fetches user from API', async () => {
  const user = await getUser();
  expect(user.name).toBe('Test');
});
```

### E2E with Playwright
```javascript
// e2e/checkout.spec.ts
import { test, expect } from '@playwright/test';

test('user can complete checkout', async ({ page }) => {
  await page.goto('/shop');
  await page.click('[data-testid="add-to-cart"]');
  await page.click('[data-testid="checkout"]');
  await page.fill('[name="email"]', 'test@example.com');
  await page.click('[type="submit"]');
  
  await expect(page).toHaveURL('/checkout/success');
});
```

**Run E2E Tests:**
```bash
# Run all E2E tests
npx playwright test

# Run specific test
npx playwright test checkout.spec.ts

# Run with UI mode
npx playwright test --ui

# Debug specific test
npx playwright test checkout.spec.ts --debug
```

## Test Coverage

### Coverage Reports
```bash
# Generate coverage report
npm test -- --coverage

# Open HTML report
open coverage/lcov-report/index.html

# Check coverage thresholds
npm test -- --coverage --coverageThreshold='{"global":{"branches":80}}'
```

**Focus on What Matters:**
```bash
# View uncovered lines
cat coverage/lcov.info | grep -A 2 "LF:" | head -20

# Ask Codex to add tests for uncovered code
codex "Add tests to cover these uncovered lines:
$(cat coverage/lcov.info)"
```

### Coverage Best Practices
- Aim for 80%+ coverage on business logic
- Don't obsess over 100% coverage
- Focus on critical paths and edge cases
- Mock external dependencies
- Test behavior, not implementation

## Troubleshooting Common Issues

### Flaky Tests
```bash
# Run test multiple times to detect flakiness
for i in {1..10}; do npm test -- --testNamePattern="flaky test"; done

# Ask Codex to stabilize
codex "This test is flaky, help me make it deterministic:
$(cat flaky.test.js)"
```

### Slow Tests
```bash
# Find slowest tests
npm test -- --verbose 2>&1 | grep -E "PASS|FAIL" | sort -k3 -n

# Run in parallel
npm test -- --maxWorkers=4
```

### Memory Issues
```bash
# Run with increased memory
node --max-old-space-size=4096 node_modules/.bin/jest

# Isolate memory-heavy tests
npm test -- --runInBand --logHeapUsage
```

## Debug Commands Quick Reference

```bash
# List all tests without running
npm test -- --listTests

# Run tests matching pattern
npm test -- --testPathPattern="api"

# Run only failed tests from last run
npm test -- --onlyFailures

# Verbose output
npm test -- --verbose

# No cache (fresh run)
npm test -- --no-cache

# Show seed for randomization
npm test -- --showSeed
```

## Codex-Specific Tips

### 1. Start with the Test
Let Codex understand requirements through test cases first.

### 2. Provide Context
Share the function, its usage, and expected behavior.

### 3. Be Specific
Ask for specific test cases (edge cases, error cases).

### 4. Iterate
Run tests, share errors, ask for fixes.

### 5. Review Coverage
Ask Codex to identify untested code paths.

### Effective Prompts

**Generate comprehensive tests:**
```bash
codex "Write unit tests for this function including edge cases and error handling:
$(cat utils.js)"
```

**Fix failing test:**
```bash
codex "This test is failing with 'Expected 5 but received undefined'. Fix the implementation:
$(cat code.js)"
```

**Add missing coverage:**
```bash
codex "These lines are uncovered. Add tests:
$(cat uncovered-lines.txt)"
```

**Debug complex failure:**
```bash
codex "Debug this async test timeout.
Test: $(cat test.js)
Implementation: $(cat impl.js)"
```

## Snapshot Testing

```javascript
// Component snapshot test
import { render } from '@testing-library/react';
import Button from './Button';

it('renders correctly', () => {
  const { container } = render(<Button>Click me</Button>);
  expect(container).toMatchSnapshot();
});
```

**Update snapshots:**
```bash
# Update all snapshots
npm test -- --updateSnapshot

# Update specific snapshot
npm test -- --updateSnapshot --testNamePattern="Button"
```

## Property-Based Testing

```javascript
import fc from 'fast-check';

it('should always return positive for positive inputs', () => {
  fc.assert(
    fc.property(fc.integer({ min: 1 }), (n) => {
      return calculate(n) > 0;
    })
  );
});
```
