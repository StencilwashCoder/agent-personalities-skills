/**
 * MCP Server Validator - GitHub Action
 * Validates MCP server configurations against the specification
 * 
 * Author: Eric Grill (https://ericgrill.com)
 */

const core = require('@actions/core');
const glob = require('glob');
const fs = require('fs');
const path = require('path');
const { validateMcpConfig } = require('./validator');
const { formatOutput, writeSarif } = require('./formatters');

async function run() {
  try {
    // Get inputs
    const configPath = core.getInput('config-path') || 'mcp.json';
    const strict = core.getBooleanInput('strict');
    const outputFormat = core.getInput('output-format') || 'pretty';
    const outputFile = core.getInput('output-file');
    const skipAuthCheck = core.getBooleanInput('skip-auth-check');
    const customRulesPath = core.getInput('custom-rules');

    core.info(`🔍 MCP Server Validator - by Eric Grill`);
    core.info(`   Config path: ${configPath}`);
    core.info(`   Strict mode: ${strict}`);
    core.info('');

    // Load custom rules if provided
    let customRules = null;
    if (customRulesPath && fs.existsSync(customRulesPath)) {
      try {
        customRules = JSON.parse(fs.readFileSync(customRulesPath, 'utf8'));
        core.info(`📋 Loaded custom rules from ${customRulesPath}`);
      } catch (e) {
        core.warning(`Failed to load custom rules: ${e.message}`);
      }
    }

    // Find all matching config files
    const files = await glob.glob(configPath, { 
      cwd: process.env.GITHUB_WORKSPACE || process.cwd() 
    });

    if (files.length === 0) {
      core.warning(`No MCP config files found matching: ${configPath}`);
      core.setOutput('valid', 'true');
      core.setOutput('errors', '0');
      core.setOutput('warnings', '0');
      core.setOutput('report', '{}');
      return;
    }

    core.info(`Found ${files.length} config file(s) to validate`);
    core.info('');

    // Validate each file
    let totalErrors = 0;
    let totalWarnings = 0;
    const allResults = [];

    for (const file of files) {
      const fullPath = path.resolve(process.env.GITHUB_WORKSPACE || process.cwd(), file);
      
      if (!fs.existsSync(fullPath)) {
        core.error(`Config file not found: ${file}`);
        totalErrors++;
        continue;
      }

      core.info(`📄 Validating: ${file}`);
      
      const result = validateMcpConfig(fullPath, {
        strict,
        skipAuthCheck,
        customRules
      });

      totalErrors += result.errors.length;
      totalWarnings += result.warnings.length;
      allResults.push({ file, ...result });

      // Print results
      if (outputFormat === 'pretty') {
        printPrettyResults(file, result);
      }
    }

    // Generate output
    const summary = {
      valid: totalErrors === 0,
      totalFiles: files.length,
      totalErrors,
      totalWarnings,
      results: allResults
    };

    // Set outputs
    core.setOutput('valid', String(totalErrors === 0));
    core.setOutput('errors', String(totalErrors));
    core.setOutput('warnings', String(totalWarnings));
    core.setOutput('report', JSON.stringify(summary));

    // Write output file if specified
    if (outputFile) {
      const formatted = formatOutput(summary, outputFormat);
      fs.writeFileSync(outputFile, formatted);
      core.info(`\n📝 Results written to: ${outputFile}`);
    }

    // Write SARIF for GitHub Security tab
    if (outputFormat === 'sarif') {
      const sarifPath = outputFile || 'mcp-validation.sarif';
      writeSarif(allResults, sarifPath);
      core.info(`📝 SARIF written to: ${sarifPath}`);
    }

    // Summary
    core.info('');
    core.info('═'.repeat(50));
    if (totalErrors === 0) {
      core.info('✅ All MCP configurations are valid!');
      if (totalWarnings > 0) {
        core.info(`⚠️  ${totalWarnings} warning(s) found`);
      }
    } else {
      core.info(`❌ Validation failed: ${totalErrors} error(s), ${totalWarnings} warning(s)`);
    }
    core.info('═'.repeat(50));

    // Fail if errors found
    if (totalErrors > 0) {
      core.setFailed(`MCP validation failed with ${totalErrors} error(s)`);
    }

  } catch (error) {
    core.setFailed(`Action failed: ${error.message}`);
  }
}

function printPrettyResults(file, result) {
  if (result.errors.length === 0 && result.warnings.length === 0) {
    core.info(`  ✅ Valid`);
    return;
  }

  for (const error of result.errors) {
    core.error(`  ❌ ${error.path}: ${error.message}`);
  }
  for (const warning of result.warnings) {
    core.warning(`  ⚠️  ${warning.path}: ${warning.message}`);
  }
}

run();
