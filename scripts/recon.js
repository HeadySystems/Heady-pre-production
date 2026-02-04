// HEADY_BRAND:BEGIN
// HEADY SYSTEMS :: SACRED GEOMETRY
// FILE: scripts/recon.js
// LAYER: root
// 
//         _   _  _____    _    ____   __   __
//        | | | || ____|  / \  |  _ \ \ \ / /
//        | |_| ||  _|   / _ \ | |_| | \ V / 
//        |  _  || |___/ ___ \|  _  |   | |  
//        |_| |_||_____/_/   \_\____/   |_|  
// 
//    Sacred Geometry :: Organic Systems :: Breathing Interfaces
// HEADY_BRAND:END

/**
 * Heady Recon - Task Analysis and Preparation
 * 
 * Analyzes user input, identifies tasks, prepares system for build
 * Creates checkpoint predictions and workflow orchestration
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class HeadyRecon {
    constructor() {
        this.patterns = {
            // Task patterns that indicate work to be done
            'fix': /fix|repair|debug|resolve/i,
            'build': /build|compile|deploy|install/i,
            'test': /test|verify|validate|check/i,
            'create': /create|add|implement|develop|write/i,
            'update': /update|modify|enhance|improve/i,
            'remove': /remove|delete|clean|clear/i,
            'sync': /sync|push|commit|deploy/i,
            'analyze': /analyze|review|examine|investigate/i,
            'document': /doc|write|read|guide/i,
            'pattern': /pattern|validate|check|scan/i,
            'concept': /concept|idea|feature|requirement/i,
            'security': /security|auth|encrypt|protect/i,
            'performance': /performance|optimize|speed|cache/i
        };
        
        this.functionalIndicators = {
            // Signs that system is in a functional state
            buildComplete: ['dist', 'build', 'out'],
            depsInstalled: ['node_modules', 'package-lock.json'],
            testsPassing: ['test-results', 'coverage', 'test-report'],
            gitClean: ['no uncommitted changes', 'working tree clean'],
            patternsValid: ['pattern-registry.ts', 'checkpoint-validation.ps1'],
            docsComplete: ['README.md', 'USER_MANUAL.md'],
            brandingComplete: ['brand_headers.js', '.windsurfrules']
        };
        
        this.checkpointLevels = {
            quick: '2s - Before commits',
            standard: '10s - Before pushes',
            full: '30s - Before deployments',
            deep: '5min - Monthly reviews',
            production: '24h+ uptime'
        };
        
        this.predictedCheckpoints = [
            {
                name: 'Initial Setup Complete',
                triggers: ['deps installed', 'first build success'],
                validation: ['depsInstalled', 'buildComplete'],
                description: 'System ready for development'
            },
            {
                name: 'Core Features Implemented',
                triggers: ['tests pass', 'API responding'],
                validation: ['testsPassing', 'gitClean'],
                description: 'Core functionality complete'
            },
            {
                name: 'Visual Integration Complete',
                triggers: ['branding complete', 'docs have diagrams'],
                validation: ['brandingComplete', 'docsComplete'],
                description: 'Visual excellence achieved'
            },
            {
                name: 'Deployment Ready',
                triggers: ['all checks pass', 'superiority >= 85%'],
                validation: ['gitClean', 'patternsValid', 'docsComplete'],
                description: 'Ready for production'
            },
            {
                name: 'Production Stable',
                triggers: ['uptime >= 24h', 'no errors'],
                validation: ['no errors', 'performance met'],
                description: 'Production stable'
            }
        ];
    }

    /**
     * Analyze user input to identify tasks and prepare system
     */
    analyzeInput(input) {
        const analysis = {
            timestamp: new Date().toISOString(),
            input: input,
            detectedTasks: [],
            recommendedActions: [],
            predictedCheckpoint: null,
            systemState: this.checkSystemState(),
            priority: this.calculatePriority(input)
        };

        // Detect task patterns in input
        for (const [pattern, description] of Object.entries(this.patterns)) {
            if (pattern.test(input)) {
                analysis.detectedTasks.push({
                    type: this.getTaskType(pattern, description),
                    description: description,
                    priority: this.getTaskPriority(pattern),
                    confidence: this.getConfidence(pattern, input)
                });
            }
        }

        // Predict next checkpoint based on tasks
        analysis.predictedCheckpoint = this.predictCheckpoint(analysis.detectedTasks);

        // Recommend actions
        analysis.recommendedActions = this.recommendActions(analysis.detectedTasks);

        return analysis;
    }

    /**
     * Check current system state
     */
    checkSystemState() {
        const state = {};
        for (const [indicator, files] of Object.entries(this.functionalIndicators)) {
            state[indicator] = files.some(file => 
                fs.existsSync(path.join('C:\\Users\\erich\\Heady', file)) ||
                fs.existsSync(path.join('C:\\Users\\erich\\CascadeProjects\\HeadyMonorepo', file))
            );
        }
        return state;
    }

    /**
     * Calculate task priority based on pattern
     */
    getTaskPriority(pattern) {
        const priorities = {
            'fix': 'HIGH',
            'build': 'HIGH',
            'test': 'MEDIUM',
            'create': 'MEDIUM',
            'update': 'MEDIUM',
            'remove': 'LOW',
            'sync': 'HIGH',
            'analyze': 'LOW',
            'document': 'LOW',
            'pattern': 'MEDIUM',
            'concept': 'HIGH',
            'security': 'CRITICAL',
            'performance': 'HIGH'
        };
        
        for (const [pattern, priority] of Object.entries(priorities)) {
            if (pattern.test('')) return priority;
        }
        return 'MEDIUM';
    }

    /**
     * Get task type from pattern
     */
    getTaskType(pattern, description) {
        const types = {
            'fix': 'Bug Fix',
            'build': 'Build',
            'test': 'Test',
            'create': 'Create',
            'update': 'Update',
            'remove': 'Remove',
            'sync': 'Sync',
            'analyze': 'Analyze',
            'document': 'Document',
            'pattern': 'Pattern',
            'concept': 'Concept',
            'security': 'Security',
            'performance': 'Performance'
        };
        
        for (const [pattern, type] of Object.entries(types)) {
            if (pattern.test(description)) return type;
        }
        return 'Task';
    }

    /**
     * Get confidence level for pattern match
     */
    getConfidence(pattern, input) {
        const matches = input.match(pattern);
        if (!matches) return 0;
        
        // Higher confidence for exact matches
        if (matches[0] === input.toLowerCase()) return 100;
        
        // Lower confidence for partial matches
        return Math.max(50, 100 - (input.length / input.length * 50));
    }

    /**
     * Predict next checkpoint based on detected tasks
     */
    predictCheckpoint(tasks) {
        if (tasks.length === 0) return null;
        
        // Find highest priority task
        const highestPriority = tasks.reduce((max, task) => 
            task.priority === 'HIGH' ? task : max, tasks[0]
        );
        
        // Find matching checkpoint
        for (const checkpoint of this.predictedCheckpoints) {
            if (this.matchesCheckpoint(checkpoint, tasks)) {
                return checkpoint;
            }
        }
        
        // Default to next checkpoint
        const currentIndex = this.predictedCheckpoints.findIndex(cp => 
            cp.name === 'Initial Setup Complete'
        );
        return currentIndex >= 0 ? this.predictedCheckpoints[currentIndex] : null;
    }

    /**
     * Check if tasks match checkpoint criteria
     */
    matchesCheckpoint(checkpoint, tasks) {
        return checkpoint.triggers.some(trigger => 
            tasks.some(task => 
                task.description.toLowerCase().includes(trigger.toLowerCase())
            )
        );
    }

    /**
     * Recommend actions based on detected tasks
     */
    recommendActions(tasks) {
        const actions = [];
        
        if (tasks.some(t => t.priority === 'CRITICAL')) {
            actions.push('🚨 CRITICAL: Fix immediately');
        }
        
        if (tasks.some(t => t.priority === 'HIGH')) {
            actions.push('⚠️ HIGH: Address high priority tasks');
        }
        
        if (tasks.some(t => t.type === 'build')) {
            actions.push('🔨 Run HCAutoBuild');
        }
        
        if (tasks.some(t => t.type === 'sync')) {
            actions.push('🔄 Run HeadySync (hc -a hs)');
        }
        
        if (tasks.some(t => t.type === 'test')) {
            actions.push('🧪 Run tests');
        }
        
        return actions;
    }

    /**
     * Calculate priority score for input
     */
    calculatePriority(input) {
        let score = 50; // Base score
        
        // Higher priority for action-oriented words
        const actionWords = ['fix', 'build', 'deploy', 'test', 'sync', 'run', 'start', 'stop'];
        actionWords.forEach(word => {
            if (input.toLowerCase().includes(word)) score += 20;
        });
        
        // Higher priority for critical words
        const criticalWords = ['error', 'fail', 'broken', 'missing', 'urgent'];
        criticalWords.forEach(word => {
            if (input.toLowerCase().includes(word)) score += 30;
        });
        
        return Math.min(score, 100);
    }

    /**
     * Generate report
     */
    generateReport(analysis) {
        return {
            timestamp: analysis.timestamp,
            input: analysis.input,
            detectedTasks: analysis.detectedTasks,
            recommendedActions: analysis.recommendedActions,
            predictedCheckpoint: analysis.predictedCheckpoint,
            systemState: analysis.systemState,
            priority: analysis.priority,
            nextSteps: this.getNextSteps(analysis)
        };
    }

    /**
     * Get next steps based on analysis
     */
    getNextSteps(analysis) {
        const steps = [];
        
        if (analysis.predictedCheckpoint) {
            steps.push(`📍 Create checkpoint: ${analysis.predictedCheckpoint.name}`);
        }
        
        if (analysis.recommendedActions.length > 0) {
            steps.push(`📋 Recommended: ${analysis.recommendedActions.join(', ')}`);
        }
        
        if (analysis.detectedTasks.length > 0) {
            steps.push(`📝 Tasks to complete: ${analysis.detectedTasks.length} (${analysis.detectedTasks.map(t => t.type).join(', ')})`);
        }
        
        return steps;
    }

    /**
     * Save analysis to file
     */
    saveReport(analysis) {
        const report = this.generateReport(analysis);
        const reportPath = path.join('C:\\Users\\erich\\Heady\\logs\\recon-analysis.json');
        
        // Ensure directory exists
        const logDir = path.dirname(reportPath);
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }
        
        fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
        console.log(`📊 Recon analysis saved to: ${reportPath}`);
    }

    /**
     * Load previous analysis
     */
    loadReport() {
        const reportPath = path.join('C:\\Users\\erich\\Heady\\logs\\recon-analysis.json');
        if (fs.existsSync(reportPath)) {
            const data = fs.readFileSync(reportPath, 'utf8');
            return JSON.parse(data);
        }
        return null;
    }
}

module.exports = HeadyRecon;
