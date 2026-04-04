/**
 * MCP Configuration Validator
 * Validates against Model Context Protocol specification
 */

const fs = require('fs');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

// MCP JSON Schema (based on official spec)
const mcpSchema = {
  type: 'object',
  required: ['mcpServers'],
  properties: {
    mcpServers: {
      type: 'object',
      additionalProperties: {
        type: 'object',
        required: ['transport'],
        properties: {
          transport: {
            type: 'string',
            enum: ['stdio', 'http', 'sse']
          },
          // stdio transport
          command: { type: 'string' },
          args: {
            type: 'array',
            items: { type: 'string' }
          },
          env: {
            type: 'object',
            additionalProperties: { type: 'string' }
          },
          cwd: { type: 'string' },
          // http/sse transport
          url: { type: 'string', format: 'uri' },
          headers: {
            type: 'object',
            additionalProperties: { type: 'string' }
          },
          auth: {
            type: 'object',
            properties: {
              type: {
                type: 'string',
                enum: ['bearer', 'basic', 'api-key', 'oauth']
              },
              tokenEnv: { type: 'string' },
              usernameEnv: { type: 'string' },
              passwordEnv: { type: 'string' },
              apiKeyEnv: { type: 'string' },
              clientIdEnv: { type: 'string' },
              clientSecretEnv: { type: 'string' }
            }
          },
          // Tools configuration
          tools: {
            type: 'array',
            items: {
              type: 'object',
              required: ['name', 'description'],
              properties: {
                name: { type: 'string' },
                description: { type: 'string' },
                inputSchema: { type: 'object' },
                annotations: {
                  type: 'object',
                  properties: {
                    title: { type: 'string' },
                    readOnlyHint: { type: 'boolean' },
                    destructiveHint: { type: 'boolean' },
                    openWorldHint: { type: 'boolean' }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
};

class McpValidator {
  constructor(options = {}) {
    this.strict = options.strict || false;
    this.skipAuthCheck = options.skipAuthCheck || false;
    this.customRules = options.customRules || null;
    this.errors = [];
    this.warnings = [];
    
    this.ajv = new Ajv({ 
      allErrors: true, 
      strict: false,
      allowUnionTypes: true 
    });
    addFormats(this.ajv);
  }

  validate(configPath) {
    this.errors = [];
    this.warnings = [];

    // Load and parse config
    let config;
    try {
      const content = fs.readFileSync(configPath, 'utf8');
      config = JSON.parse(content);
    } catch (e) {
      this.errors.push({
        path: 'config',
        message: `Failed to parse JSON: ${e.message}`
      });
      return this.getResults();
    }

    // Validate against schema
    const validate = this.ajv.compile(mcpSchema);
    const valid = validate(config);

    if (!valid) {
      for (const error of validate.errors || []) {
        this.errors.push({
          path: error.instancePath || 'config',
          message: error.message,
          schemaPath: error.schemaPath
        });
      }
    }

    // Additional semantic validation
    if (config.mcpServers) {
      for (const [serverName, serverConfig] of Object.entries(config.mcpServers)) {
        this.validateServer(serverName, serverConfig);
      }
    }

    // Run custom rules
    if (this.customRules && this.customRules.rules) {
      this.runCustomRules(config, configPath);
    }

    return this.getResults();
  }

  validateServer(name, config) {
    const path = `mcpServers.${name}`;

    // Transport-specific validation
    switch (config.transport) {
      case 'stdio':
        this.validateStdioServer(path, config);
        break;
      case 'http':
        this.validateHttpServer(path, config);
        break;
      case 'sse':
        this.validateSseServer(path, config);
        break;
    }

    // Tool validation
    if (config.tools) {
      this.validateTools(`${path}.tools`, config.tools);
    }
  }

  validateStdioServer(path, config) {
    if (!config.command) {
      this.errors.push({
        path: `${path}.command`,
        message: 'stdio transport requires "command" field'
      });
    }

    // Check for common stdio servers and validate their requirements
    if (config.command === 'npx' || config.command === 'node') {
      if (!config.args || config.args.length === 0) {
        this.warnings.push({
          path: `${path}.args`,
          message: 'No arguments provided for node/npx command'
        });
      }
    }
  }

  validateHttpServer(path, config) {
    if (!config.url) {
      this.errors.push({
        path: `${path}.url`,
        message: 'HTTP transport requires "url" field'
      });
    } else {
      // Check for insecure URLs
      if (config.url.startsWith('http://') && !config.url.includes('localhost')) {
        this.warnings.push({
          path: `${path}.url`,
          message: 'Using insecure HTTP - consider HTTPS for remote servers'
        });
      }

      // Auth check for remote servers
      if (!this.skipAuthCheck && !config.auth) {
        if (!config.url.includes('localhost') && !config.url.includes('127.0.0.1')) {
          this.warnings.push({
            path: `${path}.auth`,
            message: 'Authentication recommended for remote HTTP servers'
          });
        }
      }
    }

    // Validate auth configuration
    if (config.auth) {
      this.validateAuth(`${path}.auth`, config.auth);
    }
  }

  validateSseServer(path, config) {
    if (!config.url) {
      this.errors.push({
        path: `${path}.url`,
        message: 'SSE transport requires "url" field'
      });
    }
  }

  validateAuth(path, auth) {
    switch (auth.type) {
      case 'bearer':
        if (!auth.tokenEnv) {
          this.errors.push({
            path: `${path}.tokenEnv`,
            message: 'Bearer auth requires "tokenEnv" field'
          });
        }
        break;
      case 'basic':
        if (!auth.usernameEnv || !auth.passwordEnv) {
          this.errors.push({
            path,
            message: 'Basic auth requires "usernameEnv" and "passwordEnv" fields'
          });
        }
        break;
      case 'api-key':
        if (!auth.apiKeyEnv) {
          this.errors.push({
            path: `${path}.apiKeyEnv`,
            message: 'API key auth requires "apiKeyEnv" field'
          });
        }
        break;
      case 'oauth':
        if (!auth.clientIdEnv || !auth.clientSecretEnv) {
          this.warnings.push({
            path,
            message: 'OAuth may require "clientIdEnv" and "clientSecretEnv" fields'
          });
        }
        break;
    }
  }

  validateTools(path, tools) {
    const seenNames = new Set();

    for (let i = 0; i < tools.length; i++) {
      const tool = tools[i];
      const toolPath = `${path}[${i}]`;

      // Check for duplicate names
      if (seenNames.has(tool.name)) {
        this.errors.push({
          path: `${toolPath}.name`,
          message: `Duplicate tool name: "${tool.name}"`
        });
      }
      seenNames.add(tool.name);

      // Validate inputSchema if present
      if (tool.inputSchema) {
        this.validateJsonSchema(`${toolPath}.inputSchema`, tool.inputSchema);
      }

      // Check for suspicious descriptions (potential prompt injection)
      if (tool.description) {
        const suspicious = ['ignore previous', 'disregard', 'system prompt', 'instructions'];
        for (const pattern of suspicious) {
          if (tool.description.toLowerCase().includes(pattern)) {
            this.warnings.push({
              path: `${toolPath}.description`,
              message: `Description may contain prompt injection attempt: "${pattern}"`
            });
          }
        }
      }
    }
  }

  validateJsonSchema(path, schema) {
    try {
      // Basic JSON Schema validation
      if (schema.type === 'object' && schema.properties) {
        for (const [propName, propSchema] of Object.entries(schema.properties)) {
          if (!propSchema.description && this.strict) {
            this.warnings.push({
              path: `${path}.properties.${propName}`,
              message: `Property "${propName}" missing description`
            });
          }
        }
      }
    } catch (e) {
      this.warnings.push({
        path,
        message: `Could not validate JSON Schema: ${e.message}`
      });
    }
  }

  runCustomRules(config, configPath) {
    for (const rule of this.customRules.rules) {
      switch (rule.check || 'pattern') {
        case 'pattern':
          this.checkPatternRule(rule, config, configPath);
          break;
        case 'envVarExists':
          this.checkEnvVarRule(rule);
          break;
      }
    }
  }

  checkPatternRule(rule, config, configPath) {
    const regex = new RegExp(rule.pattern, 'i');
    const configStr = JSON.stringify(config);
    
    if (regex.test(configStr)) {
      const issue = {
        path: configPath,
        message: rule.message,
        ruleId: rule.id
      };
      
      if (rule.severity === 'error') {
        this.errors.push(issue);
      } else {
        this.warnings.push(issue);
      }
    }
  }

  checkEnvVarRule(rule) {
    if (!rule.params || rule.params.length === 0) return;
    
    for (const envVar of rule.params) {
      if (!process.env[envVar]) {
        const issue = {
          path: 'environment',
          message: `Required environment variable not set: ${envVar}`,
          ruleId: rule.id
        };
        
        if (rule.severity === 'error') {
          this.errors.push(issue);
        } else {
          this.warnings.push(issue);
        }
      }
    }
  }

  getResults() {
    return {
      errors: this.errors,
      warnings: this.warnings,
      valid: this.errors.length === 0
    };
  }
}

function validateMcpConfig(configPath, options = {}) {
  const validator = new McpValidator(options);
  return validator.validate(configPath);
}

module.exports = {
  McpValidator,
  validateMcpConfig,
  mcpSchema
};
