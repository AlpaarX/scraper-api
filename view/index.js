const host = "http://localhost:8000";

async function load() {
  const city = document.getElementById("city").value;
  const pref = document.getElementById("pref").value;
  const url = `${host}/scrape/?city=${city}&prefecture=${pref}`;
  const res = await fetch(url);
  const data = await res.json();
  console.log(data);
  toArr(data, city);
}

function toArr(data, city) {
  const freqData = data.frequency;
  const price = Object.keys(freqData).map((key) => key);
  const frequency = Object.keys(freqData).map((key) => freqData[key]);
  render(price, frequency, data, city);
}

function render(x, y, data, city) {
  const listings = data.listings;
  const title = document.getElementById("title");
  title.innerHTML = `${listings} listings in ${city}`;

  const CHART = document.getElementById("chart");
  Plotly.newPlot(
    CHART,
    [
      {
        x: x, // yoko
        y: y, // tate
        type: "bar",
      },
    ],
    {
      margin: { t: 0 },
    }
  );
}

document.getElementById("search").addEventListener("click", (e) => load());
