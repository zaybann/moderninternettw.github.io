// ပွဲစမယ့်အချိန်ကို သတ်မှတ်ခြင်း (မြန်မာစံတော်ချိန်)
const matchTime = new Date('October 9, 2025 00:00:00 GMT+0630').getTime();

// Countdown ကို update လုပ်မယ့် function
function updateCountdown() {
    const now = new Date().getTime();
    const distance = matchTime - now;

    // Element များကို ရယူခြင်း
    const matchDateElement = document.getElementById('matchDate');
    const matchStatusElement = document.getElementById('matchStatus');
    const countdownElement = document.getElementById('countdown');

    // စတင်ပွဲစဉ်အချက်အလက်များကို ပြသခြင်း
    matchDateElement.innerText = '9.10.2025';

    if (distance < 0) {
        // ပွဲစသွားပြီဆိုရင်
        clearInterval(countdownInterval);
        matchStatusElement.innerText = 'LIVE';
        countdownElement.style.display = 'none'; // အချိန်ရေတွက်မှုကို ဖျောက်လိုက်ခြင်း
        document.getElementById('score').style.color = '#e53935'; // ရမှတ်အရောင်ကို ပြန်ပြောင်းခြင်း
    } else {
        // ပွဲမစသေးပါက countdown ပြသခြင်း
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        matchStatusElement.innerText = 'Match starts in';
        countdownElement.innerText = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        countdownElement.style.display = 'block'; // အချိန်ရေတွက်မှုကို ပေါ်နေစေခြင်း
        document.getElementById('score').style.color = '#555'; // ရမှတ်အရောင်ကို မှိန်ထားခြင်း
    }
}

// စက္ကန့်တိုင်း update ဖြစ်အောင် ပြုလုပ်ခြင်း
const countdownInterval = setInterval(updateCountdown, 1000);

// စတင်တဲ့အခါ တစ်ခါတည်း update လုပ်ပေးဖို့
updateCountdown();
