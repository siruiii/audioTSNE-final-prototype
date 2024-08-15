const logMessages = [];
    const originalConsoleLog = console.log;
  console.log = function(...args) {
    logMessages.push(args.join(' '));
    originalConsoleLog.apply(console, args);
  };
  
  function downloadLog() {
    const blob = new Blob([logMessages.join('\n')], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
  
    // Get the current date and time
    const now = new Date();
    const dateStr = now.toISOString().replace(/[:.]/g, '-');
    const filename = `console-log-${dateStr}.txt`;
  
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }