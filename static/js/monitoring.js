// ==================== CTF Integrity Monitoring System ====================

// Track page visibility changes (tab switching)
let tabSwitchCount = 0;
let lastTabSwitch = Date.now();

document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        tabSwitchCount++;
        lastTabSwitch = Date.now();
        
        // Log violation if excessive tab switching
        if (tabSwitchCount > 3) {
            logViolation('tab_switch_excessive', {
                count: tabSwitchCount,
                timestamp: new Date().toISOString()
            });
        }
    }
});

// Track copy-paste attempts
let copyAttempts = 0;
let pasteAttempts = 0;

document.addEventListener('copy', function(e) {
    copyAttempts++;
    
    if (copyAttempts > 5) {
        logViolation('copy_excessive', {
            count: copyAttempts,
            timestamp: new Date().toISOString()
        });
    }
});

document.addEventListener('paste', function(e) {
    pasteAttempts++;
    
    // Allow paste in flag submission fields
    const target = e.target;
    if (target.name === 'flag') {
        return;
    }
    
    if (pasteAttempts > 3) {
        logViolation('paste_suspicious', {
            count: pasteAttempts,
            timestamp: new Date().toISOString()
        });
    }
});

// Track right-click (context menu) attempts
let rightClickCount = 0;

document.addEventListener('contextmenu', function(e) {
    rightClickCount++;
    
    if (rightClickCount > 5) {
        logViolation('right_click_excessive', {
            count: rightClickCount,
            timestamp: new Date().toISOString()
        });
    }
});

// Track keyboard shortcuts (potential DevTools opening)
document.addEventListener('keydown', function(e) {
    // F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C, Ctrl+U
    const devToolsKeys = [
        e.keyCode === 123, // F12
        (e.ctrlKey && e.shiftKey && e.keyCode === 73), // Ctrl+Shift+I
        (e.ctrlKey && e.shiftKey && e.keyCode === 74), // Ctrl+Shift+J
        (e.ctrlKey && e.shiftKey && e.keyCode === 67), // Ctrl+Shift+C
        (e.ctrlKey && e.keyCode === 85) // Ctrl+U
    ];
    
    if (devToolsKeys.some(key => key)) {
        logViolation('devtools_attempt', {
            key: e.keyCode,
            timestamp: new Date().toISOString()
        });
    }
});

// Detect window blur (switching to another application)
let blurCount = 0;
let blurStartTime = null;

window.addEventListener('blur', function() {
    blurCount++;
    blurStartTime = Date.now();
});

window.addEventListener('focus', function() {
    if (blurStartTime) {
        const blurDuration = Date.now() - blurStartTime;
        
        // If away for more than 30 seconds, log it
        if (blurDuration > 30000) {
            logViolation('prolonged_absence', {
                duration: blurDuration,
                count: blurCount,
                timestamp: new Date().toISOString()
            });
        }
    }
});

// Track mouse movements to detect bot-like behavior
let mouseMovements = [];
let lastMouseTime = Date.now();

document.addEventListener('mousemove', function(e) {
    const now = Date.now();
    const timeDiff = now - lastMouseTime;
    
    mouseMovements.push({
        x: e.clientX,
        y: e.clientY,
        time: now,
        speed: timeDiff
    });
    
    // Keep only last 100 movements
    if (mouseMovements.length > 100) {
        mouseMovements.shift();
    }
    
    lastMouseTime = now;
    
    // Detect suspiciously uniform movements (bot)
    if (mouseMovements.length >= 50) {
        const speeds = mouseMovements.map(m => m.speed);
        const avgSpeed = speeds.reduce((a, b) => a + b) / speeds.length;
        const variance = speeds.reduce((sum, speed) => sum + Math.pow(speed - avgSpeed, 2), 0) / speeds.length;
        
        // Very low variance might indicate bot
        if (variance < 10) {
            logViolation('bot_like_behavior', {
                variance: variance,
                avgSpeed: avgSpeed,
                timestamp: new Date().toISOString()
            });
        }
    }
});

// Detect rapid clicking (potential automation)
let clickTimes = [];

document.addEventListener('click', function() {
    const now = Date.now();
    clickTimes.push(now);
    
    // Keep only last 10 clicks
    if (clickTimes.length > 10) {
        clickTimes.shift();
    }
    
    // Check if 10 clicks in less than 2 seconds
    if (clickTimes.length === 10) {
        const timeSpan = clickTimes[9] - clickTimes[0];
        if (timeSpan < 2000) {
            logViolation('rapid_clicking', {
                clicks: 10,
                timespan: timeSpan,
                timestamp: new Date().toISOString()
            });
        }
    }
});

// Browser fingerprinting
function getBrowserFingerprint() {
    return {
        userAgent: navigator.userAgent,
        language: navigator.language,
        platform: navigator.platform,
        screenResolution: `${screen.width}x${screen.height}`,
        colorDepth: screen.colorDepth,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        plugins: Array.from(navigator.plugins).map(p => p.name).join(','),
        canvas: getCanvasFingerprint(),
        webgl: getWebGLFingerprint()
    };
}

function getCanvasFingerprint() {
    try {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        ctx.textBaseline = 'top';
        ctx.font = '14px Arial';
        ctx.fillText('Browser Fingerprint', 2, 2);
        return canvas.toDataURL();
    } catch (e) {
        return 'unavailable';
    }
}

function getWebGLFingerprint() {
    try {
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
        return {
            vendor: gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL),
            renderer: gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL)
        };
    } catch (e) {
        return 'unavailable';
    }
}

// Store fingerprint on page load
const browserFingerprint = getBrowserFingerprint();
console.log('Browser fingerprint generated:', browserFingerprint);

// Function to log violations to server
function logViolation(type, data) {
    fetch('/log_violation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            type: type,
            data: data,
            fingerprint: browserFingerprint
        })
    }).catch(error => {
        console.error('Error logging violation:', error);
    });
}

// Periodic activity check
setInterval(function() {
    // Send heartbeat with current stats
    const stats = {
        tabSwitches: tabSwitchCount,
        copyAttempts: copyAttempts,
        pasteAttempts: pasteAttempts,
        rightClicks: rightClickCount,
        blurs: blurCount,
        timestamp: new Date().toISOString()
    };
    
    console.log('Activity stats:', stats);
}, 60000); // Every minute

// Detect if DevTools is open (size check)
let devtoolsOpen = false;
const threshold = 160;

setInterval(function() {
    if (window.outerWidth - window.innerWidth > threshold || 
        window.outerHeight - window.innerHeight > threshold) {
        if (!devtoolsOpen) {
            devtoolsOpen = true;
            logViolation('devtools_open', {
                timestamp: new Date().toISOString()
            });
        }
    } else {
        devtoolsOpen = false;
    }
}, 1000);

// Show monitoring indicator
window.addEventListener('load', function() {
    console.log('%c⚠️ CTF MONITORING ACTIVE', 'color: red; font-size: 20px; font-weight: bold;');
    console.log('%cYour activity is being monitored for competition integrity.', 'font-size: 14px;');
    console.log('%cAny suspicious behavior will be flagged.', 'font-size: 14px;');
});
