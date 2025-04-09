
//const socket = io("http://54.180.77.228:8000");
const COOLDOWN = 3; //s

const user_id = Math.random().toString(36).substr(2, 8);
const username = document.getElementById('welcome').dataset.username;

const socket = io({
    query: {user_name: username}
});

let canPress = true;

const up = document.getElementById('up');
const left = document.getElementById('left');
const right = document.getElementById('right');
const down = document.getElementById('down');
const interact = document.getElementById('interact');
const attack = document.getElementById('attack');
const dash = document.getElementById('dash');
const special = document.getElementById('special');

const slider = document.getElementById('cooldownSlider');

up.addEventListener('click', () => sendInput('up'));
left.addEventListener('click', () => sendInput('left'));
right.addEventListener('click', () => sendInput('right'));
down.addEventListener('click', () => sendInput('down'));
interact.addEventListener('click', () => sendInput('interact'));
attack.addEventListener('click', () => sendInput('attack'));
dash.addEventListener('click', () => sendInput('dash'));
special.addEventListener('click', () => sendInput('special'));

function sendInput(input_btn) {
    if (!canPress) return;

    socket.emit('move_input', {
        user_name: username,
        user_id: user_id,
        input_btn: input_btn
    });

    startCooldown();
}

function startCooldown() {
    canPress = false;
    disableButtons(true);

    slider.value = 1;
    slider.max = 1;
    slider.min = 0;
    slider.disabled = false;

    let elapsed = 0;
    const step = 0.1;

    cooldownInterval = setInterval(() => {
        elapsed += step;
        slider.value = ((COOLDOWN - elapsed)/COOLDOWN).toFixed(2);

        if (elapsed >= COOLDOWN) {
            clearInterval(cooldownInterval);
            endCooldown();
        }
    }, step * 1000);
}

function endCooldown() {
    canPress = true;
    disableButtons(false);

    slider.value = 1;
    slider.disabled = true;
}

function disableButtons(disable) {
    up.disabled = disable;
    left.disabled = disable;
    right.disabled = disable;
    down.disabled = disable;
    interact.disabled = disable;
    attack.disabled = disable;
    dash.disabled = disable;
    special.disabled = disable;
}

