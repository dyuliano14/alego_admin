const flashcards = [
    { pergunta: "Qual é o objetivo principal do Regimento Interno?", resposta: "Estabelecer normas para o funcionamento da instituição." },
    { pergunta: "Quem é responsável por modificar o Regimento Interno?", resposta: "A Assembleia Geral, mediante votação." },
    { pergunta: "Com que frequência o Regimento Interno deve ser revisado?", resposta: "A cada dois anos ou quando necessário." },
    // Adicione mais flashcards conforme necessário
];

let indiceAtual = 0;
const flashcard = document.getElementById("flashcard");
const pergunta = document.getElementById("pergunta");
const resposta = document.getElementById("resposta");

function exibirFlashcard(indice) {
    const card = flashcards[indice];
    pergunta.textContent = card.pergunta;
    resposta.textContent = card.resposta;
    flashcard.classList.remove("flipped");
}

function proximoFlashcard() {
    indiceAtual = (indiceAtual + 1) % flashcards.length;
    exibirFlashcard(indiceAtual);
}

function flashcardAnterior() {
    indiceAtual = (indiceAtual - 1 + flashcards.length) % flashcards.length;
    exibirFlashcard(indiceAtual);
}

function embaralharFlashcards() {
    for (let i = flashcards.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [flashcards[i], flashcards[j]] = [flashcards[j], flashcards[i]];
    }
    indiceAtual = 0;
    exibirFlashcard(indiceAtual);
}

flashcard.addEventListener("click", () => {
    flashcard.classList.toggle("flipped");
});

document.getElementById("proximo").addEventListener("click", proximoFlashcard);
document.getElementById("anterior").addEventListener("click", flashcardAnterior);
document.getElementById("embaralhar").addEventListener("click", embaralharFlashcards);

// Navegação via teclado
document.addEventListener("keydown", (event) => {
    switch (event.key) {
        case "ArrowRight":
            proximoFlashcard();
            break;
        case "ArrowLeft":
            flashcardAnterior();
            break;
        case "Enter":
            flashcard.classList.toggle("flipped");
            break;
    }
});

// Inicialização
exibirFlashcard(indiceAtual);

document.addEventListener("DOMContentLoaded", () => {
    const checkboxes = document.querySelectorAll(".tarefa");
    const progresso = document.getElementById("progresso");

    function atualizarProgresso() {
        const total = checkboxes.length;
        const marcadas = Array.from(checkboxes).filter(c => c.checked).length;
        const percentual = (marcadas / total) * 100;
        progresso.value = percentual;
        localStorage.setItem("progresso_regimento", percentual);
        checkboxes.forEach((cb, idx) => {
            localStorage.setItem(`tarefa_regimento_${idx}`, cb.checked);
        });
    }

    checkboxes.forEach((cb, idx) => {
        cb.checked = localStorage.getItem(`tarefa_regimento_${idx}`) === "true";
        cb.addEventListener("change", atualizarProgresso);
    });

    const progressoSalvo = localStorage.getItem("progresso_regimento");
    if (progressoSalvo) progresso.value = progressoSalvo;
});


