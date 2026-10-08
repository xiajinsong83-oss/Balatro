// Balatro Score Calculator
document.addEventListener('DOMContentLoaded', function() {
  const handSelect = document.getElementById('hand-type');
  const chipsInput = document.getElementById('card-chips');
  const multInput = document.getElementById('joker-mult');
  const retriggersInput = document.getElementById('retriggers');
  const resultValue = document.getElementById('score-result');

  if (!handSelect) return;

  const handBase = {
    'high-card': { chips: 5, mult: 1 },
    'pair': { chips: 10, mult: 2 },
    'two-pair': { chips: 20, mult: 2 },
    'three-kind': { chips: 30, mult: 3 },
    'straight': { chips: 30, mult: 4 },
    'flush': { chips: 35, mult: 4 },
    'full-house': { chips: 40, mult: 4 },
    'four-kind': { chips: 60, mult: 7 },
    'straight-flush': { chips: 100, mult: 8 },
    'royal-flush': { chips: 100, mult: 8 },
    'five-kind': { chips: 120, mult: 12 }
  };

  function calculate() {
    const base = handBase[handSelect.value];
    const chips = base.chips + (parseInt(chipsInput.value) || 0);
    const mult = base.mult + (parseInt(multInput.value) || 0);
    const retrigger = parseInt(retriggersInput.value) || 1;
    resultValue.textContent = (chips * mult * retrigger).toLocaleString();
  }

  [handSelect, chipsInput, multInput, retriggersInput].forEach(el => {
    el.addEventListener('input', calculate);
  });
  calculate();

  // FAQ accordion
  document.querySelectorAll('.faq-question').forEach(q => {
    q.addEventListener('click', function() {
      this.parentElement.classList.toggle('open');
    });
  });
});
