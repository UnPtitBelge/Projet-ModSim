"""
HTML head configuration for Dash application.

This module centralizes all HTML head setup, including CSS styling,
MathJax configuration, and meta information, keeping app.py clean.
"""

from __future__ import annotations

__all__ = ["get_index_string"]


def get_index_string() -> str:
    """
    Generate the complete HTML index string for the Dash application.

    Returns:
        str: Complete HTML document structure with embedded CSS and scripts.
    """
    return """<!DOCTYPE html>
<html>
  <head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>
      /* Chaos mode: inverted colors from project palette */
      #sidebar-container.chaos-mode {
        background-color: #3E2723 !important;  /* text color as bg */
        border-right-color: #2C1810 !important;  /* darker variant */
      }
      #sidebar-container.chaos-mode h3 {
        color: #FEF5F1 !important;  /* bg color as text */
      }
      #sidebar-container.chaos-mode a {
        color: #FEF5F1 !important;  /* bg color as text */
      }
      #sidebar-container.chaos-mode a:hover {
        background-color: rgba(254, 245, 241, 0.12) !important;  /* subtle hover overlay */
        color: #FEF5F1 !important;
      }
    </style>
    <script>
      window.MathJax = {
        tex: {
          inlineMath: [['$', '$']],
          displayMath: [['$$', '$$']],
          processEscapes: true,
          packages: {'[+]': ['ams']},
          tags: 'ams'
        },
        options: {
          skipHtmlTags: ['script', 'noscript', 'style', 'textarea'],
          ignoreHtmlClass: 'tex2jax_ignore',
          processHtmlClass: 'tex2jax_process'
        },
        chtml: {
          fontURL: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2',
          scale: 1.0
        }
      };
      
      // Fonction pour générer un son de tonnerre
      function playThunderSound() {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const duration = 0.5;
        const now = audioContext.currentTime;
        
        // Créer un bruit blanc (tonnerre)
        const bufferSize = audioContext.sampleRate * duration;
        const noiseBuffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate);
        const noiseData = noiseBuffer.getChannelData(0);
        
        for (let i = 0; i < bufferSize; i++) {
          noiseData[i] = Math.random() * 2 - 1;
        }
        
        const noiseSource = audioContext.createBufferSource();
        noiseSource.buffer = noiseBuffer;
        
        // Créer l'enveloppe d'amplitude (fade in/out)
        const gainNode = audioContext.createGain();
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.3, now + 0.05); // Attack
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + duration); // Decay
        
        // Filtrer le bruit pour plus de réalisme (basses fréquences)
        const filter = audioContext.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(5000, now);
        filter.frequency.exponentialRampToValueAtTime(1000, now + duration);
        
        noiseSource.connect(filter);
        filter.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        noiseSource.start(now);
        noiseSource.stop(now + duration);
      }
      
      // Ajouter l'événement au lien Chaos une fois que le DOM est prêt
      document.addEventListener('DOMContentLoaded', function() {
        const chaosLink = document.querySelector('a[href="/chaos"]');
        if (chaosLink) {
          chaosLink.addEventListener('click', playThunderSound);
        }
      });
    </script>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
    <style>
      mjx-container[jax="CHTML"][display="inline"] { display: inline !important; }
      mjx-container[jax="CHTML"][display="true"] {
        display: block !important;
        text-align: center;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        padding: 0.25rem 0;
      }
      a mjx-container, button mjx-container { font-size: 0.95em; }
    </style>
  </head>
  <body>
    {%app_entry%}
    <footer>
      {%config%}
      {%scripts%}
      {%renderer%}
    </footer>
    <script>
      (function() {
        function typeset() {
          if (window.MathJax && MathJax.typesetPromise) {
            MathJax.typesetPromise();
          }
        }
        if (document.readyState === 'complete') {
          typeset();
        } else {
          window.addEventListener('load', typeset);
        }
        var appRoot = document.getElementById('_dash-app') || document.body;
        var observer = new MutationObserver(function() {
          clearTimeout(observer._mjxTimer);
          observer._mjxTimer = setTimeout(typeset, 50);
        });
        observer.observe(appRoot, { childList: true, subtree: true });
      })();
    </script>
  </body>
</html>"""
