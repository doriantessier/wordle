let fin = false
let nb_max = 5
let essai = 0

async function startGame() {
  await fetch("http://127.0.0.1:8000/api/v1/wordle/new", { credentials: "include" })
  document.getElementById("game").innerHTML = ""
  document.getElementById("message").textContent = "Trouve mon mot ! Il fait 5 lettres, tu as 5 essais"
  essai = 0
  fin = false
}

async function sendGuess() {
  if (fin) return
  const input = document.getElementById("guessInput")
  const mot = input.value.trim().toUpperCase()
  if (mot.length !== 5) return
  const res = await fetch(`http://127.0.0.1:8000/api/v1/wordle/guess?mot=${mot}`, {
    credentials: "include"
  })
  const data = await res.json()

  if (data.error) {
    document.getElementById("message").textContent = data.error
    return
  }

  const ligne = document.createElement("div")
  for (const letterInfo of data.correct) {
    const span = document.createElement("span")
    span.textContent = letterInfo.letter
    span.className = `letter ${letterInfo.color}`
    ligne.appendChild(span)
  }
  document.getElementById("game").appendChild(ligne)
  input.value = ""
  essai++

  const won = data.correct.every(l => l.color === "green")
  if (won) {
    document.getElementById("message").textContent = "T'as trouvé le mot, bien joué !"
    fin = true
  } else if (essai >= nb_max) {
    document.getElementById("message").textContent = "Perdu, tu peux relancer une partie pour essayer de me battre cette fois !"
    fin = true
  }
}
