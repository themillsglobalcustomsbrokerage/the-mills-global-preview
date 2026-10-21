/**
 * Scroll-scrubbed hero video engine for The Mills Global.
 * Desktop: the video's own playback position is driven directly by scroll
 * (currentTime = progress * duration), updated every frame - scrolling
 * down moves forward through the clip, scrolling up moves back.
 * Mobile: scrubs too, using a smaller all-keyframe copy of the clip (every
 * frame is seekable) with eased, throttled seeking so touch scrolling stays smooth.
 * Self-initializes on DOMContentLoaded.
 */
document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.hero-scroll-container');
    const viewport = document.querySelector('.hero-viewport');
    const video = document.querySelector('.hero-video');
    const placeholders = document.querySelector('.hero-placeholders');
    const placeholderSlides = document.querySelectorAll('.hero-placeholder__slide');
    const slides = document.querySelectorAll('.hero-slide');
    const progressEl = document.querySelector('.hero-progress');
    const indicator = document.querySelector('.scroll-indicator');
    const nav = document.querySelector('.nav');
    const frameEl = document.querySelector('.hero-frame');
    const hudEl = document.querySelector('.hero-hud');
    const hudRouteEl = document.querySelector('.hero-hud__route');

    if (!container || !viewport) return;

    let lastHudIndex = -1;

    // Continuous scroll-scrubbed motion for a slide's local progress `t`
    // (0..1 within its own zone, can fall outside that range when another
    // slide is active). Fades AND translates - no discrete on/off snap.
    const slideMotion = (t) => {
        if (t <= 0) return { opacity: 0, y: 40 };
        if (t >= 1) return { opacity: 0, y: -50 };
        if (t < 0.12) {
            const p = t / 0.12;
            return { opacity: p, y: 40 * (1 - p) };
        }
        if (t < 0.86) {
            const p = (t - 0.12) / 0.74;
            return { opacity: 1, y: -10 * p };
        }
        const p = (t - 0.86) / 0.14;
        return { opacity: 1 - p, y: -10 - (40 * p) };
    };

    let isMobile = false;
    let isActive = false;
    let scrollY = window.scrollY;
    let lastProgress = -1;
    let smoothTime = 0;
    let rafId = null;
    let containerTop = 0;
    let containerHeight = 0;
    let windowHeight = 0;
    let hasVideo = false;
    let videoPrimed = false;
    // Set once, the first time the video has a frame to show, and never
    // re-checked after - readyState briefly dips below 2 mid-seek while
    // scrubbing, and re-testing it every frame flickered the placeholder
    // on and off during scroll (looked like the video glitching).
    let videoReady = false;

    // Choose the clip by screen size (the mobile copy is a ~4 MB portrait-cropped, all-keyframe clip) and start loading it
    const phone = window.innerWidth < 768;
    if (video && video.dataset.src) {
        video.src = (phone && video.dataset.mobileSrc) ? video.dataset.mobileSrc : video.dataset.src;
        video.preload = 'auto';
        video.load();
    }

    // Check if video is valid
    if (video) {
        if (video.getAttribute('src') || video.querySelector('source')) {
            hasVideo = true;
            video.addEventListener('loadedmetadata', () => {
                video.classList.add('loaded');
            });
            video.addEventListener('loadeddata', () => {
                videoReady = true;
                if (placeholders) placeholders.style.display = 'none';
            });
            // Fallback if already loaded
            if (video.readyState >= 1) {
                video.classList.add('loaded');
            }
            if (video.readyState >= 2) {
                videoReady = true;
                if (placeholders) placeholders.style.display = 'none';
            }
        }
    }

    const checkMobile = () => {
        isMobile = window.innerWidth < 768;
    };

    const calculateDimensions = () => {
        containerTop = container.offsetTop;
        containerHeight = container.offsetHeight;
        windowHeight = viewport.offsetHeight || window.innerHeight;
    };

    // Desktop: currentTime is driven by scroll (see render() step 4), so
    // the video needs to stay paused - but a <video> that has never
    // actually played won't paint a new frame when you seek it (Safari
    // in particular just holds on a blank/first frame). So we "prime" it
    // with one real play → pause cycle, then hand control to scroll.
    const primeVideoForScrub = () => {
        if (!hasVideo || !video) return;
        video.loop = false;
        if (videoPrimed) {
            video.pause();
            return;
        }
        videoPrimed = true;
        const playPromise = video.play();
        if (playPromise && typeof playPromise.then === 'function') {
            playPromise.then(() => video.pause()).catch(() => video.pause());
        } else {
            video.pause();
        }
    };

    const onScroll = () => {
        scrollY = window.scrollY;
    };

    const render = () => {
        if (!isActive) return;

        let progress = (scrollY - containerTop) / (containerHeight - windowHeight);
        progress = Math.max(0, Math.min(1, progress));

        if (Math.abs(progress - lastProgress) > 0.0001) {
            lastProgress = progress;

            // 1. Progress bar
            if (progressEl) {
                progressEl.style.width = `${progress * 100}%`;
            }

            // 2. Nav state
            if (nav) {
                if (scrollY > 50 || progress > 0.01) {
                    nav.classList.add('scrolled');
                } else {
                    nav.classList.remove('scrolled');
                }
            }

            // 3. Indicator
            if (indicator) {
                if (progress > 0.04) {
                    indicator.classList.add('hidden');
                } else {
                    indicator.classList.remove('hidden');
                }
            }

            // 4. Video scrub / placeholder - video stays paused (primed
            // once, see primeVideoForScrub) and we seek currentTime
            // directly every frame so playback position tracks scroll
            // 1:1. Placeholder visibility is decided once via videoReady
            // (see above), never re-checked here, so it can't flicker.
            if (hasVideo && video && videoReady) {
                if (!isMobile && !isNaN(video.duration) && isFinite(video.duration)) {
                    video.currentTime = progress * video.duration;
                }
            } else if (!videoReady && placeholderSlides.length > 0) {
                if (placeholders) placeholders.style.display = 'block';
                // Zones: 0-0.25, 0.25-0.5, 0.5-0.75, 0.75-1.0
                const zoneIndex = Math.min(3, Math.floor(progress / 0.25));
                const zoneProgress = (progress - (zoneIndex * 0.25)) / 0.25;
                const scale = 1.08 - (zoneProgress * 0.08);

                placeholderSlides.forEach((slide, idx) => {
                    if (idx === zoneIndex) {
                        slide.classList.add('active');
                        slide.style.transform = `scale(${scale})`;
                    } else {
                        slide.classList.remove('active');
                    }
                });
            }

            // 5. Slides - continuous scroll-scrubbed fade + translate, one
            // quarter of total progress per slide, tracking the scrollbar
            // (and therefore the video) 1:1 rather than snapping in/out.
            slides.forEach((slide, i) => {
                let t = (progress - (i * 0.25)) / 0.25;
                // The very first slide starts already "settled in" at page
                // load (progress 0) instead of fading in from nothing.
                if (i === 0) t = Math.max(t, 0.12);
                const { opacity, y } = slideMotion(t);
                slide.style.opacity = opacity.toFixed(3);
                slide.style.pointerEvents = opacity > 0.5 ? 'auto' : 'none';
                const base = (!isMobile && slide.dataset.baseTransform) ? slide.dataset.baseTransform + ' ' : '';
                slide.style.transform = `${base}translateY(${y.toFixed(1)}px)`;
            });

            // 6. HUD route readout - swaps with the active slide, drifts
            // slowly upward as an independent parallax layer.
            if (hudEl) {
                const activeIndex = Math.max(0, Math.min(slides.length - 1, Math.floor(progress / 0.25)));
                if (activeIndex !== lastHudIndex) {
                    lastHudIndex = activeIndex;
                    const route = slides[activeIndex] ? slides[activeIndex].dataset.route : '';
                    if (hudRouteEl && route) hudRouteEl.innerHTML = route;
                }
                hudEl.style.transform = `translateY(${(-progress * 40).toFixed(1)}px)`;
            }

            // 7. Corner viewfinder frame - fades in once scrolling begins,
            // scales open very slightly as an extra layer of scroll motion.
            if (frameEl) {
                frameEl.classList.toggle('visible', progress > 0.015 && progress < 0.98);
                frameEl.style.transform = `scale(${(1 + progress * 0.015).toFixed(4)})`;
            }
        }

        // Mobile: ease toward the scroll position and never queue a seek while one is still running
        if (isMobile && hasVideo && video && videoReady && isFinite(video.duration) && video.duration > 0) {
            const target = lastProgress * video.duration;
            smoothTime += (target - smoothTime) * 0.22;
            if (!video.seeking && Math.abs(video.currentTime - smoothTime) > 0.02) {
                video.currentTime = smoothTime;
            }
        }

        rafId = requestAnimationFrame(render);
    };

    const init = () => {
        checkMobile();
        calculateDimensions();

        primeVideoForScrub();
        if (!isActive) {
            isActive = true;
            window.addEventListener('scroll', onScroll, { passive: true });
            lastProgress = -1; // force render
            rafId = requestAnimationFrame(render);
        }
    };

    const destroy = () => {
        window.removeEventListener('scroll', onScroll);
        if (rafId) cancelAnimationFrame(rafId);
        isActive = false;
    };

    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            checkMobile();
            calculateDimensions();
            lastProgress = -1;
        }, 200);
    });

    init();

    window.MillsScrollVideo = {
        destroy,
        refresh: () => {
            calculateDimensions();
            lastProgress = -1; // force render
        }
    };
});
