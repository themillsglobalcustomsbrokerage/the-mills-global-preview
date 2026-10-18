/**
 * Custom cursor: a small dot that tracks the pointer exactly, plus a larger
 * outlined ring that trails it with a short delay and catches up to it. Both invert what is beneath them. The ring grows over
 * links and buttons. Desktop (fine pointer) only.
 */
(function () {
    'use strict';
    if (!window.matchMedia || !window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var root = document.documentElement;
    var ring = document.createElement('div');
    var dot = document.createElement('div');
    ring.className = 'mills-cursor';
    dot.className = 'mills-cursor-dot';
    ring.setAttribute('aria-hidden', 'true');
    dot.setAttribute('aria-hidden', 'true');
    document.body.appendChild(ring);
    document.body.appendChild(dot);
    root.classList.add('has-custom-cursor');

    var mouse = { x: -100, y: -100 };
    var pos = { x: -100, y: -100 };
    var scale = 1, scaleTarget = 1;
    var seen = false;

    var FOLLOW = 0.32;      // the ring eases toward the dot: always behind it, never past it

    var INTERACTIVE = 'a, button, [data-open], [role="button"], summary, label, .content-card, .faq-question, .service-slide, .cta-pair *';
    var TEXTY = 'input, textarea, select';

    document.addEventListener('mousemove', function (e) {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
        if (!seen) {
            seen = true;
            pos.x = mouse.x;
            pos.y = mouse.y;
            root.classList.add('cursor-visible');
        }
        var t = e.target;
        var texty = t.closest && t.closest(TEXTY);
        root.classList.toggle('cursor-texty', !!texty);
        var hot = t.closest && t.closest(INTERACTIVE);
        scaleTarget = hot ? 1.9 : 1;
        ring.classList.toggle('is-hot', !!hot);
    }, { passive: true });

    document.addEventListener('mousedown', function () { ring.classList.add('is-down'); });
    document.addEventListener('mouseup', function () { ring.classList.remove('is-down'); });
    document.addEventListener('mouseleave', function () { root.classList.remove('cursor-visible'); seen = false; });
    document.addEventListener('mouseenter', function () { root.classList.add('cursor-visible'); });

    var running = false;
    function tick() {
        // plain easing: the ring simply lags a moment behind the dot, then catches up
        pos.x += (mouse.x - pos.x) * FOLLOW;
        pos.y += (mouse.y - pos.y) * FOLLOW;
        scale += (scaleTarget - scale) * 0.14;

        ring.style.transform = 'translate3d(' + pos.x + 'px,' + pos.y + 'px,0) translate(-50%,-50%) scale(' + scale + ')';
        dot.style.transform = 'translate3d(' + mouse.x + 'px,' + mouse.y + 'px,0) translate(-50%,-50%)';
        var settled = Math.abs(mouse.x - pos.x) < 0.05 && Math.abs(mouse.y - pos.y) < 0.05 && Math.abs(scaleTarget - scale) < 0.005;
        if (settled) { running = false; return; }   // idle: stop the loop until the pointer moves
        window.requestAnimationFrame(tick);
    }
    function wake() { if (!running) { running = true; window.requestAnimationFrame(tick); } }
    document.addEventListener('mousemove', wake, { passive: true });
    wake();
})();
