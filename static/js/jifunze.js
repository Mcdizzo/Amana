const COUPON_RATE = 0.1025;
const YEARS = 5;

function formatTZS(amount) {
    return 'TZS ' + Math.round(amount).toLocaleString('en-US');
}

function calculate(amount) {
    const annual = amount * COUPON_RATE;
    const semiAnnual = annual / 2;
    const totalReturn = annual * YEARS;
    const grandTotal = amount + totalReturn;

    document.getElementById('annualReturn').textContent = formatTZS(annual);
    document.getElementById('semiAnnual').textContent = formatTZS(semiAnnual);
    document.getElementById('totalReturn').textContent = formatTZS(totalReturn);
    document.getElementById('grandTotal').textContent = formatTZS(grandTotal);
}

const amountInput = document.getElementById('investAmount');
const slider = document.getElementById('investSlider');

amountInput.addEventListener('input', () => {
    const val = parseInt(amountInput.value) || 1000000;
    slider.value = Math.min(val, 10000000);
    calculate(val);
});

slider.addEventListener('input', () => {
    amountInput.value = slider.value;
    calculate(parseInt(slider.value));
});

// Init
calculate(1000000);