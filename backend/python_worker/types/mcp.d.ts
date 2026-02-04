// HEADY_BRAND:BEGIN
// HEADY SYSTEMS :: SACRED GEOMETRY
// FILE: backend/python_worker/types/mcp.d.ts
// LAYER: backend
// 
//         _   _  _____    _    ____   __   __
//        | | | || ____|  / \  |  _ \ \ \ / /
//        | |_| ||  _|   / _ \ | | | | \ V / 
//        |  _  || |___ / ___ \| |_| |  | |  
//        |_| |_||_____/_/   \_\____/   |_|  
// 
//    Sacred Geometry :: Organic Systems :: Breathing Interfaces
// HEADY_BRAND:END

// MCP interfaces for Heady Sonic Workspace

export interface McpServer {
  name: string;
  command: string;
  args: string[];
  env?: Record<string, string>;
}

export interface McpConfig {
  mcpServers: Record<string, McpServer>;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  priority: number; // Fibonacci number
  status: 'pending' | 'in-progress' | 'done';
  createdAt: string;
  updatedAt?: string;
}

export interface TrackNote {
  id: string;
  taskId: string;
  content: string;
  createdAt: string;
  updatedAt?: string;
}
