// static/js/script.js
// Main JavaScript for AI Personal Farming Assistant

// Global Variables
const APP = {
    initialized: false,
    currentPage: 'dashboard',
    language: 'en',
    theme: 'light'
};

// Initialize Application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    if (APP.initialized) return;
    
    // Initialize components
    initNavigation();
    initFormValidation();
    initImageUpload();
    initVoiceAssistant();
    initAnimations();
    initThemeToggle();
    
    APP.initialized = true;
    console.log('AI Personal Farming Assistant initialized successfully!');
}

// Navigation Handler
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const target = this.getAttribute('data-target');
            if (target) {
                e.preventDefault();
                navigateTo(target);
            }
        });
    });
}

function navigateTo(page) {
    APP.currentPage = page;
    // Update active state
    document.querySelectorAll('.page-content').forEach(el => {
        el.classList.remove('active');
    });
    const targetPage = document.getElementById(`page-${page}`);
    if (targetPage) {
        targetPage.classList.add('active');
    }
    // Update navigation
    document.querySelectorAll('.nav-link').forEach(el => {
        el.classList.remove('active');
        if (el.getAttribute('data-target') === page) {
            el.classList.add('active');
        }
    });
}

// Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('[data-validate]');
    
    inputs.forEach(input => {
        const value = input.value.trim();
        const validationType = input.getAttribute('data-validate');
        const errorElement = document.getElementById(`${input.id}-error`);
        
        if (!validateInput(value, validationType)) {
            isValid = false;
            input.classList.add('is-invalid');
            if (errorElement) {
                errorElement.style.display = 'block';
            }
        } else {
            input.classList.remove('is-invalid');
            if (errorElement) {
                errorElement.style.display = 'none';
            }
        }
    });
    
    return isValid;
}

function validateInput(value, type) {
    switch(type) {
        case 'required':
            return value.length > 0;
        case 'email':
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
        case 'number':
            return !isNaN(value) && value > 0;
        case 'phone':
            return /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/.test(value);
        default:
            return true;
    }
}

// Image Upload Handler
function initImageUpload() {
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach(area => {
        const fileInput = area.querySelector('input[type="file"]');
        if (!fileInput) return;
        
        // Click to upload
        area.addEventListener('click', function(e) {
            if (e.target !== fileInput) {
                fileInput.click();
            }
        });
        
        // File selection
        fileInput.addEventListener('change', function(e) {
            const file = this.files[0];
            if (file) {
                handleFileUpload(file, area);
            }
        });
        
        // Drag and drop
        area.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });
        
        area.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
        });
        
        area.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                handleFileUpload(files[0], area);
            }
        });
    });
}

function handleFileUpload(file, area) {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif'];
    if (!validTypes.includes(file.type)) {
        showNotification('Please upload a valid image file (JPG, PNG, GIF)', 'error');
        return;
    }
    
    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        showNotification('File size should be less than 5MB', 'error');
        return;
    }
    
    // Preview image
    const reader = new FileReader();
    reader.onload = function(e) {
        const previewContainer = area.querySelector('.preview-container') || 
                                document.createElement('div');
        previewContainer.className = 'preview-container mt-3';
        
        const img = document.createElement('img');
        img.src = e.target.result;
        img.className = 'img-fluid rounded';
        img.style.maxHeight = '200px';
        
        previewContainer.innerHTML = '';
        previewContainer.appendChild(img);
        area.appendChild(previewContainer);
        
        showNotification('Image uploaded successfully!', 'success');
    };
    reader.readAsDataURL(file);
}

