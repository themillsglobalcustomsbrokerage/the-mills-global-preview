/**
 * Site loading screen: silent Mills mograph on a navy gradient.
 *  - First page of a browser session: the full mograph, on screen at least 4 s.
 *  - Every page after that: the fast (3x) mograph, on screen at least 1 s.
 * It leaves once the page and its assets have loaded AND the minimum time has
 * passed. Add ?loader=1 to any URL to preview the full version again.
 * Loaded in <head>.
 */
(function () {
    'use strict';
    var force = /[?&]loader=1\b/.test(window.location.search);
    var seen = false;
    try {
        seen = !!window.sessionStorage.getItem('millsLoaderSeen');
        window.sessionStorage.setItem('millsLoaderSeen', '1');
    } catch (e) { /* storage blocked: treat as a first visit */ }
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var BASE = (document.currentScript && document.currentScript.src) ? document.currentScript.src.replace(/js\/loader\.js.*$/, '') : '';
    var fast = seen && !force;
    var MIN_MS = fast ? 1000 : 4000;
    var clip = fast ? 'loader-fast' : 'loader-mograph-v2';
    var shownAt = Date.now();

    var css = '' +
        '#millsLoader{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;' +
        'background:linear-gradient(90deg,#4A6BA3 0%,#2F3B5C 30%,#212431 58%,#212431 100%);transition:opacity .5s ease,visibility .5s ease}' +
        '#millsLoader.is-leaving{opacity:0;visibility:hidden}' +
        '#millsLoader .ml-lockup{width:clamp(220px,24vw,320px)}' +
        '#millsLoader video{display:block;width:100%;height:auto;mix-blend-mode:screen;pointer-events:none}' +
        '#millsLoader .ml-tag{display:inline-block;margin-left:17.6%;white-space:nowrap;line-height:1;text-transform:uppercase;font-family:'Plus Jakarta Sans',sans-serif;font-weight:500;color:#F5F5F5;opacity:.85}' +
        'html.mills-loading{overflow:hidden}';
    var style = document.createElement('style');
    style.textContent = css;
    document.documentElement.appendChild(style);

    var el = document.createElement('div');
    el.id = 'millsLoader';
    el.setAttribute('role', 'status');
    el.setAttribute('aria-label', 'Loading');
    el.innerHTML = '<div class="ml-lockup"><video muted playsinline autoplay preload="auto" aria-hidden="true">' +
        '<source src="' + BASE + 'assets/videos/' + clip + '.webm" type="video/webm">' +
        '<source src="' + BASE + 'assets/videos/' + clip + '.mp4" type="video/mp4"></video>' +
        '<span class="ml-tag" aria-hidden="true">TRADE WITHOUT LIMITS</span></div>';
    // The logo fills 17.6% to 97% of the video frame; fit the tagline to exactly that width, tucked under the logo
    var lock = el.querySelector('.ml-lockup'), tag = el.querySelector('.ml-tag');
    function fitTag() {
        var W = lock.getBoundingClientRect().width, target = W * 0.794;
        if (!W) return;
        tag.style.fontSize = (target * 0.07).toFixed(2) + 'px';
        tag.style.letterSpacing = '0px'; tag.style.marginRight = '0px';
        var ls = (target - tag.getBoundingClientRect().width) / 19;
        tag.style.letterSpacing = ls.toFixed(3) + 'px';
        tag.style.marginRight = (-ls).toFixed(3) + 'px';
        tag.style.marginTop = (-W * 0.066 + target * 0.04).toFixed(2) + 'px';
    }
    document.documentElement.appendChild(el);
    document.documentElement.classList.add('mills-loading');
    var video = el.querySelector('video');
    fitTag();
    window.addEventListener('resize', fitTag);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitTag);
    video.muted = true;
    var p = video.play();
    if (p && p.catch) p.catch(function () { /* autoplay blocked: gradient only */ });

    var done = false;
    function leave() {
        if (done) return;
        done = true;
        el.classList.add('is-leaving');
        document.documentElement.classList.remove('mills-loading');
        setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 650);
    }
    function leaveWhenReady() {
        var wait = MIN_MS - (Date.now() - shownAt);
        if (wait > 0) setTimeout(leave, wait);
        else leave();
    }
    if (document.readyState === 'complete') leaveWhenReady();
    else window.addEventListener('load', leaveWhenReady);
    setTimeout(leave, 12000); // safety net so a slow asset never traps the visitor
})();
