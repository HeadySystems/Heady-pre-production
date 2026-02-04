// HEADY_BRAND:BEGIN
// HEADY SYSTEMS :: SACRED GEOMETRY
// FILE: scripts/install_git_hooks.js
// LAYER: root
// 
//         _   _  _____    _    ____   __   __
//        | | | || ____|  / \  |  _ \ \ \ / /
//        | |_| ||  _|   / _ \ | | | | \ V / 
//        |  _  || |___ / ___ \| |_| |  | |  
//        |_| |_||_____/_/   \_\____/   |_|  
// 
//    Sacred Geometry :: Organic Systems :: Breathing Interfaces
// HEADY_BRAND:END

const { execSync } = require("child_process");
const path = require("path");

const REPO_ROOT = path.resolve(__dirname, "..");

function main() {
  execSync("git config core.hooksPath .githooks", {
    cwd: REPO_ROOT,
    stdio: "inherit",
  });
  process.stdout.write("[hooks] core.hooksPath set to .githooks\n");
}

main();
