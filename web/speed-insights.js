// Vercel Speed Insights - Standalone initialization
// Based on @vercel/speed-insights v2.0.0

(function() {
  'use strict';
  
  // Initialize queue
  function initQueue() {
    if (window.si) return;
    window.si = function(...params) {
      window.siq = window.siq || [];
      window.siq.push(params);
    };
  }
  
  // Utility functions
  function isBrowser() {
    return typeof window !== "undefined";
  }
  
  function detectEnvironment() {
    try {
      const env = process.env.NODE_ENV;
      if (env === "development" || env === "test") {
        return "development";
      }
    } catch {
    }
    return "production";
  }
  
  function isDevelopment() {
    return detectEnvironment() === "development";
  }
  
  function makeAbsolute(url) {
    return url.startsWith("http://") || url.startsWith("https://") || url.startsWith("/") ? url : `/${url}`;
  }
  
  function getScriptSrc(props) {
    if (props.scriptSrc) {
      return makeAbsolute(props.scriptSrc);
    }
    if (isDevelopment()) {
      return "https://va.vercel-scripts.com/v1/speed-insights/script.debug.js";
    }
    if (props.dsn) {
      return "https://va.vercel-scripts.com/v1/speed-insights/script.js";
    }
    if (props.basePath) {
      return makeAbsolute(`${props.basePath}/speed-insights/script.js`);
    }
    return "/_vercel/speed-insights/script.js";
  }
  
  function loadProps(explicitProps) {
    const props = explicitProps || {};
    const dataset = {
      sdkn: "@vercel/speed-insights",
      sdkv: "2.0.0"
    };
    
    if (props.sampleRate) {
      dataset.sampleRate = props.sampleRate.toString();
    }
    if (props.route) {
      dataset.route = props.route;
    }
    if (isDevelopment() && props.debug === false) {
      dataset.debug = "false";
    }
    if (props.dsn) {
      dataset.dsn = props.dsn;
    }
    if (props.endpoint) {
      dataset.endpoint = makeAbsolute(props.endpoint);
    } else if (props.basePath) {
      dataset.endpoint = makeAbsolute(`${props.basePath}/speed-insights/vitals`);
    }
    
    return {
      src: getScriptSrc(props),
      beforeSend: props.beforeSend,
      dataset
    };
  }
  
  // Main injection function
  function injectSpeedInsights(props) {
    if (!isBrowser() || (props && props.route === null)) return null;
    
    initQueue();
    const { beforeSend, src, dataset } = loadProps(props || {});
    
    if (document.head.querySelector(`script[src*="${src}"]`)) return null;
    
    if (beforeSend) {
      window.si && window.si("beforeSend", beforeSend);
    }
    
    const script = document.createElement("script");
    script.src = src;
    script.defer = true;
    
    for (const [key, value] of Object.entries(dataset)) {
      script.dataset[key] = value;
    }
    
    script.onerror = function() {
      console.log(
        `[Vercel Speed Insights] Failed to load script from ${src}. Please check if any content blockers are enabled and try again.`
      );
    };
    
    document.head.appendChild(script);
    
    return {
      setRoute: function(route) {
        script.dataset.route = route || undefined;
      }
    };
  }
  
  // Auto-inject on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      injectSpeedInsights();
    });
  } else {
    injectSpeedInsights();
  }
})();
