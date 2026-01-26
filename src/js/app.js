// Sample JavaScript file for static assets template

/**
 * Initialize the application
 */
function init() {
    console.log('Static Assets Template - App initialized');
    
    // Add event listeners
    setupEventListeners();
    
    // Load initial data
    loadData();
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    // Example: Handle button clicks
    const buttons = document.querySelectorAll('.button');
    buttons.forEach(button => {
        button.addEventListener('click', handleButtonClick);
    });
    
    // Example: Handle form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
}

/**
 * Handle button click events
 */
function handleButtonClick(event) {
    event.preventDefault();
    const button = event.target;
    console.log('Button clicked:', button.textContent);
    
    // Add your button click logic here
    showNotification('Button clicked successfully!');
}

/**
 * Handle form submission
 */
function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    
    console.log('Form submitted:', Object.fromEntries(formData));
    
    // Add your form submission logic here
    showNotification('Form submitted successfully!');
}

/**
 * Load data from API or local storage
 */
async function loadData() {
    try {
        // Example: Fetch data from an API
        // const response = await fetch('/data/sample.json');
        // const data = await response.json();
        
        console.log('Data loaded');
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

/**
 * Show a notification message
 */
function showNotification(message) {
    // Simple notification implementation
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #2ecc71;
        color: white;
        padding: 15px 20px;
        border-radius: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        z-index: 1000;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
