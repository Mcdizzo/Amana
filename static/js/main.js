// Load counter on page load
fetch('/count')
    .then(r => r.json())
    .then(data => {
        document.getElementById('counter').textContent = data.count.toLocaleString();
    });

// Form submission
document.getElementById('waitlistForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const btn = document.getElementById('submitBtn');
    const msg = document.getElementById('formMsg');

    const payload = {
        name: document.getElementById('name').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value,
        location: document.getElementById('location').value
    };

    btn.disabled = true;
    btn.textContent = 'Inasajili...';
    msg.className = 'form-msg';
    msg.textContent = '';

    try {
        const res = await fetch('/join', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (data.success) {
            msg.className = 'form-msg success';
            msg.textContent = data.message;
            document.getElementById('counter').textContent = data.count.toLocaleString();
            showShare(payload.name, payload.location);
            this.reset();
            btn.textContent = 'Umefanikiwa ✓';
        } else {
            msg.className = 'form-msg error';
            msg.textContent = data.message;
            btn.disabled = false;
            btn.textContent = 'Hifadhi Nafasi Yangu →';
        }

    } catch (err) {
        msg.className = 'form-msg error';
        msg.textContent = 'Hitilafu imetokea. Jaribu tena.';
        btn.disabled = false;
        btn.textContent = 'Hifadhi Nafasi Yangu →';
    }
});

function showShare(name, location) {
    const section = document.getElementById('shareSection');
    const msgEl = document.getElementById('shareMsg');
    const waBtn = document.getElementById('whatsappBtn');
    const copyBtn = document.getElementById('copyBtn');

    const message = `🇹🇿 Nimejiunga na Amana!\n\nApp mpya inayokuwezesha kuwekeza Tanzania ukiwa popote ulipo — salama, rahisi, kwa Kiswahili.\n\nSerikali inatoa riba ya 10.75% kwa mwaka. Pesa yako inafanya kazi nyumbani.\n\nJiunge nawe: amana.tz\n\n"Mcheza Kwao Hutunzwa."`;

    msgEl.textContent = message;
    waBtn.href = `https://wa.me/?text=${encodeURIComponent(message)}`;

    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(message).then(() => {
            copyBtn.textContent = 'Imenakiliwa ✓';
            setTimeout(() => copyBtn.textContent = 'Nakili Ujumbe', 2000);
        });
    });

    section.style.display = 'block';
    section.scrollIntoView({ behavior: 'smooth' });
}

// Contact form
document.getElementById('contactForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const btn = document.getElementById('contactBtn');
    const msg = document.getElementById('contactMsg');

    const payload = {
        name: document.getElementById('contactName').value,
        phone: document.getElementById('contactPhone').value,
        message: document.getElementById('contactMessage').value
    };

    btn.disabled = true;
    btn.textContent = 'Inatuma...';
    msg.className = 'form-msg';
    msg.textContent = '';

    try {
        const res = await fetch('/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (data.success) {
            msg.className = 'form-msg success';
            msg.textContent = data.message;
            this.reset();
            btn.textContent = 'Umetumwa ✓';
        } else {
            msg.className = 'form-msg error';
            msg.textContent = data.message;
            btn.disabled = false;
            btn.textContent = 'Tuma Ujumbe →';
        }

    } catch (err) {
        msg.className = 'form-msg error';
        msg.textContent = 'Hitilafu imetokea. Jaribu tena.';
        btn.disabled = false;
        btn.textContent = 'Tuma Ujumbe →';
    }
});