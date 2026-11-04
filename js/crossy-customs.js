/**
 * Crossy Customs: guide the truck across the port without getting seized.
 * Arrow keys / swipe to move. Obstacles speed up every 5 crossings.
 */
(function () {
    'use strict';

    var canvas = document.getElementById('gameCanvas');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    var box = document.getElementById('gameContainer');

    var GAME_WIDTH, GAME_HEIGHT, GRID_SIZE, ROWS;
    function resizeCanvas() {
        var avail = Math.min((box.parentElement.clientWidth || window.innerWidth) - 8, 600);
        var w = Math.max(280, avail);
        var h = Math.min(Math.round(w * 1.3), Math.round(window.innerHeight * 0.82), 780);
        canvas.width = w;
        canvas.height = h;
        GAME_WIDTH = w;
        GAME_HEIGHT = h;
        GRID_SIZE = Math.floor(GAME_WIDTH / 12);
        ROWS = Math.floor(GAME_HEIGHT / GRID_SIZE);
    }
    resizeCanvas();

    var SPRITE_URLS = {
        truck: 'assets/images/game/truck.png',
        forklift: 'assets/images/game/forklift.png',
        officer: 'assets/images/game/officer.png',
        barrel: 'assets/images/game/barrel.png'
    };
    var FALLBACK = { truck: '#EA5C1F', forklift: '#4F5D75', officer: '#1F3244', barrel: '#EA5C1F' };
    var sprites = {};
    var loaded = 0;
    var TOTAL = Object.keys(SPRITE_URLS).length;

    function loadSprites(done) {
        Object.keys(SPRITE_URLS).forEach(function (key) {
            var img = new Image();
            img.onload = img.onerror = function () { loaded++; if (loaded >= TOTAL) done(); };
            img.src = SPRITE_URLS[key];
            sprites[key] = img;
        });
    }

    function drawSprite(key, x, y, w, h, opts) {
        opts = opts || {};
        var img = sprites[key];
        ctx.save();
        ctx.translate(x + w / 2, y + h / 2);
        if (opts.rotation) ctx.rotate(opts.rotation);
        if (opts.flipH) ctx.scale(-1, 1);
        if (img && img.complete && img.naturalWidth > 0) {
            ctx.drawImage(img, -w / 2, -h / 2, w, h);
        } else {
            ctx.fillStyle = FALLBACK[key];
            ctx.fillRect(-w / 2, -h / 2, w, h);
        }
        ctx.restore();
    }

    var state = 'loading';
    var score = 0;
    var level = 1;
    var scoreEl = document.getElementById('gameScore');
    var levelEl = document.getElementById('gameLevel');
    var finalEl = document.getElementById('gameFinal');
    var overEl = document.getElementById('gameOver');
    var clearedEl = document.getElementById('gameCleared');

    var PALETTE = {
        grid: 'rgba(79, 93, 117, 0.16)',
        topBand: 'rgba(31, 50, 68, 0.82)',
        startBand: 'rgba(234, 92, 31, 0.10)',
        label: '#F5F5F5'
    };

    var player = { x: 0, y: 0, width: 0, height: 0, moving: false, targetX: 0, targetY: 0, moveSpeed: 8 };

    function resetPlayer() {
        player.width = GRID_SIZE * 0.85;
        player.height = GRID_SIZE * 0.85;
        player.x = Math.floor(GAME_WIDTH / GRID_SIZE / 2) * GRID_SIZE;
        player.y = (ROWS - 1) * GRID_SIZE;
        player.targetX = player.x;
        player.targetY = player.y;
        player.moving = false;
    }

    function diffVal(base, perLevel, max) { return Math.min(base + (level - 1) * perLevel, max); }

    var forklifts = [], officers = [], barrels = [];

    function generateObstacles() {
        forklifts = []; officers = []; barrels = [];
        var forkliftStep = Math.max(3, 7 - Math.floor(level / 2));
        var row, i;
        for (row = 2; row < ROWS - 2; row += forkliftStep) {
            var dir = Math.random() > 0.5 ? 1 : -1;
            var speed = diffVal(0.6, 0.26, 3.2) + Math.random() * 0.5;
            var minGap = Math.max(3.5, 7 - level * 0.3);
            var spacing = GRID_SIZE * (minGap + Math.random() * 2);
            var count = Math.min(2 + Math.floor(level / 4), 4);
            for (i = 0; i < count; i++) {
                forklifts.push({
                    x: dir > 0 ? -GRID_SIZE - i * spacing : GAME_WIDTH + i * spacing,
                    y: row * GRID_SIZE, width: GRID_SIZE * 0.9, height: GRID_SIZE * 0.85, speed: speed * dir
                });
            }
        }
        if (level >= 2) {
            var officerStep = Math.max(3, 8 - Math.floor(level / 2));
            for (row = 1; row < ROWS - 1; row += officerStep) {
                officers.push({
                    x: Math.random() * (GAME_WIDTH - GRID_SIZE), y: row * GRID_SIZE,
                    width: GRID_SIZE * 0.75, height: GRID_SIZE * 0.85,
                    speed: diffVal(0.35, 0.11, 2.0) + Math.random() * 0.35,
                    direction: Math.random() > 0.5 ? 1 : -1
                });
            }
        }
        if (level >= 3) {
            var barrelStep = Math.max(4, 8 - Math.floor(level / 3));
            for (row = 3; row < ROWS - 1; row += barrelStep) {
                var d = Math.random() > 0.5 ? 1 : -1;
                var sp = diffVal(1.0, 0.20, 3.6) + Math.random() * 0.7;
                var cnt = Math.min(1 + Math.floor(level / 5), 3);
                var gap = GRID_SIZE * (4 + Math.random() * 3);
                for (i = 0; i < cnt; i++) {
                    barrels.push({
                        x: d > 0 ? -GRID_SIZE * 2 - i * gap : GAME_WIDTH + GRID_SIZE * 2 + i * gap,
                        y: row * GRID_SIZE, width: GRID_SIZE * 0.8, height: GRID_SIZE * 0.8, speed: sp * d, rotation: 0
                    });
                }
            }
        }
    }

    function move(dx, dy) {
        if (state !== 'playing' || player.moving) return;
        var gx = Math.floor(player.x / GRID_SIZE);
        var gy = Math.floor(player.y / GRID_SIZE);
        if (dy < 0 && gy > 0) { player.targetY = (gy - 1) * GRID_SIZE; player.moving = true; }
        if (dy > 0 && gy < ROWS - 1) { player.targetY = (gy + 1) * GRID_SIZE; player.moving = true; }
        if (dx < 0 && gx > 0) { player.targetX = (gx - 1) * GRID_SIZE; player.moving = true; }
        if (dx > 0 && gx < Math.floor(GAME_WIDTH / GRID_SIZE) - 1) { player.targetX = (gx + 1) * GRID_SIZE; player.moving = true; }
    }

    document.addEventListener('keydown', function (e) {
        var keys = { ArrowUp: [0, -1], ArrowDown: [0, 1], ArrowLeft: [-1, 0], ArrowRight: [1, 0] };
        if (!keys[e.key]) return;
        if (state === 'playing') e.preventDefault(); // keep the page from scrolling while playing
        move(keys[e.key][0], keys[e.key][1]);
    });

    function hit(a, b) {
        var pad = GRID_SIZE * 0.18;
        return (a.x + pad) < (b.x + b.width - pad) && (a.x + a.width - pad) > (b.x + pad) &&
               (a.y + pad) < (b.y + b.height - pad) && (a.y + a.height - pad) > (b.y + pad);
    }

    function gameOver() {
        if (state === 'gameOver') return;
        state = 'gameOver';
        finalEl.textContent = score;
        overEl.style.display = 'block';
        if (window.mtgTrack) window.mtgTrack('game_over', { game: 'crossy_customs', score: score });
    }

    function update() {
        if (state !== 'playing') return;
        if (player.moving) {
            var dx = player.targetX - player.x, dy = player.targetY - player.y;
            var dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < player.moveSpeed) { player.x = player.targetX; player.y = player.targetY; player.moving = false; }
            else { player.x += (dx / dist) * player.moveSpeed; player.y += (dy / dist) * player.moveSpeed; }
        }
        if (player.y <= 0 && !player.moving) {
            score++;
            level = Math.floor(score / 5) + 1;
            clearedEl.style.display = 'none';
            void clearedEl.offsetWidth;
            clearedEl.style.display = 'block';
            setTimeout(function () { clearedEl.style.display = 'none'; }, 1600);
            resetPlayer();
            generateObstacles();
            scoreEl.textContent = score;
            levelEl.textContent = level;
        }
        forklifts.forEach(function (f) {
            f.x += f.speed;
            if (f.speed > 0 && f.x > GAME_WIDTH + GRID_SIZE) f.x = -GRID_SIZE * 2;
            if (f.speed < 0 && f.x < -GRID_SIZE * 2) f.x = GAME_WIDTH + GRID_SIZE;
            if (hit(player, f)) gameOver();
        });
        officers.forEach(function (o) {
            o.x += o.speed * o.direction;
            if (o.x <= 0 || o.x >= GAME_WIDTH - o.width) o.direction *= -1;
            if (hit(player, o)) gameOver();
        });
        barrels.forEach(function (b) {
            b.x += b.speed;
            b.rotation += b.speed * 0.045;
            if (b.speed > 0 && b.x > GAME_WIDTH + GRID_SIZE) b.x = -GRID_SIZE * 2;
            if (b.speed < 0 && b.x < -GRID_SIZE * 2) b.x = GAME_WIDTH + GRID_SIZE;
            if (hit(player, b)) gameOver();
        });
    }

    function render() {
        ctx.clearRect(0, 0, GAME_WIDTH, GAME_HEIGHT);
        if (state === 'loading') {
            ctx.fillStyle = '#1F3244';
            ctx.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT);
            ctx.fillStyle = '#EA5C1F';
            ctx.font = 'bold 18px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('Loading...', GAME_WIDTH / 2, GAME_HEIGHT / 2);
            return;
        }
        ctx.strokeStyle = PALETTE.grid;
        ctx.lineWidth = 1;
        var i;
        for (i = 0; i <= GAME_WIDTH; i += GRID_SIZE) { ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, GAME_HEIGHT); ctx.stroke(); }
        for (i = 0; i <= GAME_HEIGHT; i += GRID_SIZE) { ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(GAME_WIDTH, i); ctx.stroke(); }
        ctx.fillStyle = PALETTE.topBand;
        ctx.fillRect(0, 0, GAME_WIDTH, GRID_SIZE);
        ctx.fillStyle = PALETTE.label;
        ctx.font = 'bold 13px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('WAREHOUSE / PORT', GAME_WIDTH / 2, GRID_SIZE / 2 + 5);
        ctx.fillStyle = PALETTE.startBand;
        ctx.fillRect(0, (ROWS - 1) * GRID_SIZE, GAME_WIDTH, GRID_SIZE);
        forklifts.forEach(function (f) { drawSprite('forklift', f.x, f.y, f.width, f.height, { flipH: f.speed < 0 }); });
        officers.forEach(function (o) { drawSprite('officer', o.x, o.y, o.width, o.height, { flipH: o.direction < 0 }); });
        barrels.forEach(function (b) { drawSprite('barrel', b.x, b.y, b.width, b.height, { rotation: b.rotation }); });
        drawSprite('truck', player.x, player.y, player.width, player.height);
    }

    function restart() {
        state = 'playing';
        score = 0; level = 1;
        resetPlayer();
        generateObstacles();
        scoreEl.textContent = score;
        levelEl.textContent = level;
        overEl.style.display = 'none';
        if (window.mtgTrack) window.mtgTrack('game_start', { game: 'crossy_customs' });
    }
    document.getElementById('gameRestart').addEventListener('click', restart);

    window.addEventListener('resize', function () {
        if (state !== 'playing' && state !== 'gameOver') return;
        resizeCanvas(); resetPlayer(); generateObstacles();
    });

    // swipe controls
    var tx = 0, ty = 0;
    canvas.addEventListener('touchstart', function (e) { e.preventDefault(); tx = e.touches[0].clientX; ty = e.touches[0].clientY; }, { passive: false });
    canvas.addEventListener('touchend', function (e) {
        e.preventDefault();
        var dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty, thr = 30;
        if (Math.abs(dx) > Math.abs(dy)) { if (dx > thr) move(1, 0); else if (dx < -thr) move(-1, 0); }
        else { if (dy > thr) move(0, 1); else if (dy < -thr) move(0, -1); }
    }, { passive: false });

    loadSprites(function () {
        state = 'playing';
        resetPlayer();
        generateObstacles();
        if (window.mtgTrack) window.mtgTrack('game_start', { game: 'crossy_customs' });
    });

    (function loop() { update(); render(); window.requestAnimationFrame(loop); })();
})();
