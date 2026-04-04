import { config } from 'dotenv';
import chalk from 'chalk';
import fs from 'fs-extra';
import path from 'path';
import { optimizeGitHub } from './src/platforms/github.js';
import { optimizeDevTo } from './src/platforms/devto.js';
import { optimizeHashnode } from './src/platforms/hashnode.js';
import { generateManualGuides } from './src/platforms/manual-platforms.js';
import { generateReport } from './src/report.js';

config();

const OUTPUT_DIR = './output';

async function ensureOutputDirs() {
  const dirs = [
    'github', 'devto', 'hashnode', 
    'producthunt', 'indiehackers', 
    'stackoverflow', 'linkedin', 'twitter'
  ];
  
  for (const dir of dirs) {
    await fs.ensureDir(path.join(OUTPUT_DIR, dir));
  }
}

async function main() {
  console.log(chalk.bold.blue('\n🔍 SEO Backlink Builder for ericgrill.com\n'));
  
  await ensureOutputDirs();
  
  const results = {
    timestamp: new Date().toISOString(),
    platforms: {},
    summary: {
      automated: 0,
      manual: 0,
      failed: 0
    }
  };

  // GitHub Profile Optimization
  console.log(chalk.yellow('📦 Optimizing GitHub Profile...'));
  try {
    const githubResult = await optimizeGitHub();
    results.platforms.github = githubResult;
    results.summary.automated++;
    console.log(chalk.green('   ✅ GitHub profile optimized\n'));
  } catch (error) {
    results.platforms.github = { status: 'failed', error: error.message };
    results.summary.failed++;
    console.log(chalk.red(`   ❌ GitHub failed: ${error.message}\n`));
  }

  // Dev.to Optimization
  console.log(chalk.yellow('📝 Optimizing Dev.to Profile...'));
  try {
    const devtoResult = await optimizeDevTo();
    results.platforms.devto = devtoResult;
    if (devtoResult.automated) {
      results.summary.automated++;
      console.log(chalk.green('   ✅ Dev.to profile optimized\n'));
    } else {
      results.summary.manual++;
      console.log(chalk.yellow('   ⚠️  Dev.to requires manual setup\n'));
    }
  } catch (error) {
    results.platforms.devto = { status: 'failed', error: error.message };
    results.summary.failed++;
    console.log(chalk.red(`   ❌ Dev.to failed: ${error.message}\n`));
  }

  // Hashnode Optimization
  console.log(chalk.yellow('🚀 Optimizing Hashnode Profile...'));
  try {
    const hashnodeResult = await optimizeHashnode();
    results.platforms.hashnode = hashnodeResult;
    if (hashnodeResult.automated) {
      results.summary.automated++;
      console.log(chalk.green('   ✅ Hashnode profile optimized\n'));
    } else {
      results.summary.manual++;
      console.log(chalk.yellow('   ⚠️  Hashnode requires manual setup\n'));
    }
  } catch (error) {
    results.platforms.hashnode = { status: 'failed', error: error.message };
    results.summary.failed++;
    console.log(chalk.red(`   ❌ Hashnode failed: ${error.message}\n`));
  }

  // Generate Manual Platform Guides
  console.log(chalk.yellow('📚 Generating Manual Platform Guides...'));
  try {
    await generateManualGuides();
    results.summary.manual += 5; // ProductHunt, IndieHackers, StackOverflow, LinkedIn, Twitter
    console.log(chalk.green('   ✅ Manual guides generated\n'));
  } catch (error) {
    console.log(chalk.red(`   ❌ Manual guides failed: ${error.message}\n`));
  }

  // Generate Final Report
  console.log(chalk.yellow('📊 Generating Final Report...'));
  try {
    await generateReport(results);
    console.log(chalk.green('   ✅ Report generated\n'));
  } catch (error) {
    console.log(chalk.red(`   ❌ Report failed: ${error.message}\n`));
  }

  // Summary
  console.log(chalk.bold.blue('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'));
  console.log(chalk.bold('📈 Summary'));
  console.log(chalk.bold.blue('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'));
  console.log(chalk.green(`   ✅ Automated: ${results.summary.automated} platforms`));
  console.log(chalk.yellow(`   ⚠️  Manual setup required: ${results.summary.manual} platforms`));
  console.log(chalk.red(`   ❌ Failed: ${results.summary.failed} platforms`));
  console.log(chalk.bold.blue('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'));
  
  console.log(chalk.cyan('📁 Check the output/ directory for detailed guides and reports.\n'));
}

main().catch(console.error);
