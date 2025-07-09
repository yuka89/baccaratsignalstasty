// AI Trading Assistant - Additional JavaScript functionality

// Utility functions
const utils = {
    // Format numbers with commas
    formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
    
    // Format currency
    formatCurrency(amount, currency = 'USD') {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    },
    
    // Format percentage
    formatPercent(value) {
        return new Intl.NumberFormat('en-US', {
            style: 'percent',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(value / 100);
    },
    
    // Get time ago string
    timeAgo(date) {
        const now = new Date();
        const diff = now - date;
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
        if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        return 'Just now';
    },
    
    // Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Notification system
const notifications = {
    show(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Trigger animation
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Auto remove
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => document.body.removeChild(notification), 300);
        }, duration);
    },
    
    success(message, duration = 3000) {
        this.show(message, 'success', duration);
    },
    
    error(message, duration = 5000) {
        this.show(message, 'error', duration);
    },
    
    info(message, duration = 3000) {
        this.show(message, 'info', duration);
    }
};

// Local storage helpers
const storage = {
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Error saving to localStorage:', e);
        }
    },
    
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.error('Error reading from localStorage:', e);
            return defaultValue;
        }
    },
    
    remove(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Error removing from localStorage:', e);
        }
    }
};

// Theme management
const theme = {
    init() {
        const savedTheme = storage.get('theme', 'light');
        this.setTheme(savedTheme);
    },
    
    setTheme(themeName) {
        document.documentElement.setAttribute('data-theme', themeName);
        storage.set('theme', themeName);
    },
    
    toggle() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }
};

// Chart utilities
const chartUtils = {
    // Create sparkline chart
    createSparkline(container, data, options = {}) {
        const config = {
            type: 'line',
            data: {
                labels: data.map((_, i) => i),
                datasets: [{
                    data: data,
                    borderColor: options.color || '#2563eb',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { display: false },
                    y: { display: false }
                },
                elements: {
                    point: { radius: 0 }
                }
            }
        };
        
        new Chart(container, config);
    },
    
    // Update chart data
    updateChart(chart, newData) {
        chart.data.datasets[0].data = newData;
        chart.update('none');
    }
};

// Market data helpers
const marketData = {
    // Check if market is open
    isMarketOpen() {
        const now = new Date();
        const day = now.getDay();
        const hours = now.getHours();
        
        // Weekend check
        if (day === 0 || day === 6) return false;
        
        // Market hours (9:30 AM - 4:00 PM EST)
        return hours >= 9 && hours < 16;
    },
    
    // Get market status
    getMarketStatus() {
        return this.isMarketOpen() ? 'open' : 'closed';
    },
    
    // Format market data for display
    formatMarketData(data) {
        return {
            symbol: data.symbol,
            price: utils.formatCurrency(data.price),
            change: data.change >= 0 ? `+${data.change.toFixed(2)}` : data.change.toFixed(2),
            changePercent: utils.formatPercent(data.changePercent),
            volume: utils.formatNumber(data.volume),
            isPositive: data.change >= 0
        };
    }
};

// Form validation
const validation = {
    // Validate stock symbol
    validateSymbol(symbol) {
        const regex = /^[A-Z]{1,5}$/;
        return regex.test(symbol.toUpperCase());
    },
    
    // Validate email
    validateEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    },
    
    // Add validation styling
    addValidationStyle(element, isValid) {
        element.classList.remove('success-border', 'error-border');
        element.classList.add(isValid ? 'success-border' : 'error-border');
    }
};

// Analytics tracking
const analytics = {
    track(event, properties = {}) {
        // In a real app, this would send data to analytics service
        console.log('Analytics event:', event, properties);
    },
    
    trackPageView(page) {
        this.track('page_view', { page });
    },
    
    trackUserAction(action, details = {}) {
        this.track('user_action', { action, ...details });
    }
};

// Error handling
const errorHandler = {
    handle(error, context = 'Unknown') {
        console.error(`Error in ${context}:`, error);
        
        // Show user-friendly error message
        let message = 'An error occurred. Please try again.';
        
        if (error.message) {
            if (error.message.includes('network') || error.message.includes('fetch')) {
                message = 'Network error. Please check your connection.';
            } else if (error.message.includes('API') || error.message.includes('key')) {
                message = 'API error. Please check your configuration.';
            }
        }
        
        notifications.error(message);
        
        // Track error
        analytics.track('error', {
            message: error.message,
            context: context,
            timestamp: new Date().toISOString()
        });
    }
};

// Initialize tooltips
const tooltips = {
    init() {
        // Create tooltip elements for any element with data-tooltip
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            element.addEventListener('mouseenter', this.show.bind(this));
            element.addEventListener('mouseleave', this.hide.bind(this));
        });
    },
    
    show(event) {
        const element = event.target;
        const text = element.getAttribute('data-tooltip');
        
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip-popup';
        tooltip.textContent = text;
        
        document.body.appendChild(tooltip);
        
        // Position tooltip
        const rect = element.getBoundingClientRect();
        tooltip.style.position = 'absolute';
        tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10}px`;
        tooltip.style.left = `${rect.left + rect.width / 2 - tooltip.offsetWidth / 2}px`;
        tooltip.style.zIndex = '1000';
        
        element._tooltip = tooltip;
    },
    
    hide(event) {
        const element = event.target;
        if (element._tooltip) {
            document.body.removeChild(element._tooltip);
            element._tooltip = null;
        }
    }
};

// Performance monitoring
const performance = {
    timers: {},
    
    start(name) {
        this.timers[name] = performance.now();
    },
    
    end(name) {
        if (this.timers[name]) {
            const duration = performance.now() - this.timers[name];
            console.log(`${name} took ${duration.toFixed(2)}ms`);
            delete this.timers[name];
            return duration;
        }
    }
};

// Export for use in other scripts
window.TradingApp = {
    utils,
    notifications,
    storage,
    theme,
    chartUtils,
    marketData,
    validation,
    analytics,
    errorHandler,
    tooltips,
    performance
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    theme.init();
    tooltips.init();
    analytics.trackPageView('home');
});

// Global error handler
window.addEventListener('error', (event) => {
    errorHandler.handle(event.error, 'Global');
});

// Global unhandled promise rejection handler
window.addEventListener('unhandledrejection', (event) => {
    errorHandler.handle(event.reason, 'Promise');
});

// Service worker registration (if available)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}