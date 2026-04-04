const { validateMcpConfig, McpValidator } = require('../src/validator');
const path = require('path');
const fs = require('fs');

describe('McpValidator', () => {
  describe('validateMcpConfig', () => {
    test('validates correct stdio configuration', () => {
      const configPath = path.join(__dirname, 'fixtures', 'valid-mcp.json');
      const result = validateMcpConfig(configPath);
      
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('detects errors in invalid configuration', () => {
      const configPath = path.join(__dirname, 'fixtures', 'invalid-mcp.json');
      const result = validateMcpConfig(configPath);
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });

    test('detects duplicate tool names', () => {
      const validator = new McpValidator();
      const config = {
        mcpServers: {
          test: {
            transport: 'stdio',
            command: 'node',
            args: ['server.js'],
            tools: [
              { name: 'tool1', description: 'First' },
              { name: 'tool1', description: 'Duplicate' }
            ]
          }
        }
      };

      fs.writeFileSync('/tmp/test-dup.json', JSON.stringify(config));
      const result = validator.validate('/tmp/test-dup.json');
      
      expect(result.errors.some(e => e.message.includes('Duplicate'))).toBe(true);
      fs.unlinkSync('/tmp/test-dup.json');
    });

    test('warns about insecure HTTP URLs', () => {
      const validator = new McpValidator();
      const config = {
        mcpServers: {
          test: {
            transport: 'http',
            url: 'http://api.example.com/mcp',
            auth: { type: 'bearer', tokenEnv: 'TOKEN' }
          }
        }
      };

      fs.writeFileSync('/tmp/test-http.json', JSON.stringify(config));
      const result = validator.validate('/tmp/test-http.json');
      
      expect(result.warnings.some(w => w.message.includes('insecure'))).toBe(true);
      fs.unlinkSync('/tmp/test-http.json');
    });

    test('requires auth for remote HTTP servers', () => {
      const validator = new McpValidator();
      const config = {
        mcpServers: {
          test: {
            transport: 'http',
            url: 'https://api.example.com/mcp'
          }
        }
      };

      fs.writeFileSync('/tmp/test-auth.json', JSON.stringify(config));
      const result = validator.validate('/tmp/test-auth.json');
      
      expect(result.warnings.some(w => w.message.includes('Authentication recommended'))).toBe(true);
      fs.unlinkSync('/tmp/test-auth.json');
    });

    test('validates bearer auth requires tokenEnv', () => {
      const validator = new McpValidator();
      const config = {
        mcpServers: {
          test: {
            transport: 'http',
            url: 'https://api.example.com/mcp',
            auth: { type: 'bearer' }
          }
        }
      };

      fs.writeFileSync('/tmp/test-bearer.json', JSON.stringify(config));
      const result = validator.validate('/tmp/test-bearer.json');
      
      expect(result.errors.some(e => e.message.includes('tokenEnv'))).toBe(true);
      fs.unlinkSync('/tmp/test-bearer.json');
    });
  });

  describe('custom rules', () => {
    test('runs pattern-based custom rules', () => {
      const customRules = {
        rules: [{
          id: 'no-localhost',
          severity: 'error',
          pattern: 'localhost',
          message: 'No localhost allowed'
        }]
      };

      const validator = new McpValidator({ customRules });
      const config = {
        mcpServers: {
          test: {
            transport: 'http',
            url: 'http://localhost:8080/mcp'
          }
        }
      };

      fs.writeFileSync('/tmp/test-rule.json', JSON.stringify(config));
      const result = validator.validate('/tmp/test-rule.json');
      
      expect(result.errors.some(e => e.message === 'No localhost allowed')).toBe(true);
      fs.unlinkSync('/tmp/test-rule.json');
    });
  });
});
