const scriptTag = document.currentScript;
const ID_PRODUTO = scriptTag.dataset.idProduto;

const container = document.getElementById("produto-detalhe");
const breadcrumbProduto = document.getElementById("breadcrumb-produto");

const ICONE_CARRINHO = `
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M3 3h2l.4 2M7 13h10l3-8H5.4M7 13L5.4 5M7 13l-2.3 4.6A1 1 0 0 0 5.6 19H17M17 19a2 2 0 1 0 0 4 2 2 0 0 0 0-4ZM9 19a2 2 0 1 0 0 4 2 2 0 0 0 0-4Z"
      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
`;

function formatarPreco(preco) {
    const numero = Number(preco);
    if (Number.isNaN(numero)) return "Sob consulta";
    return numero.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function imagemUrlSegura(url) {
    if (!url) return "";
    return encodeURI(url)
        .replace(/\(/g, "%28")
        .replace(/\)/g, "%29")
        .replace(/'/g, "%27");
}

function adicionarAoCarrinho(produto, quantidade) {
    const CHAVE = "inovatech_carrinho";
    let carrinho = [];
    try {
        carrinho = JSON.parse(localStorage.getItem(CHAVE)) || [];
    } catch (e) {
        carrinho = [];
    }

    const existente = carrinho.find((item) => item.id_produto === produto.id_produto);
    if (existente) {
        existente.quantidade += quantidade;
    } else {
        carrinho.push({
            id_produto: produto.id_produto,
            nome: produto.nome,
            preco: Number(produto.preco),
            imagem_url: produto.imagem_url,
            quantidade,
        });
    }

    localStorage.setItem(CHAVE, JSON.stringify(carrinho));
    return carrinho;
}

function mostrarToast(mensagem) {
    const toastAntigo = document.querySelector(".toast-carrinho");
    if (toastAntigo) toastAntigo.remove();

    const toast = document.createElement("div");
    toast.className = "toast-carrinho";
    toast.textContent = mensagem;
    document.body.appendChild(toast);

    requestAnimationFrame(() => toast.classList.add("toast-carrinho--visivel"));

    setTimeout(() => {
        toast.classList.remove("toast-carrinho--visivel");
        setTimeout(() => toast.remove(), 300);
    }, 2200);
}

function renderizarProduto(produto) {
    breadcrumbProduto.textContent = produto.nome;
    document.title = `${produto.nome} — InovaTech Supply`;

    const estoque = Number(produto.estoque);
    const emEstoque = !Number.isFinite(estoque) || estoque > 0;
    const imagemProduto = imagemUrlSegura(produto.imagem_url || "");

    container.innerHTML = `
        <div class="produto-layout">
            <div class="produto-imagem" style="background-image: url('${imagemProduto}')">
            </div>

            <div class="produto-info">
                ${produto.categoria ? `<span class="produto-categoria">${produto.categoria}</span>` : ""}
                <h1 class="produto-titulo"></h1>
                <p class="produto-descricao"></p>

                <div class="produto-preco-linha">
                    <span class="produto-preco"></span>
                    <span class="produto-status ${emEstoque ? "produto-status--ok" : "produto-status--esgotado"}">
                        ${emEstoque ? "Em estoque" : "Esgotado"}
                    </span>
                </div>

                <div class="produto-acoes">
                    <div class="produto-quantidade">
                        <button type="button" class="qtd-btn" id="qtd-menos" aria-label="Diminuir quantidade">−</button>
                        <input type="number" id="qtd-input" value="1" min="1" max="${Number.isFinite(estoque) ? estoque : 99}" aria-label="Quantidade">
                        <button type="button" class="qtd-btn" id="qtd-mais" aria-label="Aumentar quantidade">+</button>
                    </div>

                    <button type="button" class="btn-adicionar-carrinho" id="btn-adicionar" ${!emEstoque ? "disabled" : ""}>
                        ${ICONE_CARRINHO}
                        <span>${emEstoque ? "Adicionar ao carrinho" : "Indisponível"}</span>
                    </button>
                </div>
            </div>
        </div>
    `;

    // Texto via textContent (evita injeção de HTML vindo do banco)
    container.querySelector(".produto-titulo").textContent = produto.nome || "Produto";
    container.querySelector(".produto-descricao").textContent =
        produto.descricao || "Sem descrição disponível para este produto.";
    container.querySelector(".produto-preco").textContent = formatarPreco(produto.preco);

    const qtdInput = document.getElementById("qtd-input");
    document.getElementById("qtd-menos").addEventListener("click", () => {
        qtdInput.value = Math.max(1, Number(qtdInput.value) - 1);
    });
    document.getElementById("qtd-mais").addEventListener("click", () => {
        const max = Number(qtdInput.max) || 99;
        qtdInput.value = Math.min(max, Number(qtdInput.value) + 1);
    });

    const btnAdicionar = document.getElementById("btn-adicionar");
    if (btnAdicionar) {
        btnAdicionar.addEventListener("click", () => {
            const quantidade = Math.max(1, Number(qtdInput.value) || 1);
            adicionarAoCarrinho(produto, quantidade);
            mostrarToast(`${produto.nome} adicionado ao carrinho (${quantidade}x)`);
        });
    }
}

function mostrarErro() {
    breadcrumbProduto.textContent = "Produto não encontrado";
    container.innerHTML = `
        <div class="status-mensagem">
            <strong>Não encontramos esse produto</strong>
            Ele pode ter sido removido ou o link está incorreto.
            <br>
            <a href="/" class="status-mensagem-link">Voltar ao catálogo</a>
        </div>
    `;
}

async function carregarProduto() {
    try {
        const response = await fetch(`/produtos/${ID_PRODUTO}`);
        if (!response.ok) {
            throw new Error(`Erro HTTP ${response.status}`);
        }
        const produto = await response.json();
        renderizarProduto(produto);
    } catch (erro) {
        console.error("Falha ao carregar produto:", erro);
        mostrarErro();
    }
}

document.addEventListener("DOMContentLoaded", carregarProduto);