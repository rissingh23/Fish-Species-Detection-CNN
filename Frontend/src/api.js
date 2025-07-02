export async function predictImage(file) {
    const form = new FormData();
    form.append('file', file);
    const res = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      body: form,
    });
    if (!res.ok) throw new Error('Prediction failed');
    return res.json();
  }