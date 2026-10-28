import "./style.css";

type Source = { number: number; section: string; url: string };
type AnswerResponse = { answer: string; flagged: boolean; score: number | null; sources: Source[] };

const API_URL = "http://localhost:8000/answer";

async function askQuestion(question: string): Promise<AnswerResponse> {
  const response = await fetch(API_URL, {                         
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({question: question}),                            
  });
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);   
  return await response.json();
}

function displayResult(data: AnswerResponse) {
  const answerEl = document.querySelector<HTMLDivElement>("#answer")!;
  answerEl.textContent = data.answer;                             

  const flagEl = document.querySelector<HTMLDivElement>("#flag")!;
  flagEl.hidden = !data.flagged;                                    

  const scoreEl = document.querySelector<HTMLSpanElement>("#score")!;
  scoreEl.textContent = data.score === null ? "n/a" : data.score.toFixed(2);

  const sourcesEl = document.querySelector<HTMLOListElement>("#sources")!;
  sourcesEl.innerHTML = "";                                 
  for (const source of data.sources) {
    const li = document.createElement("li");
    const link = document.createElement("a");
    link.href = source.url;
    link.target = "_blank";                                  
    link.textContent =  `[${source.number}] ${source.section}`;                                 
    li.appendChild(link);
    sourcesEl.appendChild(li);
  }

  document.querySelector<HTMLElement>("#result")!.hidden = false;
}

const form = document.querySelector<HTMLFormElement>("#ask-form")!;
const questionEl = document.querySelector<HTMLTextAreaElement>("#question")!;
const button = document.querySelector<HTMLButtonElement>("#ask-button")!;
const loadingEl = document.querySelector<HTMLParagraphElement>("#loading")!;
const errorEl = document.querySelector<HTMLParagraphElement>("#error")!;
const resultEl = document.querySelector<HTMLElement>("#result")!;

form.addEventListener("submit", async (event) => {
  event.preventDefault();                       
  const question = questionEl.value.trim();
  if (!question) return;                       

  loadingEl.hidden = false;
  errorEl.hidden = true;
  resultEl.hidden = true;
  button.disabled = true;                       

  try {
    const data = await askQuestion(question);                          
    displayResult(data);                                 
  } catch (error) {
    console.error(error);
    errorEl.textContent = "Something went wrong. Is the API running on port 8000?";
    errorEl.hidden = false;
  } finally {
    loadingEl.hidden = true;                    
    button.disabled = false;
  }
});