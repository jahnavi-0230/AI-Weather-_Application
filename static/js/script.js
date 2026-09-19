const form = document.querySelector('#weather-form');
const cityInput = document.querySelector('#city');
const submitButton = form.querySelector('button');
const status = document.querySelector('#status');
const result = document.querySelector('#result');
const setText = (id, value) => { document.querySelector(id).textContent = value; };
form.addEventListener('submit', async (event) => {
  event.preventDefault(); const city = cityInput.value.trim();
  if (!city) { status.textContent = 'Enter a city name.'; cityInput.focus(); return; }
  status.textContent = 'Getting current weather…'; result.hidden = true; submitButton.disabled = true;
  try {
    const response = await fetch('/api/weather', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ city }) });
    const data = await response.json(); if (!response.ok) throw new Error(data.error || 'Unable to get weather.');
    const w = data.weather; setText('#location', `${w.city}${w.country ? `, ${w.country}` : ''}`); setText('#condition', w.description); setText('#temperature', Math.round(w.temperature)); setText('#feels-like', `${Math.round(w.feels_like)}°C`); setText('#humidity', `${w.humidity}%`); setText('#wind', `${w.wind_speed} m/s`); setText('#visibility', `${w.visibility_km} km`);
    setText('#ai-explanation', data.ai_explanation || 'Weather details are available, but an AI explanation could not be generated.');
    const warning = document.querySelector('#ai-warning'); warning.hidden = !data.ai_error; warning.textContent = data.ai_error || '';
    const icon = document.querySelector('#weather-icon'); icon.hidden = !w.icon; icon.src = `https://openweathermap.org/img/wn/${w.icon}@2x.png`; icon.alt = w.description;
    result.hidden = false; status.textContent = '';
  } catch (error) { status.textContent = error.message; } finally { submitButton.disabled = false; }
});
