import { getTenant, getApiBase } from './api';

export interface WebSocketEvent {
  type: string;
  data: any;
  timestamp: string;
}

export interface WebSocketMessage {
  event: string;
  data: any;
  tenant: string;
  timestamp?: string;
}

class WebSocketManager {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private listeners: Map<string, Set<(data: any) => void>> = new Map();
  private isConnecting = false;

  connect() {
    if (this.ws?.readyState === WebSocket.OPEN || this.isConnecting) {
      return;
    }

    this.isConnecting = true;
    const tenant = getTenant();
    const baseUrl = getApiBase().replace('http', 'ws');
    const url = `${baseUrl}/ws/events?tenant=${tenant}`;

    try {
      this.ws = new WebSocket(url);
      
      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.isConnecting = false;
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          this.handleMessage(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      this.ws.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason);
        this.isConnecting = false;
        this.handleReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.isConnecting = false;
      };
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      this.isConnecting = false;
      this.handleReconnect();
    }
  }

  private handleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max WebSocket reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
    
    console.log(`Reconnecting WebSocket in ${delay}ms (attempt ${this.reconnectAttempts})`);
    
    setTimeout(() => {
      this.connect();
    }, delay);
  }

  private handleMessage(message: WebSocketMessage) {
    const { event, data } = message;
    
    if (this.listeners.has(event)) {
      this.listeners.get(event)?.forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error('Error in WebSocket event handler:', error);
        }
      });
    }
  }

  subscribe(event: string, callback: (data: any) => void) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);

    // Auto-connect if not already connected
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      this.connect();
    }

    // Return unsubscribe function
    return () => {
      this.listeners.get(event)?.delete(callback);
      if (this.listeners.get(event)?.size === 0) {
        this.listeners.delete(event);
      }
    };
  }

  unsubscribe(event: string, callback: (data: any) => void) {
    this.listeners.get(event)?.delete(callback);
    if (this.listeners.get(event)?.size === 0) {
      this.listeners.delete(event);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.listeners.clear();
    this.reconnectAttempts = 0;
    this.isConnecting = false;
  }

  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

// Global WebSocket instance
export const wsManager = new WebSocketManager();

// Hook for using WebSocket in components
export function useWebSocket(event: string, callback: (data: any) => void) {
  const { useEffect } = require('react');
  
  useEffect(() => {
    const unsubscribe = wsManager.subscribe(event, callback);
    return unsubscribe;
  }, [event, callback]);
}

// Mock WebSocket for development when backend doesn't support it
export function createMockWebSocket() {
  if (typeof window === 'undefined') return;

  // Simulate periodic events
  const mockEvents = [
    { type: 'operation_completed', data: { id: 'op_001', status: 'completed' } },
    { type: 'backup_created', data: { id: 'backup_001', size: '2.4GB' } },
    { type: 'file_uploaded', data: { name: 'document.pdf', size: '1.2MB' } },
    { type: 'health_check', data: { status: 'healthy', timestamp: new Date().toISOString() } },
  ];

  let eventIndex = 0;
  
  const interval = setInterval(() => {
    const event = mockEvents[eventIndex % mockEvents.length];
    const message: WebSocketMessage = {
      event: event.type,
      data: event.data,
      tenant: getTenant(),
      timestamp: new Date().toISOString(),
    };

    // Dispatch custom event that our WebSocket manager can listen to
    window.dispatchEvent(new CustomEvent('mockWebSocketMessage', { 
      detail: message 
    }));

    eventIndex++;
  }, 5000); // Send mock event every 5 seconds

  // Clean up interval on page unload
  window.addEventListener('beforeunload', () => {
    clearInterval(interval);
  });

  return () => clearInterval(interval);
}