// Voice Assistant
function initVoiceAssistant() {
    const micButton = document.getElementById('micButton');
    if (!micButton) return;
    
    let recognition = null;
    let isListening = false;
    
    micButton.addEventListener('click', function() {
        toggleVoiceRecognition();
    });
    
    function toggleVoiceRecognition() {
        if (!isListening) {
            startVoiceRecognition();
        } else {
            stopVoiceRecognition();
        }
    }
    
    function startVoiceRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            showNotification('Voice recognition is not supported in your browser', 'error');
            return;
        }
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        
        const languageSelect = document.getElementById('languageSelect');
        recognition.lang = languageSelect ? languageSelect.value : 'en-US';
        recognition.continuous = false;
        recognition.interimResults = true;
        
        recognition.onstart = function() {
            isListening = true;
            micButton.classList.add('listening');
            micButton.innerHTML = '<i class="fas fa-stop"></i>';
            updateStatus('Listening... Speak now!');
        };
        
        recognition.onresult = function(event) {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            updateStatus(`Processing: "${transcript}"`);
            
            const voiceInput = document.getElementById('voiceInput');
            if (voiceInput) {
                voiceInput.value = transcript;
            }
        };
        
        recognition.onerror = function(event) {
            showNotification(`Error: ${event.error}`, 'error');
            stopVoiceRecognition();
        };
        
        recognition.onend = function() {
            if (isListening) {
                stopVoiceRecognition();
                // Auto-submit if voice input was captured
                const voiceForm = document.getElementById('voiceForm');
                if (voiceForm) {
                    setTimeout(() => voiceForm.submit(), 500);
                }
            }
        };
        
        recognition.start();
    }
    
    function stopVoiceRecognition() {
        if (recognition) {
            recognition.stop();
        }
        isListening = false;
        micButton.classList.remove('listening');
        micButton.innerHTML = '<i class="fas fa-microphone"></i>';
        updateStatus('Click the microphone to start speaking');
    }
    
    function updateStatus(message) {
        const statusElement = document.getElementById('statusText');
        if (statusElement) {
            statusElement.textContent = message;
        }
    }
}

// Animations
function initAnimations() {
    // Add fade-in animation to elements
    const animatedElements = document.querySelectorAll('[data-animate]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const animation = entry.target.getAttribute('data-animate') || 'fadeIn';
                entry.target.classList.add(animation);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(el => observer.observe(el));
}

// Theme Toggle
function initThemeToggle() {
    const toggleBtn = document.getElementById('themeToggle');
    if (!toggleBtn) return;
    
    toggleBtn.addEventListener('click', function() {
        const currentTheme = document.body.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.body.setAttribute('data-theme', newTheme);
        APP.theme = newTheme;
        localStorage.setItem('theme', newTheme);
    });
    
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
}

// Notifications
function showNotification(message, type = 'info') {
    const notificationContainer = document.getElementById('notificationContainer') || 
                                  createNotificationContainer();
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} fade-in`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    notificationContainer.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

function createNotificationContainer() {
    const container = document.createElement('div');
    container.id = 'notificationContainer';
    container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 400px;
        width: 100%;
    `;
    document.body.appendChild(container);
    return container;
}

function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Utility Functions
function formatDate(date) {
    if (!date) return '';
    const d = new Date(date);
    return d.toLocaleDateString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    });
}

function formatCurrency(amount) {
    if (!amount) return '₹0';
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

function getCropIcon(crop) {
    const icons = {
        wheat: 'fa-wheat',
        rice: 'fa-seedling',
        maize: 'fa-seedling',
        cotton: 'fa-tree',
        tomato: 'fa-apple-alt',
        potato: 'fa-seedling',
        onion: 'fa-seedling'
    };
    return icons[crop.toLowerCase()] || 'fa-seedling';
}

// Progress Bar Animation
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar-animate');
    progressBars.forEach(bar => {
        const targetWidth = bar.getAttribute('data-width');
        if (targetWidth) {
            setTimeout(() => {
                bar.style.width = targetWidth + '%';
            }, 500);
        }
    });
}

// Statistics Counter Animation
function animateCounters() {
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const speed = 200;
        const increment = target / speed;
        let current = 0;
        
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.ceil(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };
        
        updateCounter();
    });
}

// Export functions for global use
window.showNotification = showNotification;
window.formatDate = formatDate;
window.formatCurrency = formatCurrency;
window.navigateTo = navigateTo;

console.log('AI Personal Farming Assistant JS loaded successfully!');