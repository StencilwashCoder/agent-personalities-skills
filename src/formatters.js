/**
 * Output formatters for MCP Validator
 * Supports: pretty, JSON, and SARIF formats
 */

const fs = require('fs');

function formatOutput(summary, format) {
  switch (format) {
    case 'json':
      return JSON.stringify(summary, null, 2);
    case 'sarif':
      return JSON.stringify(generateSarif(summary.results), null, 2);
    case 'pretty':
    default:
      return formatPretty(summary);
  }
}

function formatPretty(summary) {
  const lines = [];
  lines.push('MCP Validation Results');
  lines.push('=' .repeat(50));
  lines.push(`Files checked: ${summary.totalFiles}`);
  lines.push(`Errors: ${summary.totalErrors}`);
  lines.push(`Warnings: ${summary.totalWarnings}`);
  lines.push(`Valid: ${summary.valid ? '✅ Yes' : '❌ No'}`);
  lines.push('');

  for (const result of summary.results) {
    lines.push(`📄 ${result.file}`);
    if (result.errors.length === 0 && result.warnings.length === 0) {
      lines.push('  ✅ No issues');
    } else {
      for (const error of result.errors) {
        lines.push(`  ❌ ${error.path}: ${error.message}`);
      }
      for (const warning of result.warnings) {
        lines.push(`  ⚠️  ${warning.path}: ${warning.message}`);
      }
    }
    lines.push('');
  }

  return lines.join('\n');
}

function generateSarif(results) {
  const rules = new Map();
  const sarifResults = [];

  for (const fileResult of results) {
    for (const error of fileResult.errors) {
      const ruleId = error.ruleId || `mcp-error-${error.path}`;
      
      if (!rules.has(ruleId)) {
        rules.set(ruleId, {
          id: ruleId,
          name: error.path,
          shortDescription: {
            text: error.message
          },
          defaultConfiguration: {
            level: 'error'
          }
        });
      }

      sarifResults.push({
        ruleId,
        level: 'error',
        message: {
          text: error.message
        },
        locations: [{
          physicalLocation: {
            artifactLocation: {
              uri: fileResult.file
            }
          }
        }]
      });
    }

    for (const warning of fileResult.warnings) {
      const ruleId = warning.ruleId || `mcp-warning-${warning.path}`;
      
      if (!rules.has(ruleId)) {
        rules.set(ruleId, {
          id: ruleId,
          name: warning.path,
          shortDescription: {
            text: warning.message
          },
          defaultConfiguration: {
            level: 'warning'
          }
        });
      }

      sarifResults.push({
        ruleId,
        level: 'warning',
        message: {
          text: warning.message
        },
        locations: [{
          physicalLocation: {
            artifactLocation: {
              uri: fileResult.file
            }
          }
        }]
      });
    }
  }

  return {
    $schema: 'https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json',
    version: '2.1.0',
    runs: [{
      tool: {
        driver: {
          name: 'MCP Server Validator',
          informationUri: 'https://github.com/ericgrill/mcp-server-validator',
          version: '1.0.0',
          rules: Array.from(rules.values())
        }
      },
      results: sarifResults
    }]
  };
}

function writeSarif(results, outputPath) {
  const sarif = generateSarif(results);
  fs.writeFileSync(outputPath, JSON.stringify(sarif, null, 2));
}

module.exports = {
  formatOutput,
  formatPretty,
  generateSarif,
  writeSarif
};
