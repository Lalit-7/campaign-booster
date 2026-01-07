async function analyzeCampaign() {
  const title = document.getElementById("title").value.trim();
  const description = document.getElementById("description").value.trim();
  const goal = document.getElementById("goal").value.trim();

  if (!description) {
    alert("Please paste the campaign description");
    return;
  }

  const response = await fetch("/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, description, goal })
  });

  const data = await response.json();

  document.getElementById("results").classList.remove("hidden");

  document.getElementById("score").innerText = data.score;
  document.getElementById("betterTitle").innerText = data.better_title;
  document.getElementById("betterStory").innerText = data.better_story;

  const trust = document.getElementById("trust");
  trust.innerText = data.trust_level;

  trust.className = "";
  trust.classList.add(
    data.trust_level === "High" ? "trust-high" :
    data.trust_level === "Medium" ? "trust-medium" :
    "trust-low"
  );

  const list = document.getElementById("suggestions");
  list.innerHTML = "";
  data.suggestions.forEach(s => {
    const li = document.createElement("li");
    li.innerText = s;
    list.appendChild(li);
  });
}
