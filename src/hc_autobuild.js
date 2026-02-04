// HEADY_BRAND:BEGIN
// HEADY SYSTEMS :: SACRED GEOMETRY
// FILE: src/hc_autobuild.js
// LAYER: backend/src
// 
//         _   _  _____    _    ____   __   __
//        | | | || ____|  / \  |  _ \ \ \ / /
//        | |_| ||  _|   / _ \ | | | | \ V / 
//        |  _  || |___ / ___ \| |_| |  | |  
//        |_| |_||_____/_/   \_\____/   |_|  
// 
//    Sacred Geometry :: Organic Systems :: Breathing Interfaces
// HEADY_BRAND:END

const { execSync } = require('child_process');
const path = require('path');

console.log('\n🔨 Heady AutoBuild - Sacred Geometry Build System\n');

const repos = [
  'C:\\Users\\erich\\Heady',
  'C:\\Users\\erich\\CascadeProjects\\HeadyMonorepo',
  'C:\\Users\\erich\\CascadeProjects\\HeadyEcosystem',
];

repos.forEach(repo => {
  const packageJson = path.join(repo, 'package.json');
  const fs = require('fs');
  
  if (fs.existsSync(packageJson)) {
    console.log(`📦 Building: ${repo}`);
    try {
      execSync('pnpm install', { cwd: repo, stdio: 'inherit' });
      console.log(`✅ ${repo} - Dependencies installed\n`);
    } catch (error) {
      console.log(`⚠️  ${repo} - No pnpm or build script\n`);
    }
  }
});

console.log('✅ Heady AutoBuild Complete!\n');
